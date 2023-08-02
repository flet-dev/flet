package page

import (
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"strconv"
	"strings"
	"time"

	"github.com/flet-dev/flet/server/cache"
	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/model"
	"github.com/flet-dev/flet/server/pubsub"
	"github.com/flet-dev/flet/server/store"
	log "github.com/sirupsen/logrus"
)

const (
	// ZeroSession is ID of zero session
	ZeroSession string = "0"
	// ControlAutoIDPrefix is a prefix for auto-generated control IDs
	ControlAutoIDPrefix = "_"
	// ControlIDSeparator is a symbol between parts of control ID
	ControlIDSeparator = ":"
	// ReservedPageID is a reserved page ID
	ReservedPageID        = "page"
	sessionCrashedMessage = "There was an error while processing your request. Please refresh the page to start a new session."
)

type commandHandlerFn = func(*model.Command) (string, error)

type sessionHandler struct {
	session *model.Session
}

func newSessionHandler(session *model.Session) sessionHandler {
	return sessionHandler{
		session: session,
	}
}

type addCommandBatchItem struct {
	command *model.Command
	control *model.Control
}

// NewSession creates a new instance of Session.
func newSession(page *model.Page, id string, clientIP string, clientUserAgent string,
	pageRoute string, pageWidth string, pageHeight string,
	windowWidth string, windowHeight string,
	windowTop string, windowLeft string, isPwa string, isWeb string, isDebug string, platform string, platformBrightness string) *model.Session {
	s := &model.Session{}
	s.Page = page
	s.ID = id
	s.ClientIP = clientIP

	store.AddSession(s)

	h := newSessionHandler(s)
	p := model.NewControl("page", "", ReservedPageID)
	p.SetAttr("route", pageRoute)
	p.SetAttr("width", pageWidth)
	p.SetAttr("height", pageHeight)
	p.SetAttr("windowwidth", windowWidth)
	p.SetAttr("windowheight", windowHeight)
	p.SetAttr("windowtop", windowTop)
	p.SetAttr("windowleft", windowLeft)
	p.SetAttr("pwa", isPwa)
	p.SetAttr("web", isWeb)
	p.SetAttr("debug", isDebug)
	p.SetAttr("platform", platform)
	p.SetAttr("platformBrightness", platformBrightness)
	p.SetAttr("clientIP", clientIP)
	p.SetAttr("clientUserAgent", clientUserAgent)
	h.addControl(p)

	return s
}

func (h *sessionHandler) extendExpiration() {
	var expiresInMinutes int
	if h.session.ID == ZeroSession {
		expiresInMinutes = config.PageLifetimeMinutes()
	} else {
		expiresInMinutes = config.AppLifetimeMinutes()
	}
	store.SetSessionExpiration(h.session, time.Now().Add(time.Duration(expiresInMinutes)*time.Minute))
}

// ExecuteCommand executes command and returns the result
func (h *sessionHandler) execute(cmd *model.Command) (result string, err error) {
	sl := h.lockSession()
	defer sl.Unlock()

	log.Debugf("Execute command for page %s session %s: %+v\n",
		h.session.Page.Name, h.session.ID, cmd)

	handlers := map[string]commandHandlerFn{
		model.AddCommand:            h.add,
		model.ReplaceCommand:        h.replace,
		model.SetCommand:            h.set,
		model.AppendCommand:         h.appendHandler,
		model.GetCommand:            h.get,
		model.CleanCommand:          h.clean,
		model.RemoveCommand:         h.remove,
		model.OAuthAuthorizeCommand: h.oauthAuthorize,
		model.InvokeMethodCommand:   h.invokeMethod,
		model.GetUploadUrlCommand:   h.getUploadUrl,
		model.ErrorCommand:          h.sessionCrashed,
	}

	handler := handlers[strings.ToLower(cmd.Name)]
	if handler == nil {
		return "", fmt.Errorf("unknown command: %s", cmd.Name)
	}

	return handler(cmd)
}

