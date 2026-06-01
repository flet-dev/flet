/**
 * Remark plugin that injects a ### heading before each <CodeExample> element,
 * sourcing the title from examples-metadata.json (built from pyproject.toml files).
 *
 * Relies on the MDX file having an `examples` frontmatter field (e.g.
 * "controls/material/app_bar") and CodeExample path expressions of the form:
 *   path={frontMatter.examples + '/subfolder/main.py'}
 */

const fs = require("fs");
const path = require("path");

const SUBFOLDER_RE = /frontMatter\.examples\s*\+\s*'\/([^/]+)\//;
const LINK_RE = /\[([^\]]+)\]\(([^)]+)\)/g;

function markdownToInlineAst(text) {
  const children = [];
  let lastIndex = 0;
  let match;
  LINK_RE.lastIndex = 0;
  while ((match = LINK_RE.exec(text)) !== null) {
    if (match.index > lastIndex) {
      children.push({ type: "text", value: text.slice(lastIndex, match.index) });
    }
    children.push({ type: "link", url: match[2], children: [{ type: "text", value: match[1] }] });
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < text.length) {
    children.push({ type: "text", value: text.slice(lastIndex) });
  }
  return children;
}

module.exports = function remarkInjectExampleHeadings() {
  const metadataPath = path.join(__dirname, "..", ".crocodocs", "examples-metadata.json");
  let metadata = {};
  if (fs.existsSync(metadataPath)) {
    metadata = JSON.parse(fs.readFileSync(metadataPath, "utf8"));
  }

  return (tree, file) => {
    const examplesPath = file.data?.frontMatter?.examples;
    if (!examplesPath) return;

    const insertions = [];

    for (let i = 0; i < tree.children.length; i++) {
      const node = tree.children[i];
      if (node.type !== "mdxJsxFlowElement" || node.name !== "CodeExample") continue;

      const pathAttr = node.attributes?.find((a) => a.name === "path");
      if (!pathAttr) continue;

      const attrValue = pathAttr.value;
      const exprValue =
        attrValue?.type === "mdxJsxAttributeValueExpression"
          ? attrValue.value
          : typeof attrValue === "string"
          ? attrValue
          : "";

      const match = SUBFOLDER_RE.exec(exprValue);
      if (!match) continue;

      const title = metadata[`${examplesPath}/${match[1]}`]?.title;
      if (!title) continue;

      const description = metadata[`${examplesPath}/${match[1]}`]?.description ?? null;
      insertions.push({ index: i, title, description });
    }

    // Insert in reverse order so earlier indices stay valid
    for (let i = insertions.length - 1; i >= 0; i--) {
      const { index, title, description } = insertions[i];
      const nodes = [
        { type: "heading", depth: 3, children: [{ type: "text", value: title }] },
      ];
      if (description) {
        nodes.push({ type: "paragraph", children: markdownToInlineAst(description) });
      }
      tree.children.splice(index, 0, ...nodes);
    }
  };
};
