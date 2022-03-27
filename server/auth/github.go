package auth

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"

	"github.com/flet-dev/flet/server/config"
	"github.com/google/go-github/github"
	log "github.com/sirupsen/logrus"
)

func (p *SecurityPrincipal) updateFromGitHub() error {

	// retrieve token
	token, err := p.GetToken()
	if err != nil {
		return err
	}

	if token == nil {
		return errors.New("GitHub OAuth token is not set")
	}

	// GitHub client
	oauthConfig := GetOauthConfig(p.AuthProvider, p.Groups != nil)
	client := github.NewClient(oauthConfig.Client(context.Background(), token))

	// read user details
	githubUser, _, err := client.Users.Get(context.Background(), "")
	if err != nil {
		return err
	}

	p.ID = strconv.FormatInt(githubUser.GetID(), 10)
	p.Login = githubUser.GetLogin()
	p.Name = githubUser.GetName()

	// read user emails
	listEmailOpts := &github.ListOptions{
		PerPage: 10,
	}
	for {
		emails, resp, err := client.Users.ListEmails(context.Background(), listEmailOpts)
		if err != nil {
			return err
		}

		for _, email := range emails {
			if *email.Primary {
				p.Email = *email.Email
				break
			}
		}

		if p.Email != "" {
			break
		}

		if resp.NextPage == 0 {
			break
		}
		listEmailOpts.Page = resp.NextPage
	}

	// read user teams
	if p.Groups != nil {
		p.Groups = make([]string, 0)

		listTeamsOpts := &github.ListOptions{
			PerPage: 10,
		}
		for {
			teams, resp, err := client.Teams.ListUserTeams(context.Background(), listTeamsOpts)
			if err != nil {
				return err
			}

			for _, team := range teams {
				p.Groups = append(p.Groups, fmt.Sprintf("%s/%s", *team.Organization.Login, team.GetName()))
			}

			if resp.NextPage == 0 {
				break
			}
			listTeamsOpts.Page = resp.NextPage
		}
	}
	return nil
}

func (p *SecurityPrincipal) signoutGitHub() error {

	token, err := p.GetToken()
	if err != nil {
		return err
	}
	if token == nil {
		return nil
	}

	// https://docs.github.com/en/rest/reference/apps#delete-an-app-token
	client := &http.Client{}

	postBody, _ := json.Marshal(map[string]string{
		"client_id":    config.GithubClientID(),
		"access_token": token.AccessToken,
	})
	requestBody := bytes.NewBuffer(postBody)

	req, err := http.NewRequest("DELETE", fmt.Sprintf("https://api.github.com/applications/%s/token", config.GithubClientID()), requestBody)
	req.Header.Add("accept", "application/vnd.github.v3+json")
	if err != nil {
		return err
	}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)

	log.Debugln("signoutGitHub:", string(body))
	return nil
}