func (h *sessionHandler) executeBatch(commands []*model.Command) (results []string, err error) {
	results = make([]string, 0)
	messages := make([]*Message, 0)

	for _, cmd := range commands {
		cmdName := strings.ToLower(cmd.Name)
		if cmdName == model.AddCommand {
			// add
			ids, trimIDs, controls, err := h.addInternal(cmd)
			if err != nil {
				return nil, err
			}
			results = append(results, strings.Join(ids, " "))
			messages = append(messages, NewMessage("", AddPageControlsAction, &AddPageControlsPayload{
				Controls: controls,
				TrimIDs:  trimIDs,
			}))
		} else if cmdName == model.SetCommand {
			payload, err := h.setInternal(cmd)
			if err != nil {
				return nil, err
			}
			messages = append(messages, NewMessage("", UpdateControlPropsAction, payload))
		} else if cmdName == model.GetCommand {
			value, err := h.get(cmd)
			if err != nil {
				return nil, err
			}
			results = append(results, value)
		} else if cmdName == model.CleanCommand {
			payload, err := h.cleanWithMessage(cmd)
			if err != nil {
				return nil, err
			}
			messages = append(messages, NewMessage("", CleanControlAction, payload))
		} else if cmdName == model.RemoveCommand {
			payload, err := h.removeWithMessage(cmd)
			if err != nil {
				return nil, err
			}
			messages = append(messages, NewMessage("", RemoveControlAction, payload))
		}
	}

	// broadcast all message to clients
	if len(messages) > 0 {
		h.broadcastCommandToWebClients(NewMessage("", PageControlsBatchAction, messages))
	}

	return results, nil
}

func (h *sessionHandler) add(cmd *model.Command) (result string, err error) {
	ids, trimIDs, controls, err := h.addInternal(cmd)
	if err != nil {
		return "", err
	}

	// broadcast new controls to all connected web clients
	h.broadcastCommandToWebClients(NewMessage("", AddPageControlsAction, &AddPageControlsPayload{
		Controls: controls,
		TrimIDs:  trimIDs,
	}))
	return strings.Join(ids, " "), nil
}

func (h *sessionHandler) addInternal(cmd *model.Command) (ids []string, trimIDs []string, controls []*model.Control, err error) {

	// parent ID
	topParentID := cmd.Attrs["to"]
	topParentAt := -1
	if ta, err := strconv.Atoi(cmd.Attrs["at"]); err == nil {
		topParentAt = ta
	}

	// trim
	trim := 0
	if tc, err := strconv.Atoi(cmd.Attrs["trim"]); err == nil {
		trim = tc
	}

	if topParentID == "" {
		topParentID = ReservedPageID
	}

	// "Add" commands to process
	batch := make([]*addCommandBatchItem, 0)

	// top command
	if len(cmd.Values) > 0 {
		// single command
		batch = append(batch, &addCommandBatchItem{
			command: cmd,
		})
	}

	// sub-commands
	for _, childCmd := range cmd.Commands {
		childCmd.Name = "add"
		batch = append(batch, &addCommandBatchItem{
			command: childCmd,
		})
	}

	// list of control IDs
	ids = make([]string, 0)

	// list of controls to broadcast
	controls = make([]*model.Control, 0)

	affectedParents := make(map[string]bool)

	// process batch
	for i, batchItem := range batch {

		// first value must be control type
		if len(batchItem.command.Values) == 0 {
			return nil, nil, nil, errors.New("control type is not specified")
		}

		controlType := strings.ToLower(batchItem.command.Values[0])

		// other values go to boolean properties
		if len(batchItem.command.Values) > 1 {
			for _, v := range batchItem.command.Values[1:] {
				batchItem.command.Attrs[strings.ToLower(v)] = "true"
			}
		}

		parentID := ""
		parentAt := -1

		// find nearest parentID
		for pi := i - 1; pi >= 0; pi-- {
			if batch[pi].command.Indent < batchItem.command.Indent {
				parentID = batch[pi].control.ID()
				break
			}
		}

		// parent wasn't found - use the topmost one
		if parentID == "" {
			parentID = topParentID
			parentAt = topParentAt
		}

		// control ID
		id := batchItem.command.Attrs["id"]
		if id == "" {
			id = h.nextControlID()
		}
		// generate unique ID
		parentIDs := h.getControlParentIDs(parentID)
		id = strings.Join(append(parentIDs, id), ControlIDSeparator)

		batchItem.control = model.NewControl(controlType, parentID, id)
		affectedParents[parentID] = true

		if parentAt != -1 {
			batchItem.control.SetAttr("at", strconv.Itoa(parentAt))
			topParentAt++
		}

		for k, v := range batchItem.command.Attrs {
			if !model.IsSystemAttr(k) && v != "" {
				batchItem.control.SetAttr(k, v)
			}
		}

		err := h.addControl(batchItem.control)
		if err != nil {
			return nil, nil, nil, err
		}
		controls = append(controls, batchItem.control)
		ids = append(ids, id)
	}

	// re-read affected parents
	for i, ctrl := range controls {
		if affectedParents[ctrl.ID()] {
			controls[i] = store.GetSessionControl(h.session, ctrl.ID())
		}
	}

	// trim
	trimIDs = make([]string, 0)
	if trim != 0 {
		// negative - trim from the end
		// positive - trim from the start
		childIDs := h.getControl(topParentID).GetChildrenIds()
		trimCount := int(math.Abs(float64(trim)))
		if len(childIDs) > trimCount {
			if trim < 0 {
				trimIDs = childIDs[trimCount:]
			} else {
				trimIDs = childIDs[:len(childIDs)-trimCount]
			}
			h.removeInternal(trimIDs, -1)
		}
	}

	return
}

