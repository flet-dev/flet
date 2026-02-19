flet --version
DIST_PATH=$PWD/dist
flet publish apps/todo/todo.py --distpath $DIST_PATH/todo --base-url todo --app-name "Flet To-Do" --app-description "A classic To-Do app inspired by TodoMVC project."
flet publish apps/icons_browser/main.py --distpath $DIST_PATH/icons_browser --base-url icons_browser --app-name "Flet Icons Browser" --app-description "Quickly search through icons collection to use in your app."
flet publish tutorials/calculator/calc.py --distpath $DIST_PATH/calculator --base-url calculator --app-name "Calculator" --app-description "A simple calculator app written in Flet."
flet publish tutorials/solitaire_declarative/solitaire-final/main.py --distpath $DIST_PATH/solitaire --base-url solitaire --assets assets --app-name "Solitaire" --app-description "Learn how to handle gestures and position controls on a page."
#flet publish apps/trolli/src/main.py --distpath $DIST_PATH/trolli --base-url trolli --assets ../assets --route-url-strategy "hash" --app-name "Trolli" --app-description "A clone of Trello."
flet publish apps/routing_navigation/home_store.py --distpath $DIST_PATH/simple_routing --base-url simple_routing --route-url-strategy "hash" --app-name "Flet routing example" --app-description "An example of routing in Flet."
flet publish apps/counter/counter.py --distpath $DIST_PATH/counter --base-url counter --app-name "Counter" --app-description "Counter to get an idea of Flet."
flet publish apps/flet_animation/main.py --distpath $DIST_PATH/flet_animation --base-url flet_animation --app-name "Flet animation" --app-description "An example of implicit animations in Flet."
flet publish apps/greeter/greeter.py --distpath $DIST_PATH/greeter --base-url greeter --app-name "Greeter" --app-description "A basic example of interactive forms in Flet."
flet publish apps/hello_world/hello.py --distpath $DIST_PATH/hello_world --base-url hello_world --app-name "Hello, world!" --app-description "A very minimal example of Flet app."
