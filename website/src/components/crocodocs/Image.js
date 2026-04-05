import React from "react";
import {useDoc} from "@docusaurus/plugin-content-docs/client";

import {resolveDocAssetUrl} from "./utils";

/**
 * Renders a documentation screenshot figure with optional caption and link wrapper.
 * Resolves relative src paths against the current doc's location.
 *
 * @param {string} src - Image source path (absolute or relative to the doc).
 * @param {string} [alt] - Alt text for the image.
 * @param {string} [width] - CSS width value applied as an inline style.
 * @param {string} [caption] - Optional figcaption text.
 * @param {string} [link] - Optional URL to wrap the image in an anchor tag.
 */
export default function Image({src, alt, width, caption, link}) {
  const {metadata} = useDoc();
  const resolvedSrc = resolveDocAssetUrl(src, metadata?.id);
  const image = (
    <img
      alt={alt ?? ""}
      className="doc-screenshot"
      src={resolvedSrc}
      style={width ? {width} : undefined}
    />
  );
  return (
    <figure className="doc-screenshot-figure">
      {link ? <a href={link}>{image}</a> : image}
      {caption ? <figcaption>{caption}</figcaption> : null}
    </figure>
  );
}
