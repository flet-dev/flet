import React from "react";
import apiData from "@site/.crocodocs/api-data.json";
import codeExamples from "@site/.crocodocs/code-examples.json";

const IMAGE_LINE_RE = /^!\[([^\]]*)\]\(([^)]+)\)(\{[^}]*\})?$/;
const WIDTH_RE = /width="([^"]+)"/;
const INLINE_TOKEN_RE = /(`[^`]+`)|\[(.*?)\]\((.*?)\)|\[(.*?)\]\[([^\]]+)\]/g;
const API_SYMBOL_RE = /\b(?:ft|flet(?:_[a-z0-9_]+)?)\.[A-Za-z_][A-Za-z0-9_]*\b|\b[A-Z][A-Za-z0-9_]*\b/g;

export function getApiData() {
  return apiData;
}

export function getExampleSource(path) {
  return codeExamples[path] ?? null;
}

export function normalizeAnchor(name) {
  return name;
}

function classPackageCandidates(classSymbol) {
  if (!classSymbol || !classSymbol.includes(".")) {
    return [];
  }
  const packageName = classSymbol.split(".", 1)[0];
  return packageName ? [packageName] : [];
}

function cleanApiSymbol(symbol) {
  return symbol.replace(/^['"]|['"]$/g, "");
}

function formatApiSymbolLabel(symbol) {
  const cleanSymbol = cleanApiSymbol(symbol);
  if (/^(?:ft|flet(?:_[a-z0-9_]+)?)\./.test(cleanSymbol)) {
    return cleanSymbol.split(".").pop();
  }
  return cleanSymbol;
}

export function resolveApiSymbolHref(symbol, context = {}) {
  if (!symbol) {
    return null;
  }

  const api = context.api ?? getApiData();
  const cleanSymbol = cleanApiSymbol(symbol);
  const candidates = [];

  function addCandidate(candidate) {
    if (!candidate || candidates.includes(candidate)) {
      return;
    }
    candidates.push(candidate);
  }

  addCandidate(cleanSymbol);
  if (cleanSymbol.startsWith("ft.")) {
    addCandidate(`flet.${cleanSymbol.slice(3)}`);
  }

  if (!cleanSymbol.includes(".")) {
    for (const packageName of classPackageCandidates(context.classSymbol)) {
      addCandidate(`${packageName}.${cleanSymbol}`);
    }
    addCandidate(`flet.${cleanSymbol}`);
  }

  for (const candidate of candidates) {
    const href = api.xref_map?.[candidate];
    if (href) {
      return href;
    }
  }

  return null;
}

function firstTextSectionValue(sections) {
  if (!sections || sections.length === 0) {
    return null;
  }
  const textSection = sections.find(
    (section) => section.kind === "text" && typeof section.value === "string" && section.value.trim(),
  );
  return textSection?.value ?? null;
}

export function firstSentenceFromDocstring(docstring, docstringSections) {
  const source = (typeof docstring === "string" && docstring.trim()) ? docstring : firstTextSectionValue(docstringSections);
  if (!source) {
    return null;
  }

  const firstParagraph = source
    .replace(/\n\s*\n[\s\S]*$/, "")
    .replace(/\s+/g, " ")
    .trim();

  const sentenceMatch = firstParagraph.match(/^(.+?[.!?])(?:\s|$)/);
  return sentenceMatch ? sentenceMatch[1].trim() : firstParagraph;
}

function normalizeDocPath(parts) {
  const out = [];
  for (const part of parts) {
    if (!part || part === ".") {
      continue;
    }
    if (part === "..") {
      out.pop();
      continue;
    }
    out.push(part);
  }
  return out;
}

export function resolveDocAssetUrl(src, docId) {
  if (!src || /^(?:[a-z]+:)?\/\//i.test(src) || src.startsWith("/") || src.startsWith("#")) {
    return src;
  }
  if (!docId) {
    return src;
  }
  const sourceDir = docId.includes("/") ? docId.split("/").slice(0, -1) : [];
  const resolved = normalizeDocPath([...sourceDir, ...src.split("/")]);
  return `/${["docs", ...resolved].join("/")}`;
}

function stripTicks(text) {
  return text.replace(/^`|`$/g, "");
}

function resolveCrossReference(target, label, context) {
  const api = getApiData();
  const cleanLabel = stripTicks(label);
  const classSymbol = context?.classSymbol;
  const classRoute = classSymbol ? api.xref_map?.[classSymbol] : null;

  if (target === "(c)" || target === "..") {
    return classRoute;
  }
  if ((target === "(c)." || target === "..") && classRoute) {
    return `${classRoute}#${normalizeAnchor(cleanLabel)}`;
  }
  if (target.startsWith("(c).") && classRoute) {
    return `${classRoute}#${normalizeAnchor(target.slice(4))}`;
  }
  if (target.endsWith(".")) {
    const absoluteTarget = target + cleanLabel;
    return api.xref_map?.[absoluteTarget] ?? null;
  }
  return resolveApiSymbolHref(target, {...context, api});
}

