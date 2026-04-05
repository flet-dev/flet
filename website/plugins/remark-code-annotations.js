/**
 * Remark plugin that implements MkDocs Material-style code annotations.
 *
 * Detects `# (N)!` markers in code blocks, strips them from displayed code,
 * collects the corresponding numbered list items that follow, and replaces
 * the code node with an <AnnotatedCodeBlock> MDX component.
 */

const MARKER_RE = /^(.*?)\s*#\s*\((\d+)\)!\s*$/m;
const LINE_MARKER_RE = /^(.*?)\s*#\s*\((\d+)\)!\s*$/;

function extractMarkers(code) {
  const lines = code.split("\n");
  const markers = new Map(); // number -> lineIndex
  const cleanedLines = [];

  for (let i = 0; i < lines.length; i++) {
    const match = LINE_MARKER_RE.exec(lines[i]);
    if (match) {
      markers.set(parseInt(match[2], 10), i);
      cleanedLines.push(match[1].trimEnd());
    } else {
      cleanedLines.push(lines[i]);
    }
  }

  return { cleanedCode: cleanedLines.join("\n"), markers };
}

/**
 * Recursively extract text/HTML from an mdast node.
 * Handles: text, inlineCode, link, emphasis, strong, paragraph, and nested children.
 */
function mdastToHtml(node) {
  if (!node) return "";

  if (node.type === "text") {
    return escapeHtml(node.value);
  }
  if (node.type === "inlineCode") {
    return `<code>${escapeHtml(node.value)}</code>`;
  }
  if (node.type === "code") {
    return `<pre><code>${escapeHtml(node.value)}</code></pre>`;
  }
  if (node.type === "link") {
    const children = (node.children || []).map(mdastToHtml).join("");
    const href = escapeHtml(node.url || "");
    return `<a href="${href}">${children}</a>`;
  }
  if (node.type === "emphasis") {
    return `<em>${(node.children || []).map(mdastToHtml).join("")}</em>`;
  }
  if (node.type === "strong") {
    return `<strong>${(node.children || []).map(mdastToHtml).join("")}</strong>`;
  }
  if (node.type === "paragraph") {
    return `<p>${(node.children || []).map(mdastToHtml).join("")}</p>`;
  }
  if (node.type === "list") {
    const tag = node.ordered ? "ol" : "ul";
    const items = (node.children || []).map(mdastToHtml).join("");
    return `<${tag}>${items}</${tag}>`;
  }
  if (node.type === "listItem") {
    return `<li>${(node.children || []).map(mdastToHtml).join("")}</li>`;
  }
  if (node.type === "html") {
    return node.value || "";
  }
  if (Array.isArray(node.children)) {
    return node.children.map(mdastToHtml).join("");
  }
  return "";
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderListItem(listItem) {
  return (listItem.children || []).map(mdastToHtml).join("");
}

function parseMeta(meta) {
  if (!meta) return {};
  const titleMatch = meta.match(/title="([^"]+)"/);
  return titleMatch ? { title: titleMatch[1] } : {};
}

/**
 * Check if a node is a boundary that stops annotation list collection.
 */
function isBoundary(node) {
  return (
    node.type === "heading" ||
    node.type === "code" ||
    node.type === "thematicBreak"
  );
}

function visitParents(tree, fn) {
  if (Array.isArray(tree.children)) {
    fn(tree);
    for (const child of tree.children) {
      visitParents(child, fn);
    }
  }
}

module.exports = function remarkCodeAnnotations() {
  return (tree, file) => {
    visitParents(tree, (parent) => {
      if (!Array.isArray(parent.children)) return;

      const newChildren = [];
      let i = 0;

      while (i < parent.children.length) {
        const child = parent.children[i];

        if (child.type !== "code" || !MARKER_RE.test(child.value)) {
          newChildren.push(child);
          i++;
          continue;
        }

        const { cleanedCode, markers } = extractMarkers(child.value);
        const needed = new Set(markers.keys());
        const annotations = {};

        // Walk forward collecting annotation lists
        let j = i + 1;
        while (j < parent.children.length && needed.size > 0) {
          const sibling = parent.children[j];

          if (isBoundary(sibling)) break;

          if (sibling.type === "list" && sibling.ordered) {
            const start = sibling.start || 1;
            for (let k = 0; k < sibling.children.length; k++) {
              const num = start + k;
              if (needed.has(num)) {
                annotations[num] = {
                  line: markers.get(num),
                  html: renderListItem(sibling.children[k]),
                };
                needed.delete(num);
              }
            }
            j++;
          } else {
            // Skip non-list nodes (admonitions, paragraphs) if we still
            // have unmatched annotations — handles split-list case
            j++;
          }
        }

        const meta = parseMeta(child.meta);

        // Create MDX JSX element for <AnnotatedCodeBlock>
        const jsxNode = {
          type: "mdxJsxFlowElement",
          name: "AnnotatedCodeBlock",
          attributes: [
            {
              type: "mdxJsxAttribute",
              name: "code",
              value: cleanedCode,
            },
            {
              type: "mdxJsxAttribute",
              name: "lang",
              value: child.lang || "",
            },
            {
              type: "mdxJsxAttribute",
              name: "annotations",
              value: JSON.stringify(annotations),
            },
          ],
          children: [],
        };

        if (meta.title) {
          jsxNode.attributes.push({
            type: "mdxJsxAttribute",
            name: "title",
            value: meta.title,
          });
        }

        newChildren.push(jsxNode);
        i = j; // skip consumed siblings
      }

      parent.children = newChildren;
    });
  };
};
