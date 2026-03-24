import React, {useEffect, useRef, useState} from "react";
import Heading from "@theme/Heading";
import {useDoc} from "@docusaurus/plugin-content-docs/client";

import {
  firstSentenceFromDocstring,
  getApiData,
  memberAnchor,
  renderCodeExpression,
  renderDocstring,
  renderDocstringSections,
  renderInlineMarkdown,
  resolveDocAssetUrl,
  rootAnchor,
  sectionAnchor,
} from "./utils";

const MEMBER_KIND_META = {
  property: {icon: "build", className: "crocodocs-member-icon--property"},
  event: {icon: "bolt", className: "crocodocs-member-icon--event"},
  method: {icon: "deployed_code", className: "crocodocs-member-icon--method"},
};

function stripImplicitSelf(signatureText) {
  if (!signatureText) {
    return signatureText;
  }

  return signatureText
    .replace(/\(\s*self(?:\s*:\s*[^,)]+)?\s*,\s*/g, "(")
    .replace(/\(\s*self(?:\s*:\s*[^,)]+)?\s*\)/g, "()");
}

function HeadingLink({level: Tag, id, children}) {
  return (
    <Heading as={Tag} id={id}>
      {children}
    </Heading>
  );
}

function Badge({children}) {
  return <span className="crocodocs-member-badge">{children}</span>;
}

function SignatureBox({text, children}) {
  const [copied, setCopied] = useState(false);

  async function onCopy() {
    if (!navigator?.clipboard || !text) {
      return;
    }
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      // Ignore clipboard failures and leave the button idle.
    }
  }

  return (
    <div className="crocodocs-signature-box">
      <button
        className="crocodocs-signature-copy"
        onClick={onCopy}
        title={copied ? "Copied" : "Copy"}
        type="button"
      >
        {copied ? "Copied" : "Copy"}
      </button>
      <pre className="crocodocs-signature-pre">
        <code className="crocodocs-signature-content">{children}</code>
      </pre>
    </div>
  );
}

function Section({title, items, renderItem}) {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <section>
      <HeadingLink level="h2" id={items[0]?.__sectionId ?? null}>
        {title}
      </HeadingLink>
      {items.map(renderItem)}
    </section>
  );
}

function createMemberIconNode(kind) {
  const meta = MEMBER_KIND_META[kind];
  if (!meta) {
    return null;
  }
  const icon = document.createElement("span");
  icon.className = `material-symbols-outlined crocodocs-member-icon crocodocs-member-icon--toc ${meta.className}`;
  icon.setAttribute("aria-hidden", "true");
  icon.textContent = meta.icon;
  return icon;
}

let tocOwnerCounter = 0;

function useInjectedToc(sectionGroups) {
  const ownerRef = useRef(null);
  if (ownerRef.current == null) {
    tocOwnerCounter += 1;
    ownerRef.current = `crocodocs-${tocOwnerCounter}`;
  }

  useEffect(() => {
    const tocRoot = document.querySelector("ul.table-of-contents");
    if (!tocRoot) {
      return undefined;
    }

    tocRoot
      .querySelectorAll(
        `[data-crocodocs-toc='true'][data-crocodocs-toc-owner='${ownerRef.current}']`
      )
      .forEach((node) => node.remove());

    const created = [];
    for (const group of sectionGroups) {
      if (!group.items.length && !group.showWhenEmpty) {
        continue;
      }

      const top = document.createElement("li");
      top.className = [
        "table-of-contents__list-item",
        group.items.length ? "table-of-contents__list-item--nested" : "",
        "generated-crocodocs-toc",
      ]
        .filter(Boolean)
        .join(" ");
      top.dataset.crocodocsToc = "true";
      top.dataset.crocodocsTocOwner = ownerRef.current;

      const link = document.createElement("a");
      link.className = "table-of-contents__link toc-highlight";
      link.href = `#${group.id}`;
      link.textContent = group.title;
      top.appendChild(link);

      if (group.items.length) {
        const nested = document.createElement("ul");
        nested.className = "table-of-contents__sublist";
        for (const item of group.items) {
          const nestedItem = document.createElement("li");
          nestedItem.className =
            "table-of-contents__list-item generated-crocodocs-toc";
          nestedItem.dataset.crocodocsToc = "true";
          nestedItem.dataset.crocodocsTocOwner = ownerRef.current;

          const nestedLink = document.createElement("a");
          nestedLink.className =
            "table-of-contents__link toc-highlight crocodocs-member-toc-link";
          nestedLink.href = `#${item.id}`;
          const icon = createMemberIconNode(item.kind);
          if (icon) {
            nestedLink.appendChild(icon);
          }
          const label = document.createElement("span");
          label.textContent = item.label;
          nestedLink.appendChild(label);
          nestedItem.appendChild(nestedLink);
          nested.appendChild(nestedItem);
          created.push(nestedItem);
        }
        top.appendChild(nested);
      }
      tocRoot.appendChild(top);
      created.push(top);
    }

    return () => {
      created.forEach((node) => node.remove());
    };
  }, [sectionGroups]);
}