function renderAutolinkedText(text, context, code = false) {
  const nodes = [];
  let lastIndex = 0;
  let key = 0;

  for (const match of text.matchAll(API_SYMBOL_RE)) {
    const matchText = match[0];
    const href = resolveApiSymbolHref(matchText, context);
    if (!href) {
      continue;
    }
    if (match.index > lastIndex) {
      nodes.push(text.slice(lastIndex, match.index));
    }
    nodes.push(
      <a
        className={code ? "crocodocs-code-link" : undefined}
        href={href}
        key={key++}
      >
        {code ? formatApiSymbolLabel(matchText) : matchText}
      </a>,
    );
    lastIndex = match.index + matchText.length;
  }

  if (lastIndex < text.length) {
    nodes.push(text.slice(lastIndex));
  }

  return nodes.length ? nodes : text;
}

export function renderCodeExpression(text, context = {}) {
  return renderAutolinkedText(text, context, true);
}

export function renderInlineMarkdown(text, context) {
  const nodes = [];
  let lastIndex = 0;
  let key = 0;
  for (const match of text.matchAll(INLINE_TOKEN_RE)) {
    if (match.index > lastIndex) {
      nodes.push(...[].concat(renderAutolinkedText(text.slice(lastIndex, match.index), context)));
    }
    if (match[1]) {
      nodes.push(<code key={key++}>{match[1].slice(1, -1)}</code>);
    } else if (match[2] !== undefined) {
      nodes.push(
        <a key={key++} href={match[3]}>
          {renderInlineMarkdown(match[2], context)}
        </a>
      );
    } else {
      const href = resolveCrossReference(match[5], match[4], context);
      if (href) {
        nodes.push(
          <a key={key++} href={href}>
            {renderInlineMarkdown(match[4], context)}
          </a>
        );
      } else {
        nodes.push(match[0]);
      }
    }
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < text.length) {
    nodes.push(...[].concat(renderAutolinkedText(text.slice(lastIndex), context)));
  }
  return nodes;
}

function renderParagraph(text, context, key) {
  return <p key={key}>{renderInlineMarkdown(text, context)}</p>;
}

function renderList(items, context, key) {
  return (
    <ul key={key}>
      {items.map((item, index) => (
        <li key={index}>{renderInlineMarkdown(item, context)}</li>
      ))}
    </ul>
  );
}

function renderCodeBlock(code, language, key) {
  return (
    <pre key={key}>
      <code className={language ? `language-${language}` : undefined}>{code}</code>
    </pre>
  );
}

function renderImage(line, context, key) {
  const match = IMAGE_LINE_RE.exec(line.trim());
  if (!match) {
    return renderParagraph(line, context, key);
  }
  const width = WIDTH_RE.exec(match[3] ?? "")?.[1];
  const src = resolveDocAssetUrl(match[2], context?.docId);
  return (
    <figure className="doc-screenshot-figure" key={key}>
      <img
        alt={match[1]}
        className="doc-screenshot"
        src={src}
        style={width ? {width} : undefined}
      />
    </figure>
  );
}

