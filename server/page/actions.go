package page

const (
	// RegisterWebClientAction registers WS client as web (browser) client
	RegisterWebClientAction = "registerWebClient"

	// RegisterHostClientAction registers WS client as host (script) client
	RegisterHostClientAction = "registerHostClient"

	// SessionCreatedAction notifies host clients about new sessions
	SessionCreatedAction = "sessionCreated"

	// PageCommandFromHostAction adds, sets, gets, disconnects or performs other page-related command from host
	PageCommandFromHostAction = "pageCommandFromHost"

	// PageCommandFromHostAction adds, sets, gets, disconnects or performs other page-related command from host
	PageCommandsBatchFromHostAction = "pageCommandsBatchFromHost"

	// PageEventFromWebAction receives click, change, expand/collapse and other events from browser
	PageEventFromWebAction = "pageEventFromWeb"

	// PageEventToHostAction redirects events from web to host clients
	PageEventToHostAction = "pageEventToHost"

	AddPageControlsAction = "addPageControls"

	ReplacePageControlsAction = "replacePageControls"

	UpdateControlPropsAction = "updateControlProps"

	AppendControlPropsAction = "appendControlProps"

	RemoveControlAction = "removeControl"

	CleanControlAction = "cleanControl"

	PageControlsBatchAction = "pageControlsBatch"

	AppBecomeActiveAction = "appBecomeActive"

	AppBecomeInactiveAction = "appBecomeInactive"

	SessionCrashedAction = "sessionCrashed"

	InvokeMethodAction = "invokeMethod"
)