func (h *sessionHandler) replace(cmd *model.Command) (result string, err error) {

	// parent ID
	parentID := cmd.Attrs["to"]

	if parentID == "" {
		parentID = ReservedPageID
	}

	at := -1
	if a, err := strconv.Atoi(cmd.Attrs["at"]); err == nil {
		at = a
	}

	// clean control
	var allIDs []string
	if at == -1 {
		allIDs, err = h.cleanInternal([]string{parentID}, -1)
	} else {
		allIDs, err = h.removeInternal([]string{parentID}, at)
	}

	if err != nil {
		return "", err
	}

	cmd.Name = "add"
	ids, _, controls, err := h.addInternal(cmd)
	if err != nil {
		return "", err
	}

	// broadcast new controls to all connected web clients
	h.broadcastCommandToWebClients(NewMessage("", ReplacePageControlsAction, &ReplacePageControlsPayload{
		IDs:      allIDs,
		Remove:   at != -1,
		Controls: controls,
	}))
	return strings.Join(ids, " "), nil
}

func (h *sessionHandler) get(cmd *model.Command) (result string, err error) {

	// command format must be:
	// get <control-id> <property>
	if len(cmd.Values) < 2 {
		return "", errors.New("'get' command should have control ID and property specified")
	}

	// control ID
	id := cmd.Values[0]

	ctrl := h.getControl(id)
	if ctrl == nil {
		return "", fmt.Errorf("control with ID '%s' not found", id)
	}

	// control property
	prop := cmd.Values[1]

	v := ctrl.GetAttr(prop)

	if v == nil {
		return "", nil
	}

	return v.(string), nil
}

func (h *sessionHandler) set(cmd *model.Command) (result string, err error) {
	payload, err := h.setInternal(cmd)
	if err != nil {
		return "", err
	}

	// broadcast control updates to all connected web clients
	h.broadcastCommandToWebClients(NewMessage("", UpdateControlPropsAction, payload))
	return "", nil
}

func (h *sessionHandler) setInternal(cmd *model.Command) (result *UpdateControlPropsPayload, err error) {

	batch := make([]*model.Command, 0)

	// top command
	if len(cmd.Values) > 0 {
		// single command
		batch = append(batch, cmd)
	}

	// sub-commands
	for _, childCmd := range cmd.Commands {
		childCmd.Name = "set"
		batch = append(batch, childCmd)
	}

	payload := &UpdateControlPropsPayload{
		Props: make([]map[string]string, 0),
	}

	for _, batchCmd := range batch {
		// command format must be:
		// get <control-id> <property>
		if len(batchCmd.Values) < 1 {
			return nil, errors.New("'set' command should have control ID specified")
		}

		// control ID
		id := batchCmd.Values[0]

		ctrl := h.getControl(id)
		if ctrl == nil {
			return nil, fmt.Errorf("control with ID '%s' not found", id)
		}

		// other values go to boolean properties
		if len(batchCmd.Values) > 1 {
			for _, v := range batchCmd.Values[1:] {
				batchCmd.Attrs[strings.ToLower(v)] = "true"
			}
		}

		props := make(map[string]string)
		props["i"] = id

		// set control properties, except system ones
		for n, v := range batchCmd.Attrs {
			if !model.IsSystemAttr(n) {
				ctrl.SetAttr(n, v)
				props[strings.ToLower(n)] = v
			}
		}
		err = store.SetSessionControl(h.session, ctrl)
		if err != nil {
			return nil, err
		}

		payload.Props = append(payload.Props, props)
	}

	return payload, nil
}