function renderMemberHeading(item, classSymbol, kind) {
  const id = memberAnchor(classSymbol, item.name);
  const meta = MEMBER_KIND_META[kind];
  return (
    <HeadingLink level="h3" id={id}>
      <span className="crocodocs-member-heading">
        {meta ? (
          <span
            aria-hidden="true"
            className={`material-symbols-outlined crocodocs-member-icon crocodocs-member-icon--heading ${meta.className}`}
          >
            {meta.icon}
          </span>
        ) : null}
        <span>{item.name}</span>
        {(item.labels || []).length ? (
          <span className="crocodocs-member-badges">
            {(item.labels || []).map((label) => (
              <Badge key={label}>{label}</Badge>
            ))}
          </span>
        ) : null}
      </span>
    </HeadingLink>
  );
}

function renderAttribute(item, classSymbol, docId) {
  const signatureText = `${item.name}: ${item.type}${item.default != null ? ` = ${item.default}` : ""}`;
  const kind = item.name.startsWith("on_") ? "event" : "property";
  return (
    <div key={item.name}>
      {renderMemberHeading(item, classSymbol, kind)}
      {item.type ? (
        <SignatureBox text={signatureText}>
          {renderCodeExpression(signatureText, {classSymbol, docId})}
        </SignatureBox>
      ) : null}
      {renderDocstringSections(item.docstring_sections, {classSymbol, docId}) ??
        renderDocstring(item.docstring, {classSymbol, docId})}
    </div>
  );
}

function renderMethod(item, classSymbol, docId) {
  const signatureText = stripImplicitSelf(item.signature ?? item.name);
  return (
    <div key={item.name}>
      {renderMemberHeading(item, classSymbol, "method")}
      <SignatureBox text={signatureText}>
        {renderCodeExpression(signatureText, {classSymbol, docId})}
      </SignatureBox>
      {renderDocstringSections(item.docstring_sections, {classSymbol, docId}) ??
        renderDocstring(item.docstring, {classSymbol, docId})}
    </div>
  );
}

