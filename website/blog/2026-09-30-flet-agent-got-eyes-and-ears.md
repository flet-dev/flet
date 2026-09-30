---
slug: flet-agent-got-eyes-and-ears
title: Flet agent got eyes and ears
authors: feodor
tags: [ai]
toc_max_heading_level: 2
---

It's exciting to build agent
It's even more exciting to see people use it and can achieve desired results
It's even more exciting to see early adopters going beyond free plan and subscribing to Creator plan. Thank you for your support!

## AI agent basics

You can probably find ifinite number of articles about "what AI agent is" or "how to build your own agent", but I'd like to quickly recap it here and establish terminology (so we speak the same language), so we can refer to this later in various places of Flet docs.

In short, the agent is a loop with LLM (or simply "model") in the middle + prompts, skills, MCPs and tools.

[agent diagram]

You through a prompt and a new "turn" starts. The prompt is sent to an LLM ...

[turn diagram]

Send another prompt and all previews turns (all your prompts, model tool calls and output) are being sent as well.

The sum of all turns is "conversation" or "context" which is usually named on Agent UI as "chat".

[conversation diagram]

How long this conversation could be is determined by a maximum model context window size.

## The problem

Developing agent is a challenge. LLM is non-deterministic, so if you ask it 10 times to "build a counter app" it will give you different, but plausible, result every time. Prompts and skills give agent new knowledge as well as put some constraints on its "creativity" (read hallucinations), hence the term "harness".

The first iteration of Flet Agent had only tools for manipulating files in a virtual app workspace, so it could create, list directories and files, read and write their contents. The information flow was in one direction: from LLM to an app workspace.

OK, let's give an Agent a brain (model) and a pen (workspace tools) and see what happens!

You: "build a counter app with plus and minus buttons"
Agent (after calling some tools to check Flet API, thinking a minute and writing `main.py`): "here, I built a simple counter app with plus and minus buttons."

You: "there is no minus button"
Agent (read a bunch tools to check Flet API, thought a few seconds, updated `main.py`): "I added a missing minus button."

You: "there is a Python error of missing import"
Agent: (changed `main.py`)": "My apologies, I put incorrect import and now it's fixed."

You: "OK. Now, put app content at the center of the page"
Agent (thought and changed `main.py`): "I centered app content on the page."

You: "it's not at the center"
Agent (changed `main.py`): "I fixed the app and now it's centered."

You: "it's **still** not at the center!"
Agent (more thought, changed `main.py` again): "I restructured the app to make sure it's content is at the center of the page."

You: "it's not centered, again!!!"
Agent: "Could you give me a screenshot of what you see to help me figure out the solution".

You: "I can't give you a screenshot!!!"
...
(user left the chat)

Dialogs like this could go on for hours.
If you are persistent you can probably finish the job in a dozen of turns.
But it's still really annoying, right?

For an agent trying to build UI with only file manipulation tools and inability to "see" the result is the biggest gap/issue. The only way to get feedback is rely on you describing what *you* see, in text.

Or another one: "I added some prints into the code, run the app, click here and there and paste me the contents of Console" which is, OK, doable, but it's unnecessary friction for the user. See, human is still constantly necessary in the loop.

## Feedback is the key

Today's release of Flet Studio gives users an ability to attach files (pictures, PDFs, plain text and code) or paste clipboard image to a chat. So, now you can tell agent: "hey, I want you to develop form like on the attached picture" or "this button doesn't look like I described - see attached".

Flet agent itself receives three new capabilities (tools) and goes to the next level of effectiveness:
* Run the app
* Take app screenshot
* Read console output

Scenario 1:

Example loops:

...
