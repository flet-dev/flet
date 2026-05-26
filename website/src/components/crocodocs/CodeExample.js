import React from "react";
import CodeBlock from "@theme/CodeBlock";

import {getExampleSource, getExampleWebSupported} from "./utils";

const FLET_STUDIO_BASE = "https://flet.app/gallery/example";

/**
 * Renders a syntax-highlighted code block for a bundled example file.
 * When the example supports the web platform, also renders a "Try Online" button
 * above the code that opens the example in Flet Studio.
 * Shows an error message if the example path is not found in the code-examples bundle.
 *
 * @param {string} path - Relative path to the example file within the examples root.
 * @param {string} [language="python"] - Language identifier for syntax highlighting.
 * @param {string} [title] - Optional title displayed above the code block.
 */
export default function CodeExample({path, language = "python", title}) {
  const source = getExampleSource(path);

  if (source == null) {
    return <div>Missing code example for <code>{path}</code>.</div>;
  }

  const exampleDir = path.includes("/") ? path.slice(0, path.lastIndexOf("/")) : path;
  const showTryOnline = getExampleWebSupported(exampleDir);
  const studioUrl = `${FLET_STUDIO_BASE}/${exampleDir}`;

  return (
    <div className="code-example">
      {showTryOnline && (
        <a
          className="code-example-try-online"
          href={studioUrl}
          target="_blank"
          rel="noopener noreferrer"
        >
          <span className="material-symbols-outlined">play_arrow</span>
          Try Online
        </a>
      )}
      <CodeBlock language={language} title={title}>
        {source}
      </CodeBlock>
    </div>
  );
}
