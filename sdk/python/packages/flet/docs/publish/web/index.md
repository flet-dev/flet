---
title: Publishing Flet app to web
---

Flet allows publishing your app as a **static** or **dynamic** website.

**[Static website]** - content is not changing and delivered exactly as it's stored. Python code is running in the web browser.

**[Dynamic website]** - content is dynamically generated for each user. Python code is running on the server.

Here is a table comparing Flet app running as a static vs dynamic website:

|                          | [Static website]                                                                                                                                                           | [Dynamic website]                                                                                                          |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| **Loading time**         | ⬇️ Slower - Python runtime (Pyodide) along with app's Python code and all its dependencies must be loaded into the browser. Pyodide initialization takes time too.         | ✅ Faster - the app stays and runs on the server.                                                                           |
| **Python compatibility** | ⬇️ Not every program that works with native Python [can be run with Pyodide](https://pyodide.org/en/stable/usage/wasm-constraints.html)                                    | ✅ Any Python package can be used.                                                                                          |
| **Responsiveness**       | ✅ Zero latency between user-generated events (clicks, text field changes, drags) and page updates.                                                                         | ⬇️ Non-zero latency - user-generated events are communicated to a server via WebSockets. UI updates are communicated back. |
| **Performance**          | ⬇️ Slower - Pyodide is currently 3x-5x slower than native Python because of WASM                                                                                           | ✅ Faster - the code is running on the server by native Python.                                                             | 
| **Code protection**      | ⬇️ Low - app's code is loaded into a web browser and can be inspected by a user.                                                                                           | ✅ High - the app is running on the server.                                                                                 |
| **Hosting**              | ✅ Cheap/Free - no code is running on the server and thus the app can be hosted anywhere: GitHub Pages, Cloudflare Pages, Replit, Vercel, a shared hosting or your own VPS. | ⬇️ Paid - the app requires Python code to run on the server and communicate with a web browser via WebSockets.             |


[Static website]: static-website/index.md
[Dynamic website]: dynamic-website/index.md