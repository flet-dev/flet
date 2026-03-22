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
