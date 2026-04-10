const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const websiteRoot = path.resolve(__dirname, "..");
const repoRoot = path.resolve(websiteRoot, "..");

const requiredArtifacts = [
  path.join(websiteRoot, ".crocodocs", "api-data.json"),
  path.join(websiteRoot, ".crocodocs", "docs-manifest.json"),
  path.join(websiteRoot, "sidebars.js"),
];

const ALLOWED_COMMANDS = new Set(["uv", "node", "docusaurus"]);

function run(command, args, options = {}) {
  if (!ALLOWED_COMMANDS.has(command)) {
    throw new Error(`Command not allowed: ${command}`);
  }
  const result = spawnSync(command, args, {
    stdio: "inherit",
    // shell: true is intentionally avoided to prevent command injection.
    // On Windows, .cmd wrappers in node_modules/.bin require a shell.
    shell: process.platform === "win32",
    ...options,
  });
  return typeof result.status === "number" ? result.status : 1;
}

function hasAllArtifacts() {
  return requiredArtifacts.every((file) => fs.existsSync(file));
}

const generateExitCode = run(
  "uv",
  ["--directory", "./tools/crocodocs", "run", "crocodocs", "generate"],
  { cwd: repoRoot },
);

if (generateExitCode !== 0) {
  if (!hasAllArtifacts()) {
    console.error(
      "\nCrocoDocs generation failed and required generated artifacts are missing.",
    );
    console.error(
      "Connect to the internet once and run 'yarn crocodocs:generate' from website/.\n",
    );
    process.exit(generateExitCode);
  }

  console.warn(
    "\nCrocoDocs generation failed. Reusing existing generated artifacts for offline start.\n",
  );
}

// Sanitize offline-generated artifacts (removes unescaped MDX/JSX in error messages)
const sanitizeExitCode = run(
  "node",
  [path.join("scripts", "sanitize-offline-artifacts.js")],
  {
    cwd: websiteRoot,
  },
);
if (sanitizeExitCode !== 0) {
  console.error("Failed to sanitize offline artifacts");
  process.exit(sanitizeExitCode);
}

const startExitCode = run("docusaurus", ["start"], { cwd: websiteRoot });
process.exit(startExitCode);