export function renderDocstring(docstring, context = {}, keyPrefix = "doc") {
  if (!docstring) {
    return null;
  }

  const lines = docstring
    .replace(/\n\/\/\/ caption[^\n]*\n(?:\/\/\/\n)?/g, "\n")
    .split("\n");

  const blocks = [];
  let index = 0;
  let key = 0;

  while (index < lines.length) {
    const line = lines[index];
    const trimmed = line.trim();

    if (!trimmed || trimmed === "///") {
      index += 1;
      continue;
    }

    if (trimmed.startsWith("```")) {
      const language = trimmed.slice(3).trim();
      const codeLines = [];
      index += 1;
      while (index < lines.length && !lines[index].trim().startsWith("```")) {
        codeLines.push(lines[index]);
        index += 1;
      }
      index += 1;
      blocks.push(renderCodeBlock(codeLines.join("\n"), language, `${keyPrefix}-${key++}`));
      continue;
    }

    if (IMAGE_LINE_RE.test(trimmed)) {
      blocks.push(renderImage(trimmed, context, `${keyPrefix}-${key++}`));
      index += 1;
      continue;
    }

    if (trimmed.startsWith("- ")) {
      const items = [];
      while (index < lines.length && lines[index].trim().startsWith("- ")) {
        items.push(lines[index].trim().slice(2));
        index += 1;
      }
      blocks.push(renderList(items, context, `${keyPrefix}-${key++}`));
      continue;
    }

    const paragraphLines = [];
    while (index < lines.length) {
      const candidate = lines[index].trim();
      if (
        !candidate ||
        candidate === "///" ||
        candidate.startsWith("```") ||
        IMAGE_LINE_RE.test(candidate) ||
        candidate.startsWith("- ")
      ) {
        break;
      }
      paragraphLines.push(candidate);
      index += 1;
    }
    if (paragraphLines.length) {
      blocks.push(renderParagraph(paragraphLines.join(" "), context, `${keyPrefix}-${key++}`));
    }
  }

  return blocks;
}

export function renderDocstringSections(sections, context = {}) {
  if (!sections || sections.length === 0) {
    return null;
  }

  const blocks = [];
  let key = 0;

  for (const section of sections) {
    if (section.kind === "text") {
      blocks.push(...(renderDocstring(section.value, context, `section-${key++}`) ?? []));
      continue;
    }

    if (!section.items?.length) {
      continue;
    }

    const title =
      section.kind === "parameters"
        ? "Parameters"
        : section.kind === "returns"
          ? "Returns"
          : section.kind === "raises"
            ? "Raises"
            : null;

    if (!title) {
      continue;
    }

    blocks.push(
      <div key={`section-${key++}`}>
        <p>
          <strong>{title}:</strong>
        </p>
        <ul>
          {section.items.map((item, index) => {
            const fragments = [];
            let openedMeta = false;
            if (item.name) {
              fragments.push(<code key="name">{item.name}</code>);
            }
            if (item.type) {
              fragments.push(
                <React.Fragment key="type">
                  {item.name ? " (" : ""}
                  <span className="crocodocs-inline-code">
                    {renderCodeExpression(item.type, context)}
                  </span>
                </React.Fragment>
              );
              openedMeta = Boolean(item.name);
            }
            if (item.default != null) {
              fragments.push(
                <React.Fragment key="default">
                  {openedMeta ? ", " : item.name ? " (" : ""}
                  default: <code>{item.default}</code>
                </React.Fragment>
              );
              openedMeta = Boolean(item.name);
            }
            if (openedMeta) {
              fragments.push(<React.Fragment key="close">)</React.Fragment>);
            }
            if (item.description) {
              if (fragments.length) {
                fragments.push(
                  <React.Fragment key="sep">
                    {" "}{"-"}{" "}
                  </React.Fragment>
                );
              }
              fragments.push(
                <React.Fragment key="desc">
                  {renderInlineMarkdown(item.description.replace(/\s*\n\s*/g, " "), context)}
                </React.Fragment>
              );
            }

            return <li key={index}>{fragments}</li>;
          })}
        </ul>
      </div>
    );
  }

  return blocks;
}
