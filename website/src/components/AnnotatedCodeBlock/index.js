import React, { useEffect, useRef, useState } from "react";
import CodeBlock from "@theme/CodeBlock";
import styles from "./styles.module.css";

const MARKER_SVG =
  '<svg width="8" height="8" viewBox="0 0 10 10"><path d="M5 1v8M1 5h8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';

function injectMarkers(container, annotations, markerClass, onClickMarker) {
  // Remove any existing markers first
  container.querySelectorAll(`.${markerClass}`).forEach((el) => el.remove());

  const codeEl = container.querySelector("code");
  if (!codeEl) return;

  const lines = codeEl.querySelectorAll(".token-line");

  Object.entries(annotations).forEach(([num, { line }]) => {
    const lineEl = lines[line];
    if (!lineEl) return;

    const marker = document.createElement("button");
    marker.className = markerClass;
    marker.type = "button";
    marker.innerHTML = MARKER_SVG;
    marker.setAttribute("aria-label", `Annotation ${num}`);
    marker.dataset.annotationNum = num;
    marker.addEventListener("click", (e) => {
      e.stopPropagation();
      onClickMarker(num, marker);
    });

    const br = lineEl.querySelector("br");
    if (br) {
      lineEl.insertBefore(marker, br);
    } else {
      lineEl.appendChild(marker);
    }
  });
}

export default function AnnotatedCodeBlock({
  code,
  lang,
  title,
  annotations: annotationsJson,
}) {
  const containerRef = useRef(null);
  const [activeAnnotation, setActiveAnnotation] = useState(null);
  const [tooltipStyle, setTooltipStyle] = useState({});
  const annotationsRef = useRef(null);

  if (annotationsRef.current === null) {
    annotationsRef.current =
      typeof annotationsJson === "string"
        ? JSON.parse(annotationsJson)
        : annotationsJson || {};
  }
  const annotations = annotationsRef.current;

  const handleMarkerClick = (num, markerEl) => {
    const container = containerRef.current;
    if (!container) return;

    const containerRect = container.getBoundingClientRect();
    const markerRect = markerEl.getBoundingClientRect();

    setActiveAnnotation((prev) => {
      if (prev === num) return null;
      setTooltipStyle({
        top: markerRect.bottom - containerRect.top + 6,
        left: markerRect.left - containerRect.left,
      });
      return num;
    });
  };

  // Close tooltip when clicking outside
  useEffect(() => {
    if (activeAnnotation === null) return;

    function handleClick(e) {
      const isMarker =
        e.target.closest && e.target.closest(`.${styles.marker}`);
      const tooltip = containerRef.current?.querySelector(
        `.${styles.tooltip}`,
      );
      const isInTooltip = tooltip && tooltip.contains(e.target);
      if (!isMarker && !isInTooltip) {
        setActiveAnnotation(null);
      }
    }
    document.addEventListener("click", handleClick);
    return () => document.removeEventListener("click", handleClick);
  }, [activeAnnotation]);

  // Inject markers after hydration, and re-inject if DOM changes
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const doInject = () =>
      injectMarkers(
        container,
        annotations,
        styles.marker,
        handleMarkerClick,
      );

    // Initial injection after a tick (CodeBlock needs to render)
    const timer = setTimeout(doInject, 50);

    // Re-inject if React re-renders the CodeBlock (hydration, tab switch, etc.)
    const observer = new MutationObserver(() => {
      // Only re-inject if markers are missing
      if (!container.querySelector(`.${styles.marker}`)) {
        doInject();
      }
    });
    observer.observe(container, { childList: true, subtree: true });

    return () => {
      clearTimeout(timer);
      observer.disconnect();
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const activeData = activeAnnotation
    ? annotations[activeAnnotation]
    : null;

  return (
    <div ref={containerRef} className={styles.wrapper}>
      <CodeBlock language={lang} title={title}>
        {code}
      </CodeBlock>
      {activeData && (
        <div
          className={styles.tooltip}
          style={tooltipStyle}
          dangerouslySetInnerHTML={{ __html: activeData.html }}
        />
      )}
    </div>
  );
}
