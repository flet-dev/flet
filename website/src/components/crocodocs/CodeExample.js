import React, {useEffect, useRef, useState} from "react";
import CodeBlock from "@theme/CodeBlock";

import {
  getExampleMetadata,
  getExampleSource,
  getExampleWebSupported,
  loadExampleFileSource,
} from "./utils";

const FLET_STUDIO_BASE = "https://studio.flet.dev/gallery/example";
const EXAMPLES_SOURCE_BASE = "https://github.com/flet-dev/flet/tree/main/sdk/python/examples";

const LANGUAGE_BY_EXTENSION = {
  py: "python",
  toml: "toml",
  md: "markdown",
  json: "json",
  yaml: "yaml",
  yml: "yaml",
  txt: "text",
};

/** Return the Prism language for a file name, or "text" for unknown extensions. */
function languageForFile(name) {
  const extension = name.includes(".") ? name.slice(name.lastIndexOf(".") + 1) : "";
  return LANGUAGE_BY_EXTENSION[extension] ?? "text";
}

/**
 * Return the example files that can be shown as tabs, with the requested file
 * first, then pyproject.toml, then the remaining Python and text files.
 * Python sources come from the code-examples bundle; other text files are loaded
 * on demand, so only their names are checked here.
 */
function viewableFiles(exampleDir, mainFile, files) {
  const rank = (name) => {
    if (name === mainFile) return 0;
    if (name === "pyproject.toml") return 1;
    if (name.endsWith(".py")) return 2;
    return 3;
  };
  return files
    .filter((name) =>
      name.endsWith(".py")
        ? getExampleSource(`${exampleDir}/${name}`) != null
        : languageForFile(name) !== "text" || name.endsWith(".txt"),
    )
    .sort((a, b) => rank(a) - rank(b) || a.localeCompare(b));
}

function GitHubIcon() {
  return (
    <svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" fill="currentColor">
      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
    </svg>
  );
}

/**
 * A button that reveals a copyable `flet create --example` command for the example.
 */
function CreateCommand({exampleDir}) {
  const [open, setOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const containerRef = useRef(null);
  const projectName = exampleDir.slice(exampleDir.lastIndexOf("/") + 1);
  const command = `flet create --example ${exampleDir} ${projectName}`;

  useEffect(() => {
    if (!open) return undefined;
    const close = (event) => {
      if (event.type === "keydown" ? event.key === "Escape" : !containerRef.current?.contains(event.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", close);
    document.addEventListener("keydown", close);
    return () => {
      document.removeEventListener("mousedown", close);
      document.removeEventListener("keydown", close);
    };
  }, [open]);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // The command stays selectable in the popover when the clipboard is unavailable.
    }
  };

  return (
    <div className="code-example-create" ref={containerRef}>
      <button
        type="button"
        className="code-example-action"
        aria-expanded={open}
        onClick={() => setOpen((value) => !value)}
        title="Create a local project from this example"
      >
        <span className="material-symbols-outlined">terminal</span>
        <span className="code-example-action-label">Create project</span>
      </button>
      {open && (
        <div className="code-example-create-popover" role="dialog" aria-label="Create a local project">
          <p>To create a local project from this example, run:</p>
          <div className="code-example-create-command">
            <code>{command}</code>
            <button type="button" onClick={copy} aria-label="Copy command" title="Copy command">
              <span className="material-symbols-outlined">{copied ? "check" : "content_copy"}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Renders a syntax-highlighted code block for a bundled example file.
 *
 * When the file belongs to an example project (a directory with a pyproject.toml),
 * the code block's header shows the project's files as tabs, and a row of actions
 * above it holds a "Try Online" link to Flet Studio when the example supports web,
 * a link to the example's source on GitHub, and a copyable `flet create --example`
 * command. Files that can't be shown
 * as text, such as assets, are counted in the source link.
 * Shows an error message if the example path is not found in the code-examples bundle.
 *
 * @param {string} path - Relative path to the example file within the examples root.
 * @param {string} [language="python"] - Language identifier for syntax highlighting.
 * @param {string} [title] - Optional title displayed for the file, in place of its name.
 */
export default function CodeExample({path, language = "python", title}) {
  const source = getExampleSource(path);
  const exampleDir = path.includes("/") ? path.slice(0, path.lastIndexOf("/")) : path;
  const metadata = getExampleMetadata(exampleDir);
  const mainFile = path.slice(exampleDir.length + 1);
  const files = metadata?.files ?? [];
  const tabs = metadata ? viewableFiles(exampleDir, mainFile, files) : [];

  const [activeFile, setActiveFile] = useState(mainFile);
  const [loadedSources, setLoadedSources] = useState({});

  useEffect(() => {
    if (activeFile === mainFile || activeFile.endsWith(".py") || activeFile in loadedSources) {
      return undefined;
    }
    let cancelled = false;
    loadExampleFileSource(`${exampleDir}/${activeFile}`).then((text) => {
      if (!cancelled) setLoadedSources((current) => ({...current, [activeFile]: text}));
    });
    return () => {
      cancelled = true;
    };
  }, [activeFile, exampleDir, mainFile, loadedSources]);

  if (source == null) {
    return <div>Missing code example for <code>{path}</code>.</div>;
  }

  if (!metadata) {
    return (
      <div className="code-example">
        <CodeBlock language={language} title={title}>
          {source}
        </CodeBlock>
      </div>
    );
  }

  const showTryOnline = getExampleWebSupported(exampleDir);
  const studioUrl = `${FLET_STUDIO_BASE}/${exampleDir}`;
  const sourceUrl = `${EXAMPLES_SOURCE_BASE}/${exampleDir}`;
  const otherFileCount = files.length - tabs.length;

  let activeSource;
  if (activeFile === mainFile) {
    activeSource = source;
  } else if (activeFile.endsWith(".py")) {
    activeSource = getExampleSource(`${exampleDir}/${activeFile}`);
  } else {
    activeSource = loadedSources[activeFile];
  }
  const activeLanguage = activeFile === mainFile ? language : languageForFile(activeFile);

  const fileTabs = (
    <div className="code-example-tabs" role="tablist" aria-label="Example files">
      {tabs.map((name) => (
        <button
          key={name}
          type="button"
          role="tab"
          aria-selected={name === activeFile}
          className="code-example-tab"
          onClick={() => setActiveFile(name)}
        >
          {name === mainFile && title ? title : name}
        </button>
      ))}
    </div>
  );

  return (
    <div className="code-example code-example--project">
      <div className="code-example-actions">
        <CreateCommand exampleDir={exampleDir} />
        <a
          className="code-example-action"
          href={sourceUrl}
          target="_blank"
          rel="noopener noreferrer"
          title={
            otherFileCount > 0
              ? `View the full example on GitHub, including ${otherFileCount} more file${otherFileCount === 1 ? "" : "s"}`
              : "View the full example on GitHub"
          }
        >
          <GitHubIcon />
          <span className="code-example-action-label">
            Source{otherFileCount > 0 ? ` (+${otherFileCount} file${otherFileCount === 1 ? "" : "s"})` : ""}
          </span>
        </a>
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
      </div>
      <CodeBlock language={activeLanguage} title={fileTabs}>
        {activeSource ?? (activeSource === null ? `# ${activeFile} is not available.` : "Loading…")}
      </CodeBlock>
    </div>
  );
}
