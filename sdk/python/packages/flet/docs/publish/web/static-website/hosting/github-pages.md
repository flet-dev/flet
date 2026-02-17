---
title: Hosting Flet website on GitHub Pages
---

This guide shows how to build a Flet static web app and deploy it to [GitHub Pages](https://pages.github.com/) with GitHub Actions.

## Create workflow file

1. Open your repository root.
2. Create this folder if it does not exist: `.github/workflows/`
3. Create a workflow file, for example: `.github/workflows/github-pages.yml`
4. Paste the workflow below.
5. Commit and push to GitHub.
6. Open the **Actions** tab to monitor build/deploy progress.

/// admonition | Repository settings
    type: tip
In GitHub, open **Settings** -> **Pages** and make sure deployment source is **GitHub Actions**.
///

{% raw %}
```yaml
name: Web Build + Deploy to GitHub Pages # (1)!

on: # (2)!
  push: # (3)!
  pull_request: # (4)!
  workflow_dispatch: # (5)!

concurrency: # (6)!
  group: "pages" # (7)!
  cancel-in-progress: false # (8)!

env: # (9)!
  UV_PYTHON: 3.12 # (10)!

  # https://docs.flet.dev/reference/environment-variables
  FLET_CLI_NO_RICH_OUTPUT: 1 # (11)!

jobs:
  build:
    name: Build web app
    runs-on: ubuntu-latest # (12)!

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4 # (13)!

      - name: Setup uv
        uses: astral-sh/setup-uv@v6 # (14)!

      - name: Build app
        shell: bash
        run: |
          uv run flet build web --yes --verbose --base-url ${GITHUB_REPOSITORY#*/} --route-url-strategy hash # (15)!

      - name: Upload Pages Artifact
        uses: actions/upload-pages-artifact@v4.0.0 # (16)!
        with:
          path: build/web # (17)!
          name: web-build-artifact # (18)!
          retention-days: 20 # (19)!

  deploy:
    name: Deploy to GitHub Pages
    if: github.event_name == 'push' && github.ref == 'refs/heads/main' # (20)!
    needs: build # (21)!
    runs-on: ubuntu-latest

    permissions: # (22)!
      pages: write
      id-token: write

    environment: # (23)!
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - name: Setup Pages
        uses: actions/configure-pages@v5 # (24)!

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4.0.5 # (25)!
        with:
          artifact_name: web-build-artifact # (26)!
```
{% endraw %}

1. Workflow name shown in the Actions list.
2. Trigger block for the workflow.
3. Builds on every push.
4. Builds on pull request updates.
5. Allows manual runs from the Actions tab.
6. Concurrency settings for GitHub Pages deployments.
7. Places deployments into the same `pages` concurrency group.
8. Keeps the currently running deployment instead of canceling it.
9. Environment variables available to all jobs.
10. Python version used by `uv`.
11. Produces cleaner CI logs by disabling rich output.
12. Runs the build job on GitHub-hosted Ubuntu.
13. Checks out repository code.
14. Installs `uv`.
15. Builds static web output and sets:
    - `--base-url ${GITHUB_REPOSITORY#*/}` so project pages deploy under `/<repo>/`.
    - `--route-url-strategy hash` so routing works on static hosting without server-side rewrites.
16. Uploads static files as a Pages artifact.
17. Uses `build/web` as artifact source.
18. Artifact name used later by deploy step.
19. Keeps the artifact for 20 days.
20. Deploys only on pushes to `main` (PRs only build).
21. Waits for successful build job before deploy.
22. Required permissions for Pages deployment.
23. Connects deployment output URL to the GitHub environment.
24. Configures Pages runtime.
25. Deploys artifact to GitHub Pages.
26. Must match the uploaded artifact name.

/// admonition | If your default branch is not `main`
Update the deploy condition:
```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/<your-branch>'
```
///

/// admonition | User/Org Pages repositories
    type: note
If your repository is `<username>.github.io`, use `--base-url /` instead of repository name.
///
