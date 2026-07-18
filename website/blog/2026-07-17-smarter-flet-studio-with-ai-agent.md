---
slug: 2026-07-17-smarter-flet-studio-with-ai-agent
title: "Smarter Flet Studio with AI Agent"
authors: feodor
tags: ["releases", "flet studio"]
---

In case you missed it, we have [Flet Studio](https://flet.app) - an online tool for
building Flet apps and sharing them with other users. What started as a quick "FletPad"
experiment has already grown into a solid app - an online Flet IDE, if you will - with
user accounts, a forkable gallery of examples, multiple apps per account, and version
history. You can play with Flet and learn the framework before ever running
`pip install flet` on your machine. Flet Studio itself is written in Flet, with a custom
FastAPI backend, and it's a fantastic opportunity for us to dogfood Flet ourselves.

Our vision is to shape Flet Studio into a hub of online services that help you build
better Flet apps. The first such service was an online editor with the ability to share
your apps with other users.

Today we are introducing a new member of the family - the AI agent!

Go to https://flet.app and ask something like:

<a href="https://flet.app" target="_blank" rel="noopener noreferrer">
  <img src="/img/blog/flet-studio-ai/flet-studio-ai-prompt.png" className="screenshot-100" />
</a>

...and in a few moments you get code you can start working with:

<a href="https://flet.app" target="_blank" rel="noopener noreferrer">
  <img src="/img/blog/flet-studio-ai/flet-studio-ai-result-preview.png" className="screenshot-100" />
</a>

{/* truncate */}

The generated code is not your typical AI slop - it's compact and readable to any
Python developer. Maintainable code is an explicit goal for us, and we are building
tools for the agent to achieve exactly that. It helps that Flet itself, with its minimal
boilerplate, is a framework equally friendly to humans and AI.

<a href="https://flet.app" target="_blank" rel="noopener noreferrer">
  <img src="/img/blog/flet-studio-ai/flet-studio-ai-result-code.png" className="screenshot-100" />
</a>

## Why an AI agent?

* Because it's fun! Every program today has an agent, right? :)
* It helps you start a new project - and once it's off the ground, you can download it
  and continue developing on your computer.
* It's a great way to explore and learn the Flet framework: "How do I do this? How do I
  do that?"
* You can ask it to fix your own app.

We don't see the built-in agent as just a coding agent for your Flet apps - Claude or
Codex would probably do a better job there - but rather as the central "brain" of Flet
Studio, coordinating a bunch of tools and data sources. Over time it will help you with
app deployments, configuring app backends, and troubleshooting errors.

Today's agent is just the beginning of our long AI journey and, bear with us, it can be
dumb sometimes :) Let us know if you see a way to improve its behavior or teach it
something!

## Is it free?

Every account on the new free "Explorer" plan gets **1,000 credits per month for free**.

Frankly, 1,000 credits is not enough to use the agent as your everyday tool, but it's
quite enough to build 3-4 simple apps and get a taste of the framework. We are not
planning to make our profit reselling AI tokens - more interesting value-added services
are in the works - but if you want to play with AI longer, or need more fuel to finish
your app, you are not blocked: you can buy more credits or subscribe to a plan.

There is a "Creator" plan which includes **10,000 AI credits per month**,
"unlimited" app quotas, and **Flet support**! We are still fleshing out what exactly
"Flet support" means, but in essence it's your way to get closer to the Flet team and
move ahead of the line with your feature requests and issues.

## Flet MCP server

We are not going to pretend the Flet agent competes with your favorite local agent -
Claude, Codex, and others are way more powerful, including at developing Flet apps. But
Flet is a fast-growing framework with an evolving API, and most LLMs lag behind with
their training data. Flet 0.86 introduces the "official"
[Flet MCP server](/docs/cookbook/flet-mcp/) with an up-to-date dataset that helps your
agent make smarter decisions when tasked with building a Flet app. In our experiments,
adding the Flet MCP server alone reduces Flet API hallucinations next to zero.

Flet MCP supports stdio and HTTP transports and provides tools organized into groups:

- **API** - look up any Flet control, property, event, or enum as it exists in the
  installed Flet version.
- **Icons** - find the right icon by keyword.
- **Examples** - search and fetch working code examples.
- **CLI** - get help for `flet` CLI commands.

Check the [Flet MCP server cookbook](/docs/cookbook/flet-mcp/) for more details and
examples.

## Flet Skills

Agent Skills are another layer of Flet AI "wisdom". We are going to work on skills in
the coming weeks, so expect the Flet agent to become smarter - today it still struggles
in some areas like routing/navigation or declarative apps.

## Try it

Open [flet.app](https://flet.app), sign in, and ask the agent to build something - your
free monthly credits are already waiting. If you'd rather stay with your local agent,
plug in the [Flet MCP server](/docs/cookbook/flet-mcp/) and enjoy hallucination-free
Flet coding right away.

And tell us how it went: what the agent nailed, where it stumbled, and what you'd like
it to learn next. Drop your feedback in
[GitHub Discussions](https://github.com/flet-dev/flet/discussions) or on
[Discord](https://discord.gg/dzWXP8SHG8) - this is the very beginning of the journey,
and your reports are exactly what will make the agent smarter.

Happy Flet-ing!