func (h *sessionHandler) appendHandler(cmd *model.Command) (result string, err error) {
	payload, err := h.appendHandlerInternal(cmd)
	if err != nil {
		return "", err
	}

	// broadcast control updates to all connected web clients
	h.broadcastCommandToWebClients(NewMessage("", AppendControlPropsAction, payload))
	return "", nil
}

func (h *sessionHandler) appendHandlerInternal(cmd *model.Command) (result *AppendControlPropsPayload, err error) {

	batch := make([]*model.Command, 0)

	// top command
	if len(cmd.Values) > 0 {
		// single command
		batch = append(batch, cmd)
	}

	// sub-commands
	for _, childCmd := range cmd.Commands {
		childCmd.Name = "append"
		batch = append(batch, childCmd)
	}

	payload := &AppendControlPropsPayload{
		Props: make([]map[string]string, 0),
	}

	for _, batchCmd := range batch {
		// command format must be:
		// append control-id property=value property=value ...
		if len(batchCmd.Values) < 1 {
			return nil, errors.New("'append' command should have control ID specified")
		}

		// control ID
		id := batchCmd.Values[0]

		ctrl := h.getControl(id)
		if ctrl == nil {
			return nil, fmt.Errorf("control with ID '%s' not found", id)
		}

		props := make(map[string]string)
		props["i"] = id

		// set control properties, except system ones
		for n, v := range batchCmd.Attrs {
			if !model.IsSystemAttr(n) {
				ctrl.AppendAttr(n, v)
				props[n] = v
			}
		}
		err = store.SetSessionControl(h.session, ctrl)
		if err != nil {
			return nil, err
		}

		payload.Props = append(payload.Props, props)
	}

	return payload, nil
}

func (h *sessionHandler) clean(cmd *model.Command) (result string, err error) {

	payload, err := h.cleanWithMessage(cmd)
	if err != nil {
		return "", err
	}

	// broadcast command to all connected web clients
	h.broadcastCommandToWebClients(NewMessage("", CleanControlAction, payload))
	return "", nil
}

func (h *sessionHandler) cleanWithMessage(cmd *model.Command) (result *CleanControlPayload, err error) {

	// command format:
	//    clean [id_1] [id_2] ... [at=index]

	ids := make([]string, 0)
	if len(cmd.Values) == 0 {
		// clean page if no IDs specified
		ids = append(ids, ReservedPageID)
	} else {
		ids = append(ids, cmd.Values...)
	}

	at := -1
	if a, err := strconv.Atoi(cmd.Attrs["at"]); err == nil {
		at = a
	}

	if at != -1 && len(ids) > 1 {
		return nil, errors.New("'at' cannot be specified with a list of IDs")
	}

	allIds, err := h.cleanInternal(ids, at)
	if err != nil {
		return nil, err
	}

	return &CleanControlPayload{
		IDs: allIds,
	}, nil
}

func (h *sessionHandler) cleanInternal(ids []string, at int) (allIDs []string, err error) {

	allIDs = make([]string, len(ids))

	// control ID
	for i, id := range ids {
		ctrl := h.getControl(id)
		if ctrl == nil {
			return nil, fmt.Errorf("control with ID '%s' not found", id)
		}

		if at != -1 {
			childIDs := ctrl.GetChildrenIds()
			if at > len(childIDs)-1 {
				return nil, fmt.Errorf("'at' is out of range")
			}

			allIDs[i] = childIDs[at]
			ctrl = h.getControl(allIDs[i])
		} else {
			allIDs[i] = ids[i]
		}

		h.cleanControl(ctrl)
	}

	return allIDs, nil
}

