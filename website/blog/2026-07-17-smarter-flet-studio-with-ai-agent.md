---
slug: 2026-07-17-smarter-flet-studio-with-ai-agent
title: "Smarter Flet Studio with AI Agent"
authors: feodor
tags: ["releases", "flet studio"]
---

For those who didn't know we have [Flet Studio](https://flet.app) - an online tool for building Flet apps and sharing them with other users.
Started as a quick "FletPad" experiment it grown already into a solid app, online Flet IDE if you will, with user registrations, forkable gallery of examples,
multiple apps per account and versions history. You can play with Flet before `pip install flet` on your machine and spend time learning the framework.
Flet Studio itself is written in Flet with a custom FastAPI backend and it's a fantastic opportunity for us to "dog food" Flet to ourselves.

We have an vision to shape Flet Studio to a hub of online services that help you build better Flet apps.
The first service was an online editor for your apps with an ability to share them with other users.

Today, we are introducing the new member of service family - AI agent!

Go to https://flet.app and ask something like:

<a href="https://flet.app" target="_blank" rel="noopener noreferrer">
  <img src="/img/blog/flet-studio-ai/flet-studio-ai-prompt.png" className="screenshot-100" />
</a>

...and in a few moments you get the code you can start working with:

<a href="https://flet.app" target="_blank" rel="noopener noreferrer">
  <img src="/img/blog/flet-studio-ai/flet-studio-ai-results.png" className="screenshot-100" />
</a>

## Why?

* Because it's fun! Every program today has an Agent, right? :)
* It can help you to start a new project. Then you can download it and continue developing on your computer.
* You can use it to explore and learn Flet framework. How do I do this? How do I do that?
* You can ask Flet agent to fix your own app.

We don't see built-in AI agent as just a coding agent for your Flet apps - Claude or Codex will probably do a better job - but we see it more as
a central "brain" of Flet Studio IDE, coordinating a bunch tools and data sources. It will be helping you with app deployments, configuring app backends, troubleshooting errors.

Today's agent is just a beginning of our long AI journey and, bear with us, it can be dumb sometimes :)
Let us know if you see the way to improve its behavior or teach it something!

## Is it free?

We give **1,000 "credits" per month for free** to all accounts on a new free "Explorer" plan.

Frankly, 1,000 credits is not a lot to use Flet agent as your day-long tool, but quite enough to build 3-4 simple apps, to have a taste of Flet framework.
We are not going to make our profits on selling you AI tokens - we are preparing more interesting value-added services,
but if you need to "play" with AI longer or need more fuel to finish your app you are not blocked and have the ability to **buy more credits** or **subscribe to a plan**.

There is "Creator" plan which includes **10,000 AI credits per month** with "unlimited" app quotas and **Flet support**!
We are still fleshing out the definition of "Flet support", but in essence it's your way to get closer to Flet team and move ahead of the line with your feature requests or issues.

## Flet MCP server

We are not going to pretend Flet agent could compete with your favorite local agent. Claude, Codex and others are way more powerful, including developing apps in Flet.
Flet is a fast growing framework with evolving API and most LLMs sit behind with their training set.
Flet 0.86 introduces "official" [Flet MCP server](/docs/cookbook/flet-mcp/) with up-to-date dataset which helps your agent making smarter decisions when tasked to build a Flet app.
Based on our experiments adding Flet MCP server to your agent along reduces Flet API hallucinations to zero.

Flet MCP supports stdio and HTTP transports and provides the following tools:
- API
- Examples
- CLI

Check [Flet MCP server cookbook](/docs/cookbook/flet-mcp/) for more details and examples.

## Flet Skills

Agent Skills is another layer of Flet AI "wisdom". We are going to work on AI skills in the coming weeks, so expect Flet Agent become smarter - it's still struggling in some
areas like routing/navigation or declarative apps.

Once ready we are going to share Flet skills as installable bundle for your favorite agent.

## Conclusion

...
