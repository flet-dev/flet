import React from "react";
import apiData from "@site/.crocodocs/api-data.json";
import codeExamples from "@site/.crocodocs/code-examples.json";
import Admonition from "@theme/Admonition";
import {unified} from "unified";
import remarkDirective from "remark-directive";
import remarkGfm from "remark-gfm";
import remarkMdx from "remark-mdx";
import remarkParse from "remark-parse";

const IMAGE_LINE_RE = /^!\[([^\]]*)\]\(([^)]+)\)(\{[^}]*\})?$/;
const WIDTH_RE = /width="([^"]+)"/;
const XREF_TEXT_RE = /\[([^\]]+)\]\[((?:[^\]]|\](?=[^.]))+?)\]/g;
const API_SYMBOL_RE =
  /\b(?:ft|flet(?:_[a-z0-9_]+)?)\.[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\b|\b[A-Z][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\b/g;
const MARKDOWN_PARSER = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkDirective)
  .use(remarkMdx);

export function getApiData() {
  return apiData;
}

export function getExampleSource(path) {
  return codeExamples[path] ?? null;
}

export function normalizeAnchor(name) {
  return String(name)
    .replace(/["']/g, "")
    .replace(/\[([^\]]+)\]/g, "-$1")
    .replace(/[^A-Za-z0-9._-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

export function rootAnchor(symbol) {
  return normalizeAnchor(symbol);
}

export function sectionAnchor(symbol, sectionName) {
  return normalizeAnchor(`${symbol}-${sectionName.toLowerCase()}`);
}

export function memberAnchor(symbol, memberName) {
  return normalizeAnchor(`${symbol}-${memberName}`);
}

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

function cleanApiSymbol(symbol) {
  return symbol.replace(/^['"]|['"]$/g, "");
}

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
  const classBaseRoute = classRoute ? classRoute.split("#", 1)[0] : null;
  const classEntry = classSymbol
    ? api.classes?.[classSymbol] ?? api.functions?.[classSymbol] ?? api.aliases?.[classSymbol]
    : null;

  function resolveLocalMemberAnchor(memberName) {
    if (!classSymbol || !classEntry) {
      return null;
    }
    if (
      classEntry.properties?.some((item) => item.name === memberName)
    ) {
      return memberAnchor(classSymbol, memberName);
    }
    if (
      classEntry.events?.some((item) => item.name === memberName)
    ) {
      return memberAnchor(classSymbol, memberName);
    }
    if (
      classEntry.methods?.some((item) => item.name === memberName)
    ) {
      return memberAnchor(classSymbol, memberName);
    }
    if (["properties", "events", "methods"].includes(memberName.toLowerCase())) {
      return sectionAnchor(classSymbol, memberName);
    }
    return normalizeAnchor(memberName);
  }

  if (target === "(c)" || target === "..") {
    return classRoute;
  }
  if ((target === "(c)." || target === "..") && classBaseRoute) {
    return `${classBaseRoute}#${resolveLocalMemberAnchor(cleanLabel)}`;
  }
  if (target.startsWith("(c).") && classBaseRoute) {
    return `${classBaseRoute}#${resolveLocalMemberAnchor(target.slice(4))}`;
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

export function renderCodeExpression(text, context = {}) {
  return renderAutolinkedText(text, context, true);
}

function renderCodeBlock(code, language, key) {
  return (
    <pre key={key}>
      <code className={language ? `language-${language}` : undefined}>{code}</code>
    </pre>
  );
}

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

function renderImage(line, context, key) {
  const match = IMAGE_LINE_RE.exec(line.trim());
  if (!match) {
    return <p key={key}>{renderInlineMarkdown(line, context)}</p>;
  }
  return renderImageFromMatch(match, context, key);
}

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
    default:
      return [];
  }
}

export function renderInlineMarkdown(text, context) {
  if (!text) {
    return null;
  }
  const tree = MARKDOWN_PARSER.parse(
    escapeMdxUnsafeAngles(preprocessCrossReferenceMarkdown(text, context))
  );
  const paragraph =
    tree.children.length === 1 && tree.children[0].type === "paragraph"
      ? tree.children[0]
      : tree;
  return paragraph.type === "paragraph"
    ? renderInlineNodes(paragraph.children ?? [], context, "inline")
    : renderMarkdownNode(paragraph, context, "inline");
}

export function renderDocstring(docstring, context = {}, keyPrefix = "doc") {
  if (!docstring) {
    return null;
  }
  const tree = MARKDOWN_PARSER.parse(
    escapeMdxUnsafeAngles(
      preprocessCrossReferenceMarkdown(
        normalizeDocstringMarkdown(docstring),
        context
      )
    )
  );
  return renderMarkdownNode(tree, context, keyPrefix);
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