func (h *sessionHandler) remove(cmd *model.Command) (result string, err error) {
	payload, err := h.removeWithMessage(cmd)
	if err != nil {
		return "", err
	}

	// broadcast command to all connected web clients
	h.broadcastCommandToWebClients(NewMessage("", RemoveControlAction, payload))
	return "", nil
}

func (h *sessionHandler) removeWithMessage(cmd *model.Command) (result *RemoveControlPayload, err error) {

	// command format:
	//    remove [id_1] [id_2] ... [at=index]

	at := -1
	if a, err := strconv.Atoi(cmd.Attrs["at"]); err == nil {
		at = a
	}

	ids := make([]string, 0)
	if len(cmd.Values) == 0 && at == -1 {
		return nil, errors.New("'page' control cannot be removed")
	} else if len(cmd.Values) == 0 {
		ids = append(ids, ReservedPageID)
	} else {
		ids = append(ids, cmd.Values...)
	}

	if at != -1 && len(ids) > 1 {
		return nil, errors.New("'at' cannot be specified with a list of IDs")
	}

	allIds, err := h.removeInternal(ids, at)
	if err != nil {
		return nil, err
	}

	// broadcast command to all connected web clients
	return &RemoveControlPayload{
		IDs: allIds,
	}, nil
}

func (h *sessionHandler) removeInternal(ids []string, at int) (allIDs []string, err error) {

	allIDs = make([]string, len(ids))

	// control ID
	for i, id := range ids {
		ctrl := h.getControl(id)
		if ctrl == nil {
			return nil, fmt.Errorf("control with ID '%s' not found", id)
		}

		if at != -1 {
			childIDs := ctrl.GetChildrenIds()
			if at > len(childIDs)-1 {
				return nil, fmt.Errorf("'at' is out of range")
			}

			allIDs[i] = childIDs[at]
			ctrl = h.getControl(allIDs[i])
		} else {
			allIDs[i] = ids[i]
		}

		h.deleteControl(ctrl)
	}

	return allIDs, nil
}

func (h *sessionHandler) sessionCrashed(cmd *model.Command) (result string, err error) {
	errorMessage := sessionCrashedMessage

	// custom error message comes as a first value
	if len(cmd.Values) > 0 && cmd.Values[0] != "" {
		errorMessage = cmd.Values[0]
	}

	// broadcast command to all connected web clients
	h.broadcastCommandToWebClients(NewMessage("", SessionCrashedAction, &SessionCrashedPayload{
		Message: errorMessage,
	}))
	return "", nil
}

func (h *sessionHandler) oauthAuthorize(cmd *model.Command) (result string, err error) {
	var state string

	if len(cmd.Attrs) < 1 {
		return "", fmt.Errorf("oauthLogin command received wrong number of arguments")
	}

	// params
	state = cmd.Attrs["state"]

	// save page_id, session_id in a store
	store.SetOAuthState(state, &model.OAuthState{
		PageID:           h.session.Page.ID,
		SessionID:        h.session.ID,
		CompletePageHtml: cmd.Attrs["completePageHtml"],
		CompletePageUrl:  cmd.Attrs["completePageUrl"],
	}, time.Duration(5)*time.Minute)

	return "", nil
}

func (h *sessionHandler) invokeMethod(cmd *model.Command) (result string, err error) {

	if len(cmd.Values) < 3 {
		return "", fmt.Errorf("invokeMethod command received wrong number of arguments")
	}

	// broadcast command to all connected web clients
	h.broadcastCommandToWebClients(NewMessage("", InvokeMethodAction, &InvokeMethodPayload{
		MethodID:   cmd.Values[0],
		MethodName: cmd.Values[1],
		ControlID:  cmd.Values[2],
		Arguments:  cmd.Attrs,
	}))

	return "", nil
}

func (h *sessionHandler) getUploadUrl(cmd *model.Command) (result string, err error) {

	fileName := cmd.Attrs["file"]
	expires := 0

	expStr := cmd.Attrs["expires"]
	if expires, err = strconv.Atoi(expStr); err != nil {
		return "", fmt.Errorf("cannot convert expires to a number: %s", expStr)
	}

	return GetUploadUrl(fileName, expires), nil
}

