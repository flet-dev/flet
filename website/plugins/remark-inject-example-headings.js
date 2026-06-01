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

      insertions.push({ index: i, title });
    }

    // Insert in reverse order so earlier indices stay valid
    for (let i = insertions.length - 1; i >= 0; i--) {
      const { index, title } = insertions[i];
      tree.children.splice(index, 0, {
        type: "heading",
        depth: 3,
        children: [{ type: "text", value: title }],
      });
    }
  };
};
