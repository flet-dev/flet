const fs = require("fs");
const path = require("path");

function visit(node, fn) {
  fn(node);
  if (Array.isArray(node.children)) {
    for (const child of node.children) {
      visit(child, fn);
    }
  }
}

module.exports = function remarkApiLinks() {
  const apiDataPath = path.join(__dirname, "..", ".crocodocs", "api-data.json");
  let xrefMap = {};
  if (fs.existsSync(apiDataPath)) {
    const data = JSON.parse(fs.readFileSync(apiDataPath, "utf8"));
    xrefMap = data.xref_map || {};
  }

  return (tree) => {
    visit(tree, (node) => {
      if (!Array.isArray(node.children) || node.children.length < 3) {
        return;
      }

      let changed = false;
      do {
        changed = false;
        const rewritten = [];
        for (let i = 0; i < node.children.length; i += 1) {
          const current = node.children[i];
          const next = node.children[i + 1];
          const after = node.children[i + 2];

          if (
            current?.type === "text" &&
            current.value.endsWith("[") &&
            next?.type === "inlineCode" &&
            after?.type === "text"
          ) {
            const match = after.value.match(/^\]\[([^\]]+)\](.*)$/s);
            const url = match ? xrefMap[match[1]] : null;
            if (url) {
              const prefix = current.value.slice(0, -1);
              if (prefix) {
                rewritten.push({...current, value: prefix});
              }
              rewritten.push({
                type: "link",
                url,
                children: [{...next}],
              });
              if (match[2]) {
                rewritten.push({...after, value: match[2]});
              }
              i += 2;
              changed = true;
              continue;
            }
          }

          rewritten.push(current);
        }

        node.children = rewritten;
      } while (changed);
    });

    visit(tree, (node) => {
      if (node.type !== "linkReference") {
        return;
      }
      const url = xrefMap[node.identifier];
      if (!url) {
        return;
      }
      node.type = "link";
      node.url = url;
      delete node.identifier;
      delete node.referenceType;
      delete node.label;
    });
  };
};
