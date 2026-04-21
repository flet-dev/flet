import React from "react";
import apiData from "@site/.crocodocs/api-data.json";
import codeExamples from "@site/.crocodocs/code-examples.json";
import Admonition from "@theme/Admonition";
import CodeBlock from "@theme/CodeBlock";
import {unified} from "unified";
import remarkDirective from "remark-directive";
import remarkGfm from "remark-gfm";
import remarkMdx from "remark-mdx";
import remarkParse from "remark-parse";

const IMAGE_LINE_RE = /^!\[([^\]]*)\]\(([^)]+)\)(\{[^}]*\})?$/;
const WIDTH_RE = /width="([^"]+)"/;
const XREF_TEXT_RE = /\[([^\]]+)\]\[((?:[^\]]|\](?=[^.]))+?)\]/g;
const REST_XREF_RE = /^:(?:py:)?(class|attr|meth|func|data|mod|obj):`([^`\n]+)`/;
// Qualified references like `flet.Page` or `ft.Control.visible`. Safe to auto-link
// anywhere — the `flet.`/`ft.` prefix unambiguously marks this as an API reference.
const API_QUALIFIED_SYMBOL_RE =
  /\b(?:ft|flet(?:_[a-z0-9_]+)?)\.[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\b/g;
// Qualified OR bare capitalized identifiers (`Page`, `Control.visible`). Only safe
// inside code expressions (signature boxes, type annotations) where every capitalized
// token is an identifier. In prose, bare words like "Event", "Text", or "When" would
// be false positives — use API_QUALIFIED_SYMBOL_RE there instead.
const API_SYMBOL_RE =
  /\b(?:ft|flet(?:_[a-z0-9_]+)?)\.[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\b|\b[A-Z][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\b/g;
const MARKDOWN_PARSER = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkDirective)
  .use(remarkMdx);

/** Return the bundled api-data.json object. */
export function getApiData() {
  return apiData;
}

/**
 * Return the source code string for a bundled example file, or null if not found.
 * @param {string} path - Relative path key as it appears in code-examples.json.
 */
export function getExampleSource(path) {
  return codeExamples[path] ?? null;
}

/**
 * Convert a name string to a URL-safe anchor by stripping quotes, replacing brackets,
 * collapsing non-alphanumeric runs to hyphens, and trimming leading/trailing hyphens.
 */
export function normalizeAnchor(name) {
  return String(name)
    .replace(/["']/g, "")
    .replace(/\[([^\]]+)\]/g, "-$1")
    .replace(/[^A-Za-z0-9._-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

/** Return the anchor ID for the root heading of a symbol's documentation page. */
export function rootAnchor(symbol) {
  return normalizeAnchor(symbol);
}

/** Return the anchor ID for a named section (e.g. 'properties', 'events') within a symbol's page. */
export function sectionAnchor(symbol, sectionName) {
  return normalizeAnchor(`${symbol}-${sectionName.toLowerCase()}`);
}

/** Return the anchor ID for a named member (property, event, or method) within a symbol's page. */
export function memberAnchor(symbol, memberName) {
  return normalizeAnchor(`${symbol}.${memberName}`);
}

/**
 * Return all package-path prefixes of classSymbol (longest first) as symbol resolution candidates.
 * Used to expand an unqualified name like 'Text' to 'flet.controls.text.Text', etc.
 */
function classPackageCandidates(classSymbol) {
  if (!classSymbol || !classSymbol.includes(".")) {
    return [];
  }
  const parts = classSymbol.split(".").slice(0, -1);
  const candidates = [];
  for (let i = parts.length; i > 0; i -= 1) {
    const candidate = parts.slice(0, i).join(".");
    if (!candidates.includes(candidate)) {
      candidates.push(candidate);
    }
  }
  return candidates;
}

/** Strip surrounding single or double quotes from a symbol string. */
function cleanApiSymbol(symbol) {
  return symbol.replace(/^['"]|['"]$/g, "");
}

/**
 * Format a symbol for display in a code link by stripping the leading package prefix
 * (ft., flet., or flet_*.) so that only the short class/member name is shown.
 */
function formatApiSymbolLabel(symbol) {
  const cleanSymbol = cleanApiSymbol(symbol);
  if (
    cleanSymbol.startsWith("ft.") ||
    cleanSymbol.startsWith("flet.") ||
    cleanSymbol.startsWith("flet_")
  ) {
    const parts = cleanSymbol.split(".");
    return parts.length > 1 ? parts.slice(1).join(".") : parts[0];
  }
  return cleanSymbol;
}

/** Look up a symbol in classes, functions, or aliases and return the first match, or null. */
function getApiEntry(symbol, api) {
  return api.classes?.[symbol] ?? api.functions?.[symbol] ?? api.aliases?.[symbol] ?? null;
}

/**
 * Resolve a single candidate symbol string to a documentation URL.
 * First checks xref_map directly, then falls back to the entry's qualname/canonical_path.
 * Returns null if no URL can be found.
 */
function resolveApiCandidateHref(candidate, api) {
  if (!candidate) {
    return null;
  }

  const directHref = api.xref_map?.[candidate];
  if (directHref) {
    return directHref;
  }

  const entry = getApiEntry(candidate, api);
  if (!entry) {
    return null;
  }

  return (
    api.xref_map?.[entry.qualname] ??
    api.xref_map?.[entry.canonical_path] ??
    api.xref_map?.[entry.target_path] ??
    null
  );
}

/**
 * Resolve a symbol string to its documentation URL, trying multiple candidate forms.
 * Handles ft./flet. aliases and unqualified names relative to the current class context.
 *
 * @param {string} symbol - Symbol to resolve (may be qualified or unqualified).
 * @param {object} [context] - Optional context with api and classSymbol fields.
 * @returns {string|null} The resolved URL, or null if not found.
 */
export function resolveApiSymbolHref(symbol, context = {}) {
  if (!symbol) {
    return null;
  }

  const api = context.api ?? getApiData();
  const cleanSymbol = cleanApiSymbol(symbol);
  const candidates = [];

  /** Append candidate to the list if it is non-empty and not already present. */
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
  } else if (
    !cleanSymbol.startsWith("ft.") &&
    !cleanSymbol.startsWith("flet.") &&
    !cleanSymbol.startsWith("flet_")
  ) {
    for (const packageName of classPackageCandidates(context.classSymbol)) {
      addCandidate(`${packageName}.${cleanSymbol}`);
    }
    addCandidate(`flet.${cleanSymbol}`);
  }

  for (const candidate of candidates) {
    const href = resolveApiCandidateHref(candidate, api);
    if (href) {
      return href;
    }
  }

  return null;
}

/**
 * Return the value of the first 'text' section in a docstring sections array, or null.
 * Used to fall back to structured sections when a plain docstring string is absent.
 */
function firstTextSectionValue(sections) {
  if (!sections || sections.length === 0) {
    return null;
  }
  const textSection = sections.find(
    (section) => section.kind === "text" && typeof section.value === "string" && section.value.trim(),
  );
  return textSection?.value ?? null;
}

/**
 * Extract the first sentence from a docstring string or its structured sections,
 * for use in summary tables. Returns null when no text is available.
 */
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

/**
 * Resolve a split URL path array by processing '..' and '.' segments,
 * returning the resulting parts array without empty or '.' entries.
 */
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

/**
 * Resolve a doc-relative asset path to an absolute URL.
 * Absolute URLs, protocol-relative URLs, root-relative paths, and fragment refs are returned as-is.
 * Paths without '..' are served from the /docs/ static root.
 * Paths with '..' are resolved relative to the current doc's directory.
 *
 * @param {string} src - The image or asset source path.
 * @param {string} docId - The current doc's ID (e.g. 'controls/button').
 * @returns {string} The resolved absolute URL.
 */
export function resolveDocAssetUrl(src, docId) {
  if (!src || /^(?:[a-z]+:)?\/\//i.test(src) || src.startsWith("/") || src.startsWith("#")) {
    return src;
  }
  // Paths without ../ are relative to /docs/ static root
  if (!src.startsWith("..")) {
    return `/docs/${src}`;
  }
  if (!docId) {
    return src;
  }
  const sourceDir = docId.includes("/") ? docId.split("/").slice(0, -1) : [];
  const resolved = normalizeDocPath([...sourceDir, ...src.split("/")]);
  return `/${["docs", ...resolved].join("/")}`;
}

/** Remove leading and trailing backtick characters from a string. */
function stripTicks(text) {
  return text.replace(/^`|`$/g, "");
}

/** Return the API entry for context.classSymbol, or null when no classSymbol is set. */
function getContextEntry(context, api) {
  return context?.classSymbol ? getApiEntry(context.classSymbol, api) : null;
}

/**
 * Resolve memberName to an anchor ID within the current class context.
 * Matches the class name itself, any of its properties/events/methods, or section names.
 * Returns null when there is no match.
 */
function resolveLocalMemberAnchor(memberName, context, api) {
  const classSymbol = context?.classSymbol;
  const classEntry = getContextEntry(context, api);
  if (!classSymbol || !classEntry) {
    return null;
  }

  if (classEntry.name === memberName) {
    return rootAnchor(classSymbol);
  }

  if (
    classEntry.properties?.some((item) => item.name === memberName) ||
    classEntry.events?.some((item) => item.name === memberName) ||
    classEntry.methods?.some((item) => item.name === memberName)
  ) {
    return memberAnchor(classSymbol, memberName);
  }

  if (["properties", "events", "methods"].includes(memberName.toLowerCase())) {
    return sectionAnchor(classSymbol, memberName);
  }

  return null;
}

/**
 * Build a full href (route + anchor) for a member name within the current class context.
 * Returns null when the class route or member anchor cannot be resolved.
 */
function resolveLocalMemberHref(memberName, context, api) {
  const classSymbol = context?.classSymbol;
  if (!classSymbol) {
    return null;
  }

  const classRoute = resolveApiSymbolHref(classSymbol, {...context, api});
  const anchor = resolveLocalMemberAnchor(memberName, context, api);
  if (!classRoute || !anchor) {
    return null;
  }

  const classBaseRoute = classRoute.split("#", 1)[0];
  return `${classBaseRoute}#${anchor}`;
}

