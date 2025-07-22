# ResponsiveMenuLayout

ResponsiveMenuLayout creates a left panel menu using NavigationRail. It's main feature is that it
reacts to window size changes, and typically hides the menu when in portrait orientation (usually
a phone).

The AppBar in this demo app is not a part of the ResponsiveMenuLayout component. Here the main
menu button is used to toggle menu visibility, but you can have other toggles, maybe swiping once
we have gesture support in flet.

You can `from responsive_menu_layout import ResponsiveMenuLayout` to use it as a component in your
own code, or run the file to see the demo.

## Features

**Basic landscape layout, menu shown by default**

<img width="678" alt="image" src="https://user-images.githubusercontent.com/5179247/182687976-2d13639e-bf67-42de-b8ce-6886415c8730.png">

**Landscape layout, menu thinner**

This is a parameter and a toggle in the demo app.

<img width="681" alt="image" src="https://user-images.githubusercontent.com/5179247/182690795-24dac5e1-67c2-49bb-ad51-b66500f8eef3.png">

**Landscape layout, menu hidden (completely by default)**

<img width="669" alt="image" src="https://user-images.githubusercontent.com/5179247/182688450-1171017d-9724-4c88-903f-b202e6b511a2.png">

**Landscape layout, menu shown as icons only instead of hidden**

This is a parameter of ResponsiveMenu, and a toggle in the demo app.

<img width="684" alt="image" src="https://user-images.githubusercontent.com/5179247/182690945-31b575c2-6963-4d6a-8c1e-2113bff3161b.png">

**Basic portrait layout, menu hidden by default**

<img width="361" alt="image" src="https://user-images.githubusercontent.com/5179247/182688981-7a70dfa3-8801-426b-971a-f51439d44eaf.png">

**Portrait layout, menu when shown is on top of the main content**

Menu can be dismissed also by clicking outside the menu panel.

<img width="359" alt="image" src="https://user-images.githubusercontent.com/5179247/182689617-bb9dab68-ab1e-4e38-81d1-9cad96177e3d.png">

**Portrait layout, menu can also be minimized to icons instead of being hidden**

With the `minimize_to_icons` parameter, controlled by a toggle in the demo app. Minimizing behavior can also be controlled separately in each orientation by the `landscape_minimize_to_icons` and `portrait_minimize_to_icons` parameters.

<img width="359" alt="image" src="https://user-images.githubusercontent.com/5179247/182690086-676c0084-e8f2-4824-a0a6-f69ac7dba607.png">

**Route support**

Routes are supported by default in the web (selected page slug is part of the url, page can be opened directly with the right url).

<img width="675" alt="image" src="https://user-images.githubusercontent.com/5179247/182772040-2180dabb-c36d-4d63-8448-aebae8199300.png">

**Fine-tuning the NavigationRail**

NavigationRail can be accessed to make changes directly, although there are some parameters that should be avoided.

<img width="673" alt="image" src="https://user-images.githubusercontent.com/5179247/183242879-2ec3f7f7-b716-43d8-9d3f-788c3988b203.png">