func (h *sessionHandler) updateControlProps(props []map[string]string) error {
	sl := h.lockSession()
	defer sl.Unlock()

	for _, p := range props {
		id := p["i"]
		if ctrl := h.getControl(id); ctrl != nil {

			// patch control properties
			for n, v := range p {
				if !model.IsSystemAttr(n) {
					ctrl.SetAttr(n, v)
				}
			}

			err := store.SetSessionControl(h.session, ctrl)
			if err != nil {
				return err
			}
		}
	}
	return nil
}

// nextControlID returns the next auto-generated control ID
func (h *sessionHandler) nextControlID() string {
	return fmt.Sprintf("%s%d", ControlAutoIDPrefix, store.GetSessionNextControlID(h.session))
}

// addControl adds a control to a page
func (h *sessionHandler) addControl(ctrl *model.Control) error {

	existingControl := h.getControl(ctrl.ID())

	if existingControl != nil {
		ctrl.CopyChildren(existingControl)
	}

	err := store.SetSessionControl(h.session, ctrl)
	if err != nil {
		return err
	}

	// find parent
	if existingControl == nil {
		parentID := ctrl.ParentID()
		if parentID != "" {
			parentctrl := h.getControl(parentID)

			if parentctrl == nil {
				return fmt.Errorf("parent control with id '%s' not found", parentID)
			}

			// update parent's childIds
			if at := ctrl.At(); at != -1 {
				parentctrl.InsertChildID(ctrl.ID(), at)
			} else {
				parentctrl.AddChildID(ctrl.ID())
			}
			err = store.SetSessionControl(h.session, parentctrl)
			if err != nil {
				return err
			}
		}
	}

	return nil
}

func (h *sessionHandler) getControlParentIDs(parentID string) []string {
	var result []string
	result = make([]string, 0)
	idParts := strings.Split(parentID, ControlIDSeparator)
	for _, idPart := range idParts {
		if !h.isAutoID(idPart) {
			result = append(result, idPart)
		}
	}
	return result
}

func (h *sessionHandler) cleanControl(ctrl *model.Control) {

	// delete all descendants
	for _, descID := range h.getAllDescendantIds(ctrl) {
		h.deleteSessionControl(descID)
	}

	// clean up children collection
	ctrl.RemoveChildren()
	store.SetSessionControl(h.session, ctrl)
}

func (h *sessionHandler) deleteControl(ctrl *model.Control) {

	// delete all descendants
	for _, descID := range h.getAllDescendantIds(ctrl) {
		h.deleteSessionControl(descID)
	}

	// delete control itself
	h.deleteSessionControl(ctrl.ID())

	// remove control from parent's children collection
	parentCtrl := h.getControl(ctrl.ParentID())
	parentCtrl.RemoveChild(ctrl.ID())
	store.SetSessionControl(h.session, parentCtrl)
}

func (h *sessionHandler) getAllDescendantIds(ctrl *model.Control) []string {
	return h.getAllDescendantIdsRecursively(make([]string, 0), ctrl.ID())
}

func (h *sessionHandler) getAllDescendantIdsRecursively(descendantIds []string, ID string) []string {
	ctrl := h.getControl(ID)
	childrenIds := ctrl.GetChildrenIds()
	result := append(descendantIds, childrenIds...)
	for _, childID := range childrenIds {
		result = append(result, h.getAllDescendantIdsRecursively(make([]string, 0), childID)...)
	}
	return result
}

func (h *sessionHandler) isAutoID(id string) bool {
	return id == ReservedPageID || strings.HasPrefix(id, ControlAutoIDPrefix)
}

func (h *sessionHandler) broadcastCommandToWebClients(msg *Message) {

	serializedMsg, _ := json.Marshal(msg)

	for _, clientID := range store.GetSessionWebClients(h.session.Page.ID, h.session.ID) {
		pubsub.Send(ClientChannelName(clientID), serializedMsg)
	}
}

func (h *sessionHandler) getControl(ctrlID string) *model.Control {
	return store.GetSessionControl(h.session, ctrlID)
}

func (h *sessionHandler) deleteSessionControl(ctrlID string) {
	store.DeleteSessionControl(h.session, ctrlID)
}

func (h *sessionHandler) lockSession() cache.Unlocker {
	return cache.Lock(fmt.Sprintf("session-lock-%s", h.session.ID))
}