/**
 * Return symbol if it exists in the API, or its canonical public name if found via canonical_map.
 * Returns null when neither form resolves to an API entry.
 */
function resolveQualifiedSymbol(symbol, api) {
  if (getApiEntry(symbol, api)) {
    return symbol;
  }
  const publicName = api.canonical_map?.[symbol];
  if (publicName && getApiEntry(publicName, api)) {
    return publicName;
  }
  return null;
}

/** Return the last dot-separated segment of a qualified name (e.g. 'flet.Button' -> 'Button'). */
function shortenQualifiedDisplay(target) {
  return target.split(".").at(-1) ?? target;
}

/**
 * Strip the leading public Flet module alias from a display label while preserving
 * the remaining qualified path (e.g. 'flet.Page.route' -> 'Page.route').
 */
function stripFletDisplayPrefix(target) {
  if (target.startsWith("ft.")) {
    return target.slice(3);
  }
  if (target.startsWith("flet.")) {
    return target.slice(5);
  }
  return target;
}

/**
 * Format the display label for a reStructuredText cross-reference target.
 * A leading '~' causes the label to be shortened to just the last component.
 * Otherwise, leading 'flet.'/'ft.' is stripped from the rendered label.
 * A trailing '()' is preserved on the display label.
 */
function formatRestXrefLabel(target) {
  const shortened = target.startsWith("~");
  const normalized = shortened ? target.slice(1) : target;
  const hasCall = normalized.endsWith("()");
  const base = hasCall ? normalized.slice(0, -2) : normalized;
  const display = shortened
    ? shortenQualifiedDisplay(base)
    : stripFletDisplayPrefix(base);
  return hasCall ? `${display}()` : display;
}