function SummarySection({title, items, classSymbol}) {
  if (!items.length) {
    return null;
  }

  return (
    <section>
      <Heading as="h4">{title}</Heading>
      <ul>
        {items.map((item) => (
          <li key={item.name}>
            <a href={`#${memberAnchor(classSymbol, item.name)}`}>
              <code>{item.name}</code>
            </a>
            {item.summary ? (
              <>
                {" "}{"-"}{" "}
                {renderInlineMarkdown(item.summary, {classSymbol})}
              </>
            ) : null}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function ClassBlock({
  name,
  showRootHeading = false,
  showDocstring = true,
  showBases = true,
  showSummary = true,
  showMembers = true,
  image,
  imageCaption,
  imageWidth = "40%",
}) {
  const {metadata} = useDoc();
  const api = getApiData();
  const classEntry = api.classes?.[name];
  const functionEntry = api.functions?.[name];
  const aliasEntry = api.aliases?.[name];
  const entry = classEntry ?? functionEntry ?? aliasEntry;

  if (!entry) {
    return <div>Missing API entry for <code>{name}</code>.</div>;
  }

  if (!classEntry && !functionEntry && aliasEntry) {
    useInjectedToc(
      showRootHeading
        ? [{title: entry.name, id: rootAnchor(name), items: [], showWhenEmpty: true}]
        : []
    );
    return (
      <div>
        {showRootHeading ? (
          <HeadingLink level="h2" id={rootAnchor(name)}>
            {entry.name}
          </HeadingLink>
        ) : null}
        {showDocstring
          ? renderDocstring(entry.docstring, {classSymbol: name, docId: metadata?.id})
          : null}
        {entry.value ? (
          <SignatureBox text={entry.value}>
            {renderCodeExpression(entry.value, {
              api,
              classSymbol: name,
              docId: metadata?.id,
            })}
          </SignatureBox>
        ) : null}
      </div>
    );
  }

  const properties = entry.properties ?? [];
  const events = entry.events ?? [];
  const methods = entry.methods ?? [];
  const propertySummaries = properties.map((item) => ({
    name: item.name,
    kind: "property",
    summary: firstSentenceFromDocstring(item.docstring, item.docstring_sections),
  }));
  const eventSummaries = events.map((item) => ({
    name: item.name,
    kind: "event",
    summary: firstSentenceFromDocstring(item.docstring, item.docstring_sections),
  }));
  const methodSummaries = methods.map((item) => ({
    name: item.name,
    kind: "method",
    summary: firstSentenceFromDocstring(item.docstring, item.docstring_sections),
  }));

  const propertiesWithSectionId = properties.map((item) => ({
    ...item,
    __sectionId: sectionAnchor(name, "properties"),
  }));
  const eventsWithSectionId = events.map((item) => ({
    ...item,
    __sectionId: sectionAnchor(name, "events"),
  }));
  const methodsWithSectionId = methods.map((item) => ({
    ...item,
    __sectionId: sectionAnchor(name, "methods"),
  }));

  useInjectedToc(
    [
      ...(showRootHeading
        ? [{title: entry.name, id: rootAnchor(name), items: [], showWhenEmpty: true}]
        : []),
      ...(showMembers
        ? [
            {
              title: "Properties",
              id: sectionAnchor(name, "properties"),
              items: properties.map((item) => ({
                id: memberAnchor(name, item.name),
                kind: "property",
                label: item.name,
              })),
            },
            {
              title: "Events",
              id: sectionAnchor(name, "events"),
              items: events.map((item) => ({
                id: memberAnchor(name, item.name),
                kind: "event",
                label: item.name,
              })),
            },
            {
              title: "Methods",
              id: sectionAnchor(name, "methods"),
              items: methods.map((item) => ({
                id: memberAnchor(name, item.name),
                kind: "method",
                label: item.name,
              })),
            },
          ]
        : []),
    ]
  );

  return (
    <div>
      {showRootHeading ? (
        <HeadingLink level="h2" id={rootAnchor(name)}>
          {entry.name}
        </HeadingLink>
      ) : null}
      {showDocstring
        ? renderDocstring(entry.docstring, {classSymbol: name, docId: metadata?.id})
        : null}
      {image ? (
        <figure className="doc-screenshot-figure">
          <img
            alt={entry.name}
            className="doc-screenshot"
            src={resolveDocAssetUrl(image, metadata?.id)}
            style={{width: imageWidth}}
          />
          {imageCaption ? <figcaption>{imageCaption}</figcaption> : null}
        </figure>
      ) : null}
      {showBases && entry.bases?.length ? (
        <p>
          <strong>Inherits:</strong>{" "}
          {entry.bases.map((baseName, index) => {
            return (
              <React.Fragment key={baseName}>
                {index > 0 ? ", " : ""}
                <span className="crocodocs-inline-code">
                  {renderCodeExpression(baseName, {
                    api,
                    classSymbol: name,
                    docId: metadata?.id,
                  })}
                </span>
              </React.Fragment>
            );
          })}
        </p>
      ) : null}
      {showSummary ? (
        <div>
          <SummarySection title="Properties" items={propertySummaries} classSymbol={name} />
          <SummarySection title="Events" items={eventSummaries} classSymbol={name} />
          <SummarySection title="Methods" items={methodSummaries} classSymbol={name} />
        </div>
      ) : null}
      {showMembers ? (
        <>
          <Section
            title="Properties"
            items={propertiesWithSectionId}
            renderItem={(item) => renderAttribute(item, name, metadata?.id)}
          />
          <Section
            title="Events"
            items={eventsWithSectionId}
            renderItem={(item) => renderAttribute(item, name, metadata?.id)}
          />
          <Section
            title="Methods"
            items={methodsWithSectionId}
            renderItem={(item) => renderMethod(item, name, metadata?.id)}
          />
        </>
      ) : null}
    </div>
  );
}
