[Replit](https://replit.com/) is an online IDE and hosting platform for web apps written in any language. Their free tier allows running any number of apps with some performance limitations.

To run your app on Replit:

* [Sign up](https://replit.com/signup?from=landing) on Replit.
* Click "New Repl" button, select "Python" template and type the name of your repl, e.g. `my-flet-app`. Alternatively, go to [Flet template](https://replit.com/@fletdev/Flet?v=1) page and click **Use Template** button. Flet template has everything configured for you, so you can jump to `main.py` and update your program right away.

* Open `.replit` file on the left and add these two options to the root:

```toml
# Stops the packager from installing packages when running the Repl
disableInstallBeforeRun = true
# Stops the packager from guessing and auto-installing packages, but it still runs to install packages when running the Repl
disableGuessImports = true
```

  <img src="/img/docs/hosting-replit/replit-disable-guess-imports.png" className="screenshot-60 screenshot-rounded"/>

* On "Tools" pane click "Dependencies" and search for `flet` package and click "Install" button.
* Open `main.py` on "Files" pane and copy-paste your app.
* Modify call to `ft.run()` and include `view=ft.AppView.WEB_BROWSER` parameter:

```python
ft.run(main, view=ft.AppView.WEB_BROWSER)
```

* Run the app. Enjoy.

  <img src="/img/docs/hosting-replit/replit-running-app.png" className="screenshot-100"/>
