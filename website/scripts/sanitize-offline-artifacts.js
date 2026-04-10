const fs = require("fs");
const path = require("path");

/**
 * Sanitize offline-generated MDX artifacts that may contain unescaped MDX/JSX.
 * This runs as a post-processing step after CrocoDocs generates partials.
 *
 * When CrocoDocs fails (e.g., offline), the PyPI index partial may contain
 * unescaped characters like <, >, [, ] which break MDX compilation.
 *
 * This script replaces invalid partials with safe fallback versions.
 */

const crocodocs_dir = path.resolve(__dirname, "..", ".crocodocs");

function sanitize_pypi_index() {
  const pypi_file = path.join(crocodocs_dir, "pypi-index.mdx");
  if (!fs.existsSync(pypi_file)) {
    return; // File doesn't exist; nothing to sanitize
  }

  const content = fs.readFileSync(pypi_file, "utf-8");

  // Check for common unescaped MDX/JSX patterns in warning blocks
  // (heuristic: if we see <, >, [, ] outside code blocks in a warning, it's likely broken)
  const lines = content.split("\n");
  let in_warning = false;
  let has_unescaped = false;

  for (const line of lines) {
    if (line.includes(":::warning")) {
      in_warning = true;
    } else if (line.includes(":::")) {
      in_warning = false;
    }

    if (in_warning) {
      // Simple heuristic: bare < > [ ] outside backticks are problematic in MDX
      const outside_backticks = line.replace(/`[^`]+`/g, "");
      if (/[<>\[\]]/.test(outside_backticks)) {
        has_unescaped = true;
        break;
      }
    }
  }

  if (has_unescaped) {
    // Replace with safe fallback
    const fallback = `:::info
PyPI index unavailable (offline or network error).

Run \`yarn crocodocs:generate\` from \`website/\` when online to fetch the latest packages.
:::
`;
    fs.writeFileSync(pypi_file, fallback, "utf-8");
    console.warn(
      `  [warn] Sanitized ${pypi_file}: replaced invalid offline content`,
    );
  }
}

// Run sanitization
try {
  if (!fs.existsSync(crocodocs_dir)) {
    // Artifacts directory doesn't exist yet; nothing to sanitize
    process.exit(0);
  }
  sanitize_pypi_index();
} catch (err) {
  console.error("Error sanitizing offline artifacts:", err.message);
  process.exit(1);
}
