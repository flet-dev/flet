import React from "react";
import clsx from "clsx";
import {ThemeClassNames, useWindowSize} from "@docusaurus/theme-common";
import {useDoc} from "@docusaurus/plugin-content-docs/client";
import DocItemPaginator from "@theme/DocItem/Paginator";
import DocVersionBanner from "@theme/DocVersionBanner";
import DocVersionBadge from "@theme/DocVersionBadge";
import DocItemFooter from "@theme/DocItem/Footer";
import DocItemTOCMobile from "@theme/DocItem/TOC/Mobile";
import DocItemTOCDesktop from "@theme/DocItem/TOC/Desktop";
import DocItemContent from "@theme/DocItem/Content";
import DocBreadcrumbs from "@theme/DocBreadcrumbs";
import ContentVisibility from "@theme/ContentVisibility";
import docManifest from "@site/.crocodocs/docs-manifest.json";

import styles from "./styles.module.css";

function hasCrocoDocsSymbols(metadata) {
  if (!metadata?.permalink) {
    return false;
  }
  const page = docManifest.pages.find((entry) => entry.route === metadata.permalink);
  return Boolean(page?.symbol_blocks?.length);
}

function CrocoDocsTOCDesktopPlaceholder() {
  return (
    <div className="thin-scrollbar theme-doc-toc-desktop">
      <ul className="table-of-contents table-of-contents__left-border" />
    </div>
  );
}

function useDocTOC() {
  const {frontMatter, metadata, toc} = useDoc();
  const windowSize = useWindowSize();
  const hidden = frontMatter.hide_table_of_contents;
  const hasStaticTOC = toc.length > 0;
  const hasCrocoDocsTOC = hasCrocoDocsSymbols(metadata);
  const canRender = !hidden && (hasStaticTOC || hasCrocoDocsTOC);

  const mobile = hasStaticTOC && canRender ? <DocItemTOCMobile /> : undefined;
  const desktop =
    canRender && (windowSize === "desktop" || windowSize === "ssr") ? (
      hasStaticTOC ? (
        <DocItemTOCDesktop />
      ) : (
        <CrocoDocsTOCDesktopPlaceholder />
      )
    ) : undefined;

  return {
    hidden,
    mobile,
    desktop,
  };
}

export default function DocItemLayout({children}) {
  const docTOC = useDocTOC();
  const {metadata} = useDoc();

  return (
    <div className="row">
      <div className={clsx("col", !docTOC.hidden && styles.docItemCol)}>
        <ContentVisibility metadata={metadata} />
        <DocVersionBanner />
        <div className={styles.docItemContainer}>
          <article>
            <DocBreadcrumbs />
            <DocVersionBadge />
            {docTOC.mobile}
            <DocItemContent>{children}</DocItemContent>
            <DocItemFooter />
          </article>
          <DocItemPaginator />
        </div>
      </div>
      {docTOC.desktop ? <div className="col col--3">{docTOC.desktop}</div> : null}
    </div>
  );
}