/**
 * Resolve a reStructuredText cross-reference (:py:class:`Foo`, :attr:`bar`, etc.) to a href and label.
 * Tries local member resolution, then class context, then full symbol lookup, then base class walking.
 * Returns null when no href can be found.
 */
function resolveRestCrossReference(role, target, context) {
  const api = context?.api ?? getApiData();
  const trimmed = target.trim();
  if (!trimmed || trimmed.includes("<")) {
    return null;
  }

  const normalized = trimmed.startsWith("~") ? trimmed.slice(1) : trimmed;
  const lookupTarget = role === "meth" && normalized.endsWith("()")
    ? normalized.slice(0, -2)
    : normalized;

  let href = null;
  if (!lookupTarget.includes(".") && ["attr", "meth", "data", "obj"].includes(role)) {
    href = resolveLocalMemberHref(lookupTarget, context, api);
  }

  if (!href && !lookupTarget.includes(".") && role === "class") {
    const contextEntry = getContextEntry(context, api);
    if (contextEntry?.name === lookupTarget) {
      href = resolveApiSymbolHref(context.classSymbol, {...context, api});
    }
  }

  if (!href) {
    href = resolveApiSymbolHref(lookupTarget, {...context, api});
  }

  // For unqualified members, try base classes (handles inherited members)
  if (!href && !lookupTarget.includes(".") && context?.classSymbol) {
    const entry = getApiEntry(context.classSymbol, api);
    for (const base of entry?.bases ?? []) {
      const resolvedBase = resolveQualifiedSymbol(base, api);
      if (!resolvedBase) continue;
      href = resolveLocalMemberHref(lookupTarget, {...context, classSymbol: resolvedBase}, api);
      if (href) break;
    }
  }

  // For qualified member targets (e.g. flet.Card.margin), resolve class then walk bases
  if (!href && lookupTarget.includes(".")) {
    const lastDot = lookupTarget.lastIndexOf(".");
    const classPart = lookupTarget.slice(0, lastDot);
    const memberName = lookupTarget.slice(lastDot + 1);
    const resolvedClass = resolveQualifiedSymbol(classPart, api);
    if (resolvedClass) {
      href = resolveLocalMemberHref(memberName, {classSymbol: resolvedClass}, api);
      if (!href) {
        const entry = getApiEntry(resolvedClass, api);
        for (const base of entry?.bases ?? []) {
          const resolvedBase = resolveQualifiedSymbol(base, api);
          if (!resolvedBase) continue;
          href = resolveLocalMemberHref(memberName, {classSymbol: resolvedBase}, api);
          if (href) break;
        }
      }
    }
  }

  if (!href) {
    return null;
  }

  return {
    href,
    label: formatRestXrefLabel(trimmed),
  };
}

