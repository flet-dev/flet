import React from "react";
import CodeBlock from "@theme/CodeBlock";

import {getExampleSource} from "./utils";

export default function CodeExample({path, language = "python", title}) {
  const source = getExampleSource(path);

  if (source == null) {
    return <div>Missing code example for <code>{path}</code>.</div>;
  }

  return (
    <CodeBlock language={language} title={title}>
      {source}
    </CodeBlock>
  );
}
