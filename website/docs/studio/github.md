---
title: "GitHub"
---

# GitHub

Keep an app in a GitHub repository. Work on it locally in your own editor, push,
and come back to Studio to run, change and [publish](publishing/index.md) it. Studio
and the repository stay in step both ways:

- **Every change made in Studio is a commit.** Saves in the editor, publishing
  settings, store listings, uploads and each agent turn are committed to the branch
  you chose.
- **A push updates Studio.** When you push to that branch, Studio takes the new
  files within seconds.

Studio connects to repositories that already exist; create the repository on
GitHub first. Each app is connected to one repository, branch and folder.

## Before you start

Studio reaches GitHub through the **Flet Studio** GitHub App:

1. **Connect your GitHub account.** If you signed in to Studio with GitHub, this is
   already done. Otherwise, **Manage › GitHub › Connect GitHub** asks GitHub to
   authorize Studio once.
2. **Install the Flet Studio app** on your account or organization, and choose the
   repositories it may use. **Add an account or organization on GitHub** in
   **Manage › GitHub** opens GitHub's installation page and brings you back.

Studio lists only repositories you can push to yourself. An installation on an
organization doesn't let anyone in Studio use a repository they couldn't push to on
GitHub.

## Connect a repository

Open the app, then **Manage › GitHub**, and choose:

- **Account**: where the Flet Studio app is installed;
- **Repository**;
- **Branch**: the default branch is chosen for you;
- **Folder**: the repository's root, or a folder in it (a monorepo with several
  apps). Folders that hold a Flet app (a `pyproject.toml`) are marked.

Before you connect, Studio says what will happen:

- **The folder has an app.** The repository wins: Studio's files are replaced with
  the folder's. Studio keeps the app's current files as a version first.
- **The folder is empty or doesn't exist yet.** Studio's files become its first
  commit. An empty repository works too.

A folder with files but no `pyproject.toml` can't be connected: choose the app's
folder or an empty one.

### Public and private projects

A public Studio project can only use a public repository. A private project (on
paid plans) can use a public or a private one. If a connected repository is made
private on GitHub, a public project stops syncing until you make it private or
disconnect the repository.

## How changes are committed

Studio commits to the branch as you work. Each commit names what changed:

| Change in Studio | Commit message |
|---|---|
| Saves in the editor | `Edit src/main.py`. Saves a few seconds apart become one commit. |
| An agent turn | What the agent did, e.g. `Add a dark mode toggle to the app bar`, with your request in the message body. A turn is always one commit. |
| Publishing settings | The setting, e.g. `iOS: set App ID to dev.flet.todo` |
| Store listings | `Google Play listing: add Phone screenshots (en-US)` |
| Uploads, renames, deletes | `Add assets/logo.png`, `Rename …`, `Delete …` |

Commits are made under your name. If your GitHub account is connected, your GitHub
no-reply address is used, so they're linked to your GitHub profile.

Studio only adds commits on top of the branch. It never force-pushes or rewrites
history.

## When you push

A push to the connected branch updates Studio: changed files are replaced, new ones
added, deleted ones removed. If the app is open, the editor and preview reload and
Studio says which commit arrived.

**GitHub wins.** If a push arrives while Studio has changes it hasn't committed yet:

- if they're to **other files** than the push's, both are kept: Studio commits its
  changes on top of the push;
- if they're to **the same files**, Studio's changes are replaced by the push, and
  Studio tells you which files.

To avoid surprises, push and then wait a moment before editing the same files in
Studio, or the other way round.

## Versions

For a connected app, the **Versions** pane shows the branch's commits that touch the
app's folder, newest first. The commit Studio's files are at is ticked. Each commit
links to GitHub.

**Restore** makes the app's files what they were at that commit, as a new commit
on the branch. The history stays as it is.

## Publishing

Builds and store uploads use the app's files in Studio, which are the branch's.
A run's details show the commit it built (**Run information › GitHub commit**).

## What isn't synced

- Symbolic links and submodules.
- Files larger than your plan's file size limit.
- Git LFS files: their pointer files are synced, not the files themselves.
- Empty folders: Git doesn't keep them.

Files outside the app's folder are never touched.

## Disconnect

**Manage › GitHub › Disconnect** stops committing and following pushes. The app
keeps its files, and the repository stays as it is.

## Troubleshooting

**Manage › GitHub** shows whether the app is in sync. When Studio can't sync, it says
why. Fix the cause, then use **Sync now**. Common causes:

- **The Flet Studio app was uninstalled**, or the repository was removed from its
  access: install it again or give it the repository on GitHub.
- **The repository was deleted, archived or made private** (for a public project).
- **The branch was deleted**: disconnect, then connect to another branch.

If a push doesn't show up in Studio, **Sync now** looks for it. Studio also looks
whenever you open the app.