/**
 * Resolve a CrocoDocs cross-reference target string (from [label][target] syntax) to a href.
 * Special targets: '(c)' = current class, '(c).' = local member, '(c).Foo' = specific local member,
 * 'Pkg.' = absolute qualified lookup (appended with label). All other values use resolveApiSymbolHref.
 */
function resolveCrossReference(target, label, context) {
  const api = getApiData();
  const cleanLabel = stripTicks(label);

  if (target === "(c)") {
    return resolveApiSymbolHref(context?.classSymbol, {...context, api});
  }
  if (target === "(c)." || target === "..") {
    return resolveLocalMemberHref(cleanLabel, context, api);
  }
  if (target.startsWith("(c).")) {
    return resolveLocalMemberHref(target.slice(4), context, api);
  }
  if (target.endsWith(".")) {
    const absoluteTarget = target + cleanLabel;
    return resolveApiCandidateHref(absoluteTarget, api);
  }
  return resolveApiSymbolHref(target, {...context, api});
}

/**
 * Scan text for API symbol patterns and wrap each resolved symbol in an anchor element.
 * When code=true, uses formatApiSymbolLabel for the link label and adds a code-link class.
 * In prose (code=false), only qualified `flet.X`/`ft.X` references are matched — bare
 * capitalized words are skipped to avoid linking common English words like "Event".
 * Returns the original text string when no symbols resolve.
 */
