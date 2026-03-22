import React from "react";
import {useDoc} from "@docusaurus/plugin-content-docs/client";

import {resolveDocAssetUrl} from "./utils";

export default function Image({src, alt, width, caption, link}) {
  const {metadata} = useDoc();
  const resolvedSrc = resolveDocAssetUrl(src, metadata?.id);
  const image = <img alt={alt ?? ""} src={resolvedSrc} style={width ? {width} : undefined} />;
  return (
    <figure>
      {link ? <a href={link}>{image}</a> : image}
      {caption ? <figcaption>{caption}</figcaption> : null}
    </figure>
  );
}
