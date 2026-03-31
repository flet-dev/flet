---
title: Gallery
slug: gallery
---

import Card from '@site/src/components/card';

export const GalleryCard = ({title, liveUrl, sourcesUrl, description, imageUrl}) => (
    <Card>
      <a className="gallery-live-link" href={liveUrl}>
        <img src={"/img/gallery/" + imageUrl} className="screenshot-100"/>
        <h2>{title}</h2>
        <div className="gallery-description">{description}</div>
      </a>
      <div className="gallery-footer">
        <a className="gallery-github-link" href={sourcesUrl} title="View source code"></a>
      </div>
    </Card>
);

# Gallery

<div className="margin-top--lg">
  <section className="gallery-grid">
    <GalleryCard
      title="Controls gallery"
      imageUrl="controls-gallery.png"
      description="Interactive showcase app for Flet controls with code samples."
      liveUrl="https://flet-controls-gallery.fly.dev/"
      sourcesUrl="https://github.com/flet-dev/gallery"
      />
    <GalleryCard
      title="To-Do"
      imageUrl="todo.png"
      description="A classic To-Do app inspired by TodoMVC project."
      liveUrl="https://examples.flet.dev/todo/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/todo/todo.py"
      />
    <GalleryCard
      title="Icons browser"
      imageUrl="icons-browser.png"
      description="Quickly search through icons collection to use in your app."
      liveUrl="https://examples.flet.dev/icons_browser/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/icons_browser/main.py"
      />
    <GalleryCard
      title="Calculator"
      imageUrl="calc.png"
      description="A simple calculator app."
      liveUrl="https://examples.flet.dev/calculator/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/tutorials/calculator/calc.py"
      />
    <GalleryCard
      title="Solitaire"
      imageUrl="solitaire.png"
      description="Learn how to handle gestures and position controls on a page."
      liveUrl="https://examples.flet.dev/solitaire/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/tutorials/solitaire_declarative/solitaire-final/main.py"
      />
    <GalleryCard
      title="Chat"
      imageUrl="chat.gif"
      description="Multi-user realtime chat."
      liveUrl="https://flet-chat.fly.dev"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/tutorials/chat/main.py" 
      />
    <!-- <GalleryCard
      title="Trolli"
      imageUrl="trolli.png"
      description="A clone of Trello."
      liveUrl="https://examples.flet.dev/trolli/"
      sourcesUrl="https://github.com/flet-dev/flet/tree/main/sdk/python/examples/apps/trolli" 
      /> -->
    <GalleryCard
      title="Flet animation"
      imageUrl="flet-animation.png"
      description="Implicit animations in Flet."
      liveUrl="https://examples.flet.dev/flet_animation/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/flet_animation/main.py" 
      />
    <GalleryCard
      title="Counter"
      imageUrl="counter.png"
      description="Counter with button click event handlers."
      liveUrl="https://examples.flet.dev/counter/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/counter/counter.py" 
      />
    <GalleryCard
      title="Routing"
      imageUrl="routing.gif"
      description="URL routing between views."
      liveUrl="https://examples.flet.dev/simple_routing/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/routing_navigation/home_store.py" 
      />
    <GalleryCard
      title="Hello, world!"
      imageUrl="hello-world.png"
      description="All examples start with that!"
      liveUrl="https://examples.flet.dev/hello_world/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/hello_world/hello.py" 
      />
    <GalleryCard
      title="Greeter"
      imageUrl="greeter.png"
      description="Interactive form in Flet."
      liveUrl="https://examples.flet.dev/greeter/"
      sourcesUrl="https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/greeter/greeter.py" 
      />
    <GalleryCard
      title="Emoji Enigma"
      imageUrl="emoji-enigma.png"
      description="Guess 20 words using the emote icons as clues"
      liveUrl="https://ee.lshss.app/"
      sourcesUrl="https://github.com/vihutuo/emoji_riddles" 
      />

    <GalleryCard
      title="Seven Spell"
      imageUrl="seven-spell.png"
      description="Create as many 3+ letter words as you can using the same letters given to all users"
      liveUrl="https://ss.lshss.app/"
      sourcesUrl="https://github.com/vihutuo/seven_spell" 
      />

  </section>
</div>