---
title: "Web apps"
---

# Web apps

Open **Publish › Web**. Its card, **Create web app**, builds the app as a website:
static files that run your Python app in the visitor's browser, with no server of
your own needed to run it.

When the run finishes, **Download** the `.zip`. **Update** builds the app as it is
now. The web settings (base URL, routing, the installed app's colors, …) are on the
**Settings** tab.

{/* SCREENSHOT: /img/docs/studio/publishing/web-card.png — Publish › Web with the built app */}

## Host the app

The `.zip` holds a folder of static files with `index.html` at the top. Any web server
or static host can serve it:

1. Unzip the download.
2. Upload the folder's **contents** to your host: for example GitHub Pages, Netlify,
   Cloudflare Pages, an S3 bucket, or your own nginx or Apache.
3. Open the site's address. It has to be served over `http://` or `https://`:
   opening `index.html` from your disk doesn't work.

To try it on your computer first, serve the folder locally, e.g.
`python -m http.server --directory <folder>` and open `http://localhost:8000`.

### Hosting in a subfolder

If the app isn't at the root of its site (e.g. `https://example.com/my-app/`), set
**Base URL** to that path (`/my-app/`) in **Publish › Web › Settings** and
**Update** the app.

### Page addresses

With **Route URL strategy** set to `path` (the default), the app's pages have clean
addresses like `/settings`. The host then has to send every address to `index.html`:
on most static hosts that's a "single-page app" or "fallback to index.html" option.
If your host can't do that, set **Route URL strategy** to `hash`: addresses become
`/#/settings` and need nothing from the host.

## Questions

### Is it the same as the preview?

Yes: both run your app in the browser with [Pyodide](https://pyodide.org), so the
packages that work in the preview work here too.

### Can Studio host it for me?

Not yet.
