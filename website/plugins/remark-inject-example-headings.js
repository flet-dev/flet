/**
 * Remark plugin that injects a ### heading (and optional description) before
 * each <CodeExample> element, sourcing content from examples-metadata.json
 * (built from [tool.flet.metadata] in pyproject.toml files).
 *
 * Relies on the MDX file having an `examples` frontmatter field (e.g.
 * "controls/material/app_bar") and CodeExample path expressions of one of:
 *   path={frontMatter.examples + '/subfolder/main.py'}   ← relative to frontmatter
 *   path={'controls/material/some_group/subfolder/main.py'}  ← absolute hardcoded
 *
 * Set `display_title = false` in [tool.flet.metadata] to suppress injection
 * for a specific example (use when the doc page has a hand-written heading).
 */

const fs = require("fs");
const path = require("path");

// Matches: frontMatter.examples + '/subfolder/...', captures subfolder name.
const SUBFOLDER_RE = /frontMatter\.examples\s*\+\s*'\/([^/]+)\//;
// Matches: 'controls/.../subfolder/file.py', captures the directory path.
const HARDCODED_PATH_RE = /^'(controls\/.+)\/[^/']+\.py'$/;

// Matches [text](url) or [`code`](url) or `code`
const INLINE_RE = /\[(`[^`]+`|[^\]]*)\]\(([^)]+)\)|`([^`]+)`/g;

// Parse a single line of inline markdown into AST children.
// Handles: [text](url), [`code`](url), `code`, plain text.
function parseInline(text) {
  const nodes = [];
  let lastIndex = 0;
  let match;
  INLINE_RE.lastIndex = 0;
  while ((match = INLINE_RE.exec(text)) !== null) {
    if (match.index > lastIndex) {
      nodes.push({ type: "text", value: text.slice(lastIndex, match.index) });
    }
    if (match[1] !== undefined) {
      // Link: [text](url) or [`code`](url)
      const linkText = match[1];
      const url = match[2];
      const child =
        linkText.startsWith("`") && linkText.endsWith("`")
          ? { type: "inlineCode", value: linkText.slice(1, -1) }
          : { type: "text", value: linkText };
      nodes.push({ type: "link", url, children: [child] });
    } else {
      // Inline code: `code`
      nodes.push({ type: "inlineCode", value: match[3] });
    }
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < text.length) {
    nodes.push({ type: "text", value: text.slice(lastIndex) });
  }
  return nodes;
}

// Parse a (possibly multi-paragraph) markdown description string into an array
// of paragraph AST nodes. Paragraphs are separated by blank lines.
function parseDescription(text) {
  return text
    .trim()
    .split(/\n\n+/)
    .map((para) => ({
      type: "paragraph",
      children: parseInline(para.replace(/\n/g, " ")),
    }));
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

      let metaKey;
      const subfolderMatch = SUBFOLDER_RE.exec(exprValue);
      if (subfolderMatch) {
        metaKey = `${examplesPath}/${subfolderMatch[1]}`;
      } else {
        const hardcodedMatch = HARDCODED_PATH_RE.exec(exprValue);
        if (hardcodedMatch) metaKey = hardcodedMatch[1];
      }
      if (!metaKey) continue;

      const entry = metadata[metaKey];
      const title = entry?.title;
      if (!title) continue;

      if (entry.displayTitle === false) continue;

      insertions.push({ index: i, title, description: entry?.description ?? null });
    }

    // Insert in reverse order so earlier indices stay valid.
    for (let i = insertions.length - 1; i >= 0; i--) {
      const { index, title, description } = insertions[i];
      const nodes = [
        { type: "heading", depth: 3, children: [{ type: "text", value: title }] },
        ...(description ? parseDescription(description) : []),
      ];
      tree.children.splice(index, 0, ...nodes);
    }
  };
};