function renderAutolinkedText(text, context, code = false) {
  const nodes = [];
  let lastIndex = 0;
  let key = 0;

  const pattern = code ? API_SYMBOL_RE : API_QUALIFIED_SYMBOL_RE;
  for (const match of text.matchAll(pattern)) {
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

/**
 * Render a text string by resolving [label][target] cross-references to anchor elements
 * and auto-linking any remaining bare API symbols.
 */
function renderTextWithCrossReferences(text, context, keyPrefix) {
  const nodes = [];
  let lastIndex = 0;
  let key = 0;

  for (const match of text.matchAll(XREF_TEXT_RE)) {
    if (match.index > lastIndex) {
      nodes.push(
        ...[].concat(
          renderAutolinkedText(text.slice(lastIndex, match.index), context)
        )
      );
    }

    const href = resolveCrossReference(match[2], match[1], context);
    if (href) {
      nodes.push(
        <a href={href} key={`${keyPrefix}-${key++}`}>
          {renderInlineMarkdown(match[1], context)}
        </a>
      );
    } else {
      nodes.push(match[0]);
    }

    lastIndex = match.index + match[0].length;
  }

  if (lastIndex < text.length) {
    nodes.push(
      ...[].concat(renderAutolinkedText(text.slice(lastIndex), context))
    );
  }

  return nodes.length ? nodes : text;
}

/**
 * Replace [label][target] cross-references in markdown text with standard [label](href) links
 * before the text is fed to the Markdown parser. Skips fenced code blocks.
 */
function preprocessCrossReferenceMarkdown(text, context) {
  if (!text) {
    return text;
  }

  const segments = text.split(/(```[\s\S]*?```)/g);
  return segments
    .map((segment) => {
      if (segment.startsWith("```")) {
        return segment;
      }
      return segment.replace(XREF_TEXT_RE, (full, label, target) => {
        const href = resolveCrossReference(target, label, context);
        return href ? `[${label}](${href})` : full;
      });
    })
    .join("");
}

/**
 * Replace reStructuredText :role:`target` cross-references in markdown text with
 * [`label`](href) links before the text is fed to the Markdown parser.
 * Skips fenced code blocks and inline code spans.
 */
function preprocessRestCrossReferenceMarkdown(text, context) {
  if (!text) {
    return text;
  }

  let index = 0;
  let output = "";

  while (index < text.length) {
    if (text.startsWith("```", index)) {
      const fenceEnd = text.indexOf("```", index + 3);
      if (fenceEnd < 0) {
        output += text.slice(index);
        break;
      }
      output += text.slice(index, fenceEnd + 3);
      index = fenceEnd + 3;
      continue;
    }

    const roleMatch = REST_XREF_RE.exec(text.slice(index));
    if (roleMatch) {
      const resolved = resolveRestCrossReference(roleMatch[1], roleMatch[2], context);
      if (resolved) {
        output += `[\`${resolved.label}\`](${resolved.href})`;
      } else {
        output += roleMatch[0];
      }
      index += roleMatch[0].length;
      continue;
    }

    if (text[index] === "`") {
      const inlineEnd = text.indexOf("`", index + 1);
      if (inlineEnd < 0) {
        output += text.slice(index);
        break;
      }
      output += text.slice(index, inlineEnd + 1);
      index = inlineEnd + 1;
      continue;
    }

    output += text[index];
    index += 1;
  }

  return output;
}

/**
 * Escape bare '<' characters (not followed by tag-start or '!') to '&lt;' in non-code text.
 * Prevents MDX from treating angle brackets in docstrings as JSX elements.
 * Skips fenced code blocks and inline backtick spans.
 */
function escapeMdxUnsafeAngles(text) {
  if (!text) {
    return text;
  }

  const fenceSplit = text.split(/(```[\s\S]*?```)/g);
  return fenceSplit
    .map((fenceSegment) => {
      if (fenceSegment.startsWith("```")) {
        return fenceSegment;
      }
      const inlineSplit = fenceSegment.split(/(`[^`\n]+`)/g);
      return inlineSplit
        .map((inlineSegment) => {
          if (inlineSegment.startsWith("`") && inlineSegment.endsWith("`")) {
            return inlineSegment;
          }
          return inlineSegment.replace(/<(?![A-Za-z!/])/g, "&lt;");
        })
        .join("");
    })
    .join("");
}

/**
 * Render a code expression string as React nodes, auto-linking any API symbols it contains.
 * Intended for use inside signature boxes and inline type/default value displays.
 */
export function renderCodeExpression(text, context = {}) {
  return renderAutolinkedText(text, context, true);
}

/** Render a fenced code block using the Docusaurus CodeBlock theme component. */
function renderCodeBlock(code, language, key) {
  return (
    <CodeBlock key={key} language={language ?? "text"}>
      {code}
    </CodeBlock>
  );
}

/**
 * Render an image figure from a regex match array [_, alt, url, attrs].
 * Resolves the src path via resolveDocAssetUrl and applies an optional width override.
 */
function renderImageFromMatch(match, context, key, widthOverride = null) {
  const width = widthOverride ?? WIDTH_RE.exec(match[3] ?? "")?.[1];
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

/**
 * Render a single markdown line as either an image figure (if it matches IMAGE_LINE_RE)
 * or a plain paragraph with inline markdown.
 */
function renderImage(line, context, key) {
  const match = IMAGE_LINE_RE.exec(line.trim());
  if (!match) {
    return <p key={key}>{renderInlineMarkdown(line, context)}</p>;
  }
  return renderImageFromMatch(match, context, key);
}

/**
 * Transform docstring Markdown that uses the Python '/// admonition' convention into
 * Docusaurus ':::type' admonition syntax. Also strips '/// caption' and bare '///' lines.
 */
function normalizeDocstringMarkdown(docstring) {
  const lines = docstring.split("\n");
  const output = [];
  let index = 0;

  while (index < lines.length) {
    const trimmed = lines[index].trim();
    if (trimmed.startsWith("/// caption")) {
      index += 1;
      if (index < lines.length && lines[index].trim() === "///") {
        index += 1;
      }
      continue;
    }
    if (trimmed === "///") {
      index += 1;
      continue;
    }
    const admonitionMatch = trimmed.match(
      /^\/\/\/\s*admonition(?:\s*\|\s*(.+))?$/
    );
    if (!admonitionMatch) {
      output.push(lines[index]);
      index += 1;
      continue;
    }

    const title = admonitionMatch[1]?.trim();
    let admonitionType = "note";
    const body = [];
    index += 1;

    while (index < lines.length) {
      const bodyLine = lines[index];
      const bodyTrimmed = bodyLine.trim();
      if (bodyTrimmed === "///") {
        index += 1;
        break;
      }
      const typeMatch = bodyTrimmed.match(/^type:\s*(\w+)\s*$/);
      if (typeMatch) {
        admonitionType =
          typeMatch[1] === "example" ? "note" : typeMatch[1];
      } else {
        body.push(bodyLine);
      }
      index += 1;
    }

    output.push(`:::${admonitionType}${title ? `[${title}]` : ""}`);
    output.push(...body);
    output.push(":::");
  }

  return output.join("\n");
}

/**
 * Extract the directiveLabel paragraph child from a directive node and render it.
 * Returns the rendered label and the remaining children array (without the label node).
 */
function extractDirectiveLabel(node, context, keyPrefix) {
  const labelIndex = node.children?.findIndex(
    (child) => child.type === "paragraph" && child.data?.directiveLabel
  );
  if (labelIndex == null || labelIndex < 0) {
    return {label: undefined, children: node.children ?? []};
  }
  const labelNode = node.children[labelIndex];
  const label = renderInlineNodes(
    labelNode.children ?? [],
    context,
    `${keyPrefix}-label`
  );
  const children = node.children.filter((_, index) => index !== labelIndex);
  return {label, children};
}

/**
 * Extract a width value from an mdxTextExpression, mdxJsxFlowElement, or mdxJsxTextElement node.
 * Returns null when no width is present.
 */
function extractImageWidth(node) {
  if (!node) {
    return null;
  }
  if (node.type === "mdxTextExpression") {
    return node.value.match(/^width\s*=\s*"([^"]+)"$/)?.[1] ?? null;
  }
  if (
    node.type === "mdxJsxFlowElement" ||
    node.type === "mdxJsxTextElement"
  ) {
    const widthAttr = node.attributes?.find((attr) => attr.name === "width");
    return typeof widthAttr?.value === "string" ? widthAttr.value : null;
  }
  return null;
}

/**
 * Render an image figure from a raw HTML img string, resolving the src and applying width.
 * Returns null when no src attribute is found in the string.
 */
function renderHtmlImage(raw, context, key, widthOverride = null) {
  const srcMatch = raw.match(/\bsrc="([^"]+)"/);
  if (!srcMatch) {
    return null;
  }
  const alt = raw.match(/\balt="([^"]*)"/)?.[1] ?? "";
  const width = widthOverride ?? raw.match(/\bwidth="([^"]+)"/)?.[1] ?? null;
  const src = resolveDocAssetUrl(srcMatch[1], context?.docId);
  return (
    <figure className="doc-screenshot-figure" key={key}>
      <img
        alt={alt}
        className="doc-screenshot"
        src={src}
        style={width ? {width} : undefined}
      />
    </figure>
  );
}

/**
 * Render an array of inline AST nodes to React elements.
 * Pre-processes adjacent text/inlineCode/text triplets that form '[`code`][target]'
 * cross-references into synthetic 'crocodocsCodeReference' nodes before rendering.
 */
function renderInlineNodes(nodes, context, keyPrefix) {
  const repaired = [];
  for (let index = 0; index < nodes.length; index += 1) {
    const node = nodes[index];
    const next = nodes[index + 1];
    const nextNext = nodes[index + 2];
    if (
      node?.type === "text" &&
      next?.type === "inlineCode" &&
      nextNext?.type === "text"
    ) {
      const prefixMatch = node.value.match(/^(.*)\[$/s);
      const suffixMatch = nextNext.value.match(/^\]\[([^\]]+)\](.*)$/s);
      if (prefixMatch && suffixMatch) {
        if (prefixMatch[1]) {
          repaired.push({...node, value: prefixMatch[1]});
        }
        repaired.push({
          type: "crocodocsCodeReference",
          value: next.value,
          target: suffixMatch[1],
        });
        if (suffixMatch[2]) {
          repaired.push({...nextNext, value: suffixMatch[2]});
        }
        index += 2;
        continue;
      }
    }
    repaired.push(node);
  }

  return repaired.flatMap((node, index) =>
    renderMarkdownNode(node, context, `${keyPrefix}-${index}`, true)
  );
}

/**
 * Recursively render a single remark AST node to React elements.
 * Handles all standard Markdown node types plus MDX JSX image elements,
 * directives (admonitions), tables, and the custom 'crocodocsCodeReference' type.
 * Returns an empty array for unknown or unsupported node types.
 */
function renderMarkdownNode(node, context, key, inline = false) {
  if (!node) {
    return [];
  }

  switch (node.type) {
    case "root":
      return node.children.flatMap((child, index) =>
        renderMarkdownNode(child, context, `${key}-${index}`)
      );
    case "paragraph": {
      if (!inline && node.children?.length) {
        const first = node.children[0];
        const second = node.children[1];
        if (
          first.type === "image" &&
          (node.children.length === 1 ||
            (node.children.length === 2 &&
              second?.type === "mdxTextExpression"))
        ) {
          const match = [
            "",
            first.alt ?? "",
            first.url,
            second ? `{width="${extractImageWidth(second)}"}` : "",
          ];
          return renderImageFromMatch(
            match,
            context,
            key,
            second ? extractImageWidth(second) : null
          );
        }
        if (
          first.type === "mdxJsxFlowElement" &&
          first.name === "img" &&
          node.children.length === 1
        ) {
          const raw = `<img ${first.attributes
            .filter((attr) => typeof attr.value === "string")
            .map((attr) => `${attr.name}="${attr.value}"`)
            .join(" ")} />`;
          return renderHtmlImage(raw, context, key);
        }
      }
      return <p key={key}>{renderInlineNodes(node.children ?? [], context, key)}</p>;
    }
    case "text":
      return [].concat(renderTextWithCrossReferences(node.value, context, key));
    case "strong":
      return (
        <strong key={key}>
          {renderInlineNodes(node.children ?? [], context, key)}
        </strong>
      );
    case "emphasis":
      return <em key={key}>{renderInlineNodes(node.children ?? [], context, key)}</em>;
    case "delete":
      return <del key={key}>{renderInlineNodes(node.children ?? [], context, key)}</del>;
    case "inlineCode":
      return <code key={key}>{node.value}</code>;
    case "break":
      return <br key={key} />;
    case "link":
      return (
        <a key={key} href={node.url}>
          {renderInlineNodes(node.children ?? [], context, key)}
        </a>
      );
    case "linkReference": {
      const href = resolveCrossReference(
        node.identifier,
        node.label ?? "",
        context
      );
      if (!href) {
        return renderInlineNodes(node.children ?? [], context, key);
      }
      return (
        <a key={key} href={href}>
          {renderInlineNodes(node.children ?? [], context, key)}
        </a>
      );
    }
    case "crocodocsCodeReference": {
      const href = resolveCrossReference(node.target, node.value, context);
      if (!href) {
        return <code key={key}>{node.value}</code>;
      }
      return (
        <a key={key} href={href}>
          <code>{node.value}</code>
        </a>
      );
    }
    case "list":
      return React.createElement(
        node.ordered ? "ol" : "ul",
        {key},
        node.children.flatMap((child, index) =>
          renderMarkdownNode(child, context, `${key}-${index}`)
        )
      );
    case "listItem":
      if (
        node.children?.length === 1 &&
        node.children[0]?.type === "paragraph"
      ) {
        return (
          <li key={key}>
            {renderInlineNodes(node.children[0].children ?? [], context, key)}
          </li>
        );
      }
      return (
        <li key={key}>
          {node.children.flatMap((child, index) =>
            renderMarkdownNode(child, context, `${key}-${index}`)
          )}
        </li>
      );
    case "code":
      return renderCodeBlock(node.value, node.lang, key);
    case "image": {
      const match = ["", node.alt ?? "", node.url, ""];
      return renderImageFromMatch(match, context, key);
    }
    case "heading":
      return React.createElement(
        `h${Math.min(node.depth, 6)}`,
        {key},
        renderInlineNodes(node.children ?? [], context, key)
      );
    case "blockquote":
      return (
        <blockquote key={key}>
          {node.children.flatMap((child, index) =>
            renderMarkdownNode(child, context, `${key}-${index}`)
          )}
        </blockquote>
      );
    case "thematicBreak":
      return <hr key={key} />;
    case "containerDirective": {
      const {label, children} = extractDirectiveLabel(node, context, key);
      return (
        <Admonition key={key} title={label} type={node.name}>
          {children.flatMap((child, index) =>
            renderMarkdownNode(child, context, `${key}-${index}`)
          )}
        </Admonition>
      );
    }
    case "mdxJsxFlowElement":
    case "mdxJsxTextElement":
      if (node.name === "img") {
        const raw = `<img ${node.attributes
          .filter((attr) => typeof attr.value === "string")
          .map((attr) => `${attr.name}="${attr.value}"`)
          .join(" ")} />`;
        return renderHtmlImage(raw, context, key, extractImageWidth(node));
      }
      return [];
    case "html":
      if (node.value.trim().startsWith("<img")) {
        return renderHtmlImage(node.value, context, key);
      }
      return <div dangerouslySetInnerHTML={{__html: node.value}} key={key} />;
    case "table":
      return (
        <table key={key} className="docstring-table">
          <thead>
            {node.children.slice(0, 1).flatMap((child, i) =>
              renderMarkdownNode(
                {...child, data: {...child.data, isHeader: true}},
                context,
                `${key}-h${i}`
              )
            )}
          </thead>
          <tbody>
            {node.children.slice(1).flatMap((child, i) =>
              renderMarkdownNode(child, context, `${key}-b${i}`)
            )}
          </tbody>
        </table>
      );
    case "tableRow":
      return (
        <tr key={key}>
          {node.children.flatMap((child, i) =>
            renderMarkdownNode(
              node.data?.isHeader
                ? {...child, data: {...child.data, isHeader: true}}
                : child,
              context,
              `${key}-${i}`
            )
          )}
        </tr>
      );
    case "tableCell": {
      const Tag = node.data?.isHeader ? "th" : "td";
      return (
        <Tag key={key}>
          {node.children.flatMap((child, i) =>
            renderMarkdownNode(child, context, `${key}-${i}`)
          )}
        </Tag>
      );
    }
    default:
      return [];
  }
}

/**
 * Parse and render a markdown text string as inline React nodes.
 * Applies cross-reference preprocessing and MDX angle-bracket escaping before parsing.
 * Returns null for empty/null input.
 */
export function renderInlineMarkdown(text, context) {
  if (!text) {
    return null;
  }
  const tree = MARKDOWN_PARSER.parse(
    escapeMdxUnsafeAngles(
      preprocessRestCrossReferenceMarkdown(
        preprocessCrossReferenceMarkdown(text, context),
        context
      )
    )
  );
  const paragraph =
    tree.children.length === 1 && tree.children[0].type === "paragraph"
      ? tree.children[0]
      : tree;
  return paragraph.type === "paragraph"
    ? renderInlineNodes(paragraph.children ?? [], context, "inline")
    : renderMarkdownNode(paragraph, context, "inline");
}

/**
 * Parse and render a full docstring as block React elements.
 * Applies admonition normalization, cross-reference preprocessing, and MDX escaping.
 * Returns null for empty/null input.
 */
export function renderDocstring(docstring, context = {}, keyPrefix = "doc") {
  if (!docstring) {
    return null;
  }
  const tree = MARKDOWN_PARSER.parse(
    escapeMdxUnsafeAngles(
      preprocessRestCrossReferenceMarkdown(
        preprocessCrossReferenceMarkdown(
          normalizeDocstringMarkdown(docstring),
          context
        ),
        context
      )
    )
  );
  return renderMarkdownNode(tree, context, keyPrefix);
}

/**
 * Render a structured docstring sections array (as produced by griffe_extract_script) to React elements.
 * Handles 'text', 'admonition', 'parameters', 'returns', and 'raises' section kinds.
 * Returns null when sections is empty or null.
 */
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

    if (section.kind === "admonition") {
      const VALID_TYPES = new Set([
        "note", "tip", "info", "warning", "danger", "caution",
      ]);
      const admonitionType = VALID_TYPES.has(section.admonition_kind)
        ? section.admonition_kind
        : "note";
      blocks.push(
        <Admonition key={`section-${key++}`} type={admonitionType} title={section.title}>
          {renderDocstring(section.value, context, `adm-${key}`)}
        </Admonition>
      );
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
              fragments.push(
                <span className="crocodocs-summary-name" key="name">
                  {item.name}
                </span>
              );
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
