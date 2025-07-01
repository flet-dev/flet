---
title: Buttons
sidebar_label: Buttons
---

import Card from '@site/src/components/card';

export const ImageCard = ({title, href, imageUrl}) => (
    <div className="col col--4 margin-bottom--lg">
      <Card href={href}>
        <img src={"/img/docs/controls/button/" + imageUrl}/>
        <h2>{title}</h2>
      </Card>
    </div>
);

[Live example](https://flet-controls-gallery.fly.dev/buttons)

<div className="margin-top--lg">
  <section className="row">
    <ImageCard title="Cupertino" href="/docs/controls/cupertinobutton" imageUrl="cupertino-button.png" />
    <ImageCard title="CupertinoFilled" href="/docs/controls/cupertinofilledbutton" imageUrl="cupertino-filled-button.png" />
    <ImageCard title="Elevated" href="/docs/controls/elevatedbutton" imageUrl="elevated-button.png" />
    <ImageCard title="Filled" href="/docs/controls/filledbutton" imageUrl="filled-button.png" />
    <ImageCard title="Filled Tonal" href="/docs/controls/filledtonalbutton" imageUrl="filled-tonal-button.png" />
    <ImageCard title="Floating Action" href="/docs/controls/floatingactionbutton" imageUrl="floating-action-button.png" />
    <ImageCard title="Icon Button" href="/docs/controls/iconbutton" imageUrl="icon-button.png" />
    <ImageCard title="Outlined" href="/docs/controls/outlinedbutton" imageUrl="outlined-button.png" />
    <ImageCard title="Popup Menu" href="/docs/controls/popupmenubutton" imageUrl="popup-menu.gif" />
    <ImageCard title="Text Button" href="/docs/controls/textbutton" imageUrl="text-button.png" />
  </section>
</div>