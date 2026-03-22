import React, {useEffect} from "react";
import Heading from "@theme/Heading";
import CodeBlock from "@theme/CodeBlock";
import {useDoc} from "@docusaurus/plugin-content-docs/client";

import {
  firstSentenceFromDocstring,
  getApiData,
  normalizeAnchor,
  renderDocstring,
  renderDocstringSections,
  renderInlineMarkdown,
  resolveDocAssetUrl,
} from "./utils";

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

function SignatureBox({children}) {
  return <CodeBlock language="python">{children}</CodeBlock>;
}

function Section({title, items, renderItem}) {
  if (!items || items.length === 0) {
    return null;
  }

  const sectionId = normalizeAnchor(title.toLowerCase());
  return (
    <section>
      <HeadingLink level="h2" id={sectionId}>
        {title}
      </HeadingLink>
      {items.map(renderItem)}
    </section>
  );
}

function useInjectedToc(sectionGroups) {
  useEffect(() => {
    const tocRoot = document.querySelector("ul.table-of-contents");
    if (!tocRoot) {
      return undefined;
    }

    tocRoot
      .querySelectorAll("[data-crocodocs-toc='true']")
      .forEach((node) => node.remove());

    const created = [];
    for (const group of sectionGroups) {
      if (!group.items.length) {
        continue;
      }

      const top = document.createElement("li");
      top.className = "table-of-contents__list-item table-of-contents__list-item--nested generated-crocodocs-toc";
      top.dataset.crocodocsToc = "true";

      const link = document.createElement("a");
      link.className = "table-of-contents__link toc-highlight";
      link.href = `#${group.id}`;
      link.textContent = group.title;
      top.appendChild(link);

      const nested = document.createElement("ul");
      nested.className = "table-of-contents__sublist";
      for (const item of group.items) {
        const nestedItem = document.createElement("li");
        nestedItem.className = "table-of-contents__list-item generated-crocodocs-toc";
        nestedItem.dataset.crocodocsToc = "true";

        const nestedLink = document.createElement("a");
        nestedLink.className = "table-of-contents__link toc-highlight";
        nestedLink.href = `#${item.id}`;
        nestedLink.textContent = item.label;
        nestedItem.appendChild(nestedLink);
        nested.appendChild(nestedItem);
        created.push(nestedItem);
      }

      top.appendChild(nested);
      tocRoot.appendChild(top);
      created.push(top);
    }

    return () => {
      created.forEach((node) => node.remove());
    };
  }, [sectionGroups]);
}

function renderMemberHeading(item) {
  const id = normalizeAnchor(item.name);
  return (
    <HeadingLink level="h3" id={id}>
      <span className="crocodocs-member-heading">
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
  return (
    <div key={item.name}>
      {renderMemberHeading(item)}
      {item.type ? (
        <SignatureBox>
          {item.name}: {item.type}
          {item.default != null ? ` = ${item.default}` : ""}
        </SignatureBox>
      ) : null}
      {renderDocstring(item.docstring, {classSymbol, docId})}
    </div>
  );
}

function renderMethod(item, classSymbol, docId) {
  return (
    <div key={item.name}>
      {renderMemberHeading(item)}
      <SignatureBox>{item.signature ?? item.name}</SignatureBox>
      {renderDocstringSections(item.docstring_sections, {classSymbol, docId}) ??
        renderDocstring(item.docstring, {classSymbol, docId})}
    </div>
  );
}

function resolveBaseHref(api, classSymbol, baseName) {
  if (!baseName) {
    return null;
  }
  if (baseName.includes(".")) {
    return api.xref_map?.[baseName] ?? null;
  }

  const packagePrefix = classSymbol.includes(".")
    ? `${classSymbol.split(".").slice(0, -1).join(".")}.`
    : "";
  return api.xref_map?.[`${packagePrefix}${baseName}`] ?? null;
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
            <a href={`#${normalizeAnchor(item.name)}`}>
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
  showDocstring = true,
  showBases = true,
  showSummary = true,
  showMembers = true,
  image,
  imageCaption,
  imageWidth = "20%",
}) {
  const {metadata} = useDoc();
  const api = getApiData();
  const entry = api.classes?.[name] ?? api.functions?.[name];

  if (!entry) {
    return <div>Missing API entry for <code>{name}</code>.</div>;
  }

  const properties = entry.properties ?? [];
  const events = entry.events ?? [];
  const methods = entry.methods ?? [];
  const propertySummaries = properties.map((item) => ({
    name: item.name,
    summary: firstSentenceFromDocstring(item.docstring, item.docstring_sections),
  }));
  const eventSummaries = events.map((item) => ({
    name: item.name,
    summary: firstSentenceFromDocstring(item.docstring, item.docstring_sections),
  }));
  const methodSummaries = methods.map((item) => ({
    name: item.name,
    summary: firstSentenceFromDocstring(item.docstring, item.docstring_sections),
  }));

  useInjectedToc(
    showMembers
      ? [
          {
            title: "Properties",
            id: normalizeAnchor("properties"),
            items: properties.map((item) => ({
              id: normalizeAnchor(item.name),
              label: item.name,
            })),
          },
          {
            title: "Events",
            id: normalizeAnchor("events"),
            items: events.map((item) => ({
              id: normalizeAnchor(item.name),
              label: item.name,
            })),
          },
          {
            title: "Methods",
            id: normalizeAnchor("methods"),
            items: methods.map((item) => ({
              id: normalizeAnchor(item.name),
              label: item.name,
            })),
          },
        ]
      : []
  );

  return (
    <div>
      {showDocstring
        ? renderDocstring(entry.docstring, {classSymbol: name, docId: metadata?.id})
        : null}
      {showBases && entry.bases?.length ? (
        <p>
          <strong>Inherits:</strong>{" "}
          {entry.bases.map((baseName, index) => {
            const href = resolveBaseHref(api, name, baseName);
            return (
              <React.Fragment key={baseName}>
                {index > 0 ? ", " : ""}
                {href ? (
                  <a href={href}>
                    <code>{baseName}</code>
                  </a>
                ) : (
                  <code>{baseName}</code>
                )}
              </React.Fragment>
            );
          })}
        </p>
      ) : null}
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
            items={properties}
            renderItem={(item) => renderAttribute(item, name, metadata?.id)}
          />
          <Section
            title="Events"
            items={events}
            renderItem={(item) => renderAttribute(item, name, metadata?.id)}
          />
          <Section
            title="Methods"
            items={methods}
            renderItem={(item) => renderMethod(item, name, metadata?.id)}
          />
        </>
      ) : null}
    </div>
  );
}
