# Flet-Color-Browser

![GitHub top language](https://img.shields.io/github/languages/top/ndonkoHenri/Flet-Color-Browser)
![GitHub language count](https://img.shields.io/github/languages/count/ndonkoHenri/Flet-Color-Browser)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/ndonkoHenri/Flet-Color-Browser?color=ry)


> _From my experience, working with colors is not that easy._

## Table of contents:
- [Introduction](#what-is-this-about-introduction)
- [Source of Inspiration](#source-of-inspiration)
- [Screen captures](#screen-captures)
- [How to get started?](#how-to-get-started)
- [How to deploy to Fly.io?](#how-to-deploy-to-flyio)
- [Issues/Contribution](#issuescontribution)

_**Original Repo's URL:**_ [ndonkoHenri/Flet-Color-Browser](https://github.com/ndonkoHenri/Flet-Color-Browser)

### What is this about? (Introduction)

 A simple but sophisticated tool(Web and desktop UI) for easy color selection when developing [Flet](https://flet.dev/) applications.
Here is a link to the online/web version of this tool -> <u>[flet-colors-browser.fly.dev](https://flet-colors-browser.fly.dev/)</u>

### Source of Inspiration

I decided to build up this tool after looking at the [Flet-Icons-Browser](https://github.com/flet-dev/examples/tree/main/python/apps/icons-browser) - a simple browser which eases Icon selection when developing Flet apps .
This tool is actually a refactored-clone(or fork if you want) of it.
I just added my personal UI touch and included more comments in the code :)

### Screen captures

Below are some captures I made of the tool in execution.

- _**On PC:**_
  - _Dark Mode_
        <br><br>
      ![pc_dark](https://user-images.githubusercontent.com/98978078/191587712-3c8fb14d-8ed0-4045-ab97-7759be04791c.png)
        <br><br>
  - _Light Mode_
        <br><br>
      ![pc_light](https://user-images.githubusercontent.com/98978078/191587748-11d44ba2-03f1-4bbc-9abd-233ad8ff3c50.png)

- _**In a web browser:**_
  - _Dark Mode_
       <br><br>
      ![web_dark](https://user-images.githubusercontent.com/98978078/191587793-68c9f173-d8f9-497a-8bd0-8c88ebf3045d.png)

       <br><br>
  - _Light Mode_
       <br><br>
      ![web_light](https://user-images.githubusercontent.com/98978078/191587819-4d4b0770-7f2f-460c-83d3-5c6a518fcac4.png)
    <br><br>
  - **Video**
        <br><br>
              [Link to video-demo](https://user-images.githubusercontent.com/98978078/191587444-d66a4185-c677-441c-a747-ce6f6f58774e.mp4)

### How to get started?

**Easiest:** You can just download an archive(for Windows, MacOS and Linux only) from the [releases](https://github.com/ndonkoHenri/Flet-Color-Browser/releases) section, extract this and run the standalone executable file(~25Mo) found in it.

**Hardest:**

- Start by cloning and unzipping this repo: [how-to](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- Enter the directory

        cd Flet-Color-Browser
- Install the requirements(only Flet is required):
    `pip install flet`
- Run the `main.py` file

      python main.py

### How to deploy to Fly.io?

A detailed version of how to deploy [Flet](https://github.com/flet-dev/flet) apps on [Fly.io](https://fly.io/) could be found <u>[here](https://flet.dev/docs/guides/python/deploying-web-app/fly-io)</u>.

Deploy:

    flyctl deploy

Check deployment:

    flyctl status

Re-deploy:

    flyctl deploy --no-cache


### Issues/Contribution
I tried my best to make this project simple and easy to understand, but if you have problems/issues while using this :(,
then you are free to raise an issue and I will happily respond.

If you instead want to contribute(new features, bug/typo fixes, etc), just fork this project and make a pull request. :)
