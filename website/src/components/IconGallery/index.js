import React, {useCallback, useEffect, useMemo, useRef, useState} from "react";

import Head from "@docusaurus/Head";

import materialCodepoints from "@site/src/data/material-icon-codepoints.json";
import cupertinoCodepoints from "@site/src/data/cupertino-icon-codepoints.json";

// Imported rather than hard-coded so the preload below points at the
// content-hashed URL webpack actually emits, not a path that no longer exists.
import materialFontUrl from "@site/src/fonts/MaterialIcons-Regular.woff2";
import cupertinoFontUrl from "@site/src/fonts/CupertinoIcons.woff2";

import styles from "./styles.module.css";

const SETS = {
  material: {
    codepoints: materialCodepoints,
    fontClass: styles.glyphMaterial,
    fontUrl: materialFontUrl,
    // Flutter exposes each Material icon in four styles, distinguished by a
    // name suffix. "Filled" is the unsuffixed base name, so it is matched by
    // elimination rather than by a suffix of its own.
    variants: [
      {label: "All", suffix: null},
      {label: "Filled", suffix: ""},
      {label: "Outlined", suffix: "_OUTLINED"},
      {label: "Rounded", suffix: "_ROUNDED"},
      {label: "Sharp", suffix: "_SHARP"},
    ],
  },
  cupertino: {
    codepoints: cupertinoCodepoints,
    fontClass: styles.glyphCupertino,
    fontUrl: cupertinoFontUrl,
    // Cupertino names use _FILL/_CIRCLE/_SOLID rather than a consistent
    // four-style scheme, so there is no coherent facet to offer.
    variants: null,
  },
};

const STYLE_SUFFIXES = ["_OUTLINED", "_ROUNDED", "_SHARP"];

/**
 * How many tiles exist in the document before the reader scrolls.
 *
 * Rendering the whole Material set costs 2.5 MB of HTML and 27,000 DOM nodes,
 * which is ~123ms of parsing on a desktop and several times that on a phone -
 * all of it before anything can paint. A few screens' worth costs ~70 KB, and
 * the rest arrives as it is needed. Searching still covers every icon: the
 * filter runs over the full name list, not over what happens to be rendered.
 */
const BATCH = 300;

/** Return the `ft.`-prefixed expression a reader would paste into their app. */
function displaySymbol(symbol) {
  return symbol.replace(/^flet\./, "ft.");
}

/**
 * Group a count with thousands separators, identically on both sides.
 *
 * Deliberately not `toLocaleString()` with no locale: that follows the build
 * machine on the server and the reader's browser on the client, so `8,825`
 * server-rendered against `8.825` in a de-DE browser is a hydration mismatch.
 * The site ships no translations, so a fixed separator is also what it wants.
 */
function formatCount(n) {
  return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/** Copy via the legacy selection API, for contexts that refuse the async one. */
function copyViaExecCommand(text) {
  const field = document.createElement("textarea");
  field.value = text;
  field.setAttribute("readonly", "");
  field.style.position = "fixed";
  field.style.opacity = "0";
  document.body.appendChild(field);
  try {
    field.select();
    return document.execCommand("copy");
  } catch {
    return false;
  } finally {
    field.remove();
  }
}

/**
 * Renders a searchable gallery of every icon in a Flet icon set, drawing each
 * one with the same font the Flet client uses.
 *
 * @param {string} name - Fully qualified symbol, e.g. `flet.Icons`.
 * @param {"material"|"cupertino"} set - Which icon set to render.
 */
export default function IconGallery({name, set = "material"}) {
  // Resolved before any hook runs: bailing out early here would change the
  // hook call order between renders.
  const config = SETS[set] ?? SETS.material;
  const symbol = displaySymbol(name);
  const codepoints = config.codepoints;
  const allNames = useMemo(() => Object.keys(codepoints), [codepoints]);

  const gridRef = useRef(null);
  const sentinelRef = useRef(null);
  const [query, setQuery] = useState("");
  const [variant, setVariant] = useState(null);
  const [limit, setLimit] = useState(BATCH);
  const [copied, setCopied] = useState(null);
  const [pendingAnchor, setPendingAnchor] = useState(null);
  // Set only by a deep link. A link to `#flet.Icons.ADD` means that one icon,
  // but as a search term "ADD" is a substring of 207 others, so the filter has
  // to match exactly until the reader edits the box.
  const [exactName, setExactName] = useState(null);

  const matches = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return allNames.filter((iconName) => {
      if (exactName) {
        return iconName === exactName;
      }
      if (needle && !iconName.toLowerCase().includes(needle)) {
        return false;
      }
      if (variant === null) {
        return true;
      }
      return (STYLE_SUFFIXES.find((s) => iconName.endsWith(s)) ?? "") === variant;
    });
  }, [allNames, query, variant, exactName]);

  // A new filter means a new list, so the window starts again from the top.
  useEffect(() => {
    setLimit(BATCH);
  }, [query, variant, exactName]);

  const shown = matches.length > limit ? matches.slice(0, limit) : matches;

  /** Grow the window as the sentinel below the grid comes into view. */
  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel || limit >= matches.length || !window.IntersectionObserver) {
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          setLimit((current) => current + BATCH);
        }
      },
      // Start fetching a screen early so scrolling does not stall at the seam.
      {rootMargin: "600px"}
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [limit, matches.length]);

  /**
   * Honour an incoming `#flet.Icons.NAME` deep link.
   *
   * `hashchange` matters as much as mount: the docs are a single-page app, so
   * following a link to a different icon on this same page never remounts.
   */
  useEffect(() => {
    const prefix = `${name}.`;

    function applyHash() {
      const hash = decodeURIComponent(window.location.hash.replace(/^#/, ""));
      if (hash.startsWith(prefix)) {
        const iconName = hash.slice(prefix.length);
        setQuery(iconName);
        setExactName(iconName);
        setPendingAnchor(iconName);
      }
    }

    applyHash();
    window.addEventListener("hashchange", applyHash);
    return () => window.removeEventListener("hashchange", applyHash);
  }, [name]);

  /**
   * Scroll a deep-linked tile into view once it has actually been rendered.
   *
   * The browser cannot do this itself: an icon outside the first window has no
   * element to scroll to at the moment the hash is read.
   */
  useEffect(() => {
    if (!pendingAnchor) {
      return;
    }
    const tile = gridRef.current?.querySelector(
      `[data-name="${CSS.escape(pendingAnchor)}"]`
    );
    if (tile) {
      tile.scrollIntoView({block: "center"});
      tile.focus({preventScroll: true});
      setPendingAnchor(null);
    }
  }, [pendingAnchor, shown]);

  /**
   * Copy an icon's name, and say what happened either way.
   *
   * The async clipboard API is refused outright in some contexts (a denied
   * permission, an embedded frame), so a failure here is ordinary rather than
   * exceptional. Falling back to `execCommand` covers most of it, and the
   * toast shows the full name regardless - a reader who cannot be given the
   * string can at least read it.
   */
  const copy = useCallback(
    async (iconName) => {
      const text = `${symbol}.${iconName}`;
      let ok = false;
      try {
        await navigator.clipboard.writeText(text);
        ok = true;
      } catch {
        ok = copyViaExecCommand(text);
      }
      setCopied({name: iconName, ok});
      window.setTimeout(() => setCopied(null), 2000);
    },
    [symbol]
  );

  const onGridClick = useCallback(
    (event) => {
      const tile = event.target.closest("button[data-name]");
      if (tile) {
        copy(tile.dataset.name);
      }
    },
    [copy]
  );

  /** Move focus between tiles with the arrow keys, Home and End. */
  const onGridKeyDown = useCallback((event) => {
    const grid = gridRef.current;
    const current = event.target.closest("button[data-name]");
    if (!grid || !current) {
      return;
    }

    const tiles = Array.from(grid.querySelectorAll("button[data-name]"));
    const index = tiles.indexOf(current);
    if (index === -1) {
      return;
    }

    // One row's worth of tiles, so Up/Down move vertically in the wrapped grid.
    const perRow = Math.max(
      1,
      tiles.filter((tile) => tile.offsetTop === tiles[0].offsetTop).length
    );

    const next = {
      ArrowRight: index + 1,
      ArrowLeft: index - 1,
      ArrowDown: index + perRow,
      ArrowUp: index - perRow,
      Home: 0,
      End: tiles.length - 1,
    }[event.key];

    if (next === undefined) {
      return;
    }

    event.preventDefault();
    const target = tiles[Math.min(Math.max(next, 0), tiles.length - 1)];
    if (target) {
      current.tabIndex = -1;
      target.tabIndex = 0;
      target.focus();
      target.scrollIntoView({block: "nearest"});
    }
  }, []);

  const inputId = `${set}-icon-search`;
  const total = allNames.length;

  return (
    <div className={styles.gallery}>
      {/* `font-display: block` means no glyph is drawn until this arrives, and
          without a preload the browser only discovers it after the stylesheet
          has been parsed and the first tiles laid out. */}
      <Head>
        <link
          rel="preload"
          as="font"
          type="font/woff2"
          href={config.fontUrl}
          crossOrigin="anonymous"
        />
      </Head>

      <div className={styles.toolbar}>
        <div className={styles.searchField}>
          <label className={styles.searchLabel} htmlFor={inputId}>
            Search {formatCount(total)} icons
          </label>
          <input
            id={inputId}
            className={styles.search}
            type="search"
            value={query}
            autoComplete="off"
            placeholder="delete, arrow, wifi…"
            onChange={(event) => {
              setExactName(null);
              setQuery(event.target.value);
            }}
          />
        </div>

        {config.variants && (
          <div className={styles.chips} role="group" aria-label="Icon style">
            {config.variants.map(({label, suffix}) => (
              <button
                key={label}
                type="button"
                className={styles.chip}
                aria-pressed={variant === suffix}
                onClick={() => setVariant(suffix)}
              >
                {label}
              </button>
            ))}
          </div>
        )}
      </div>

      <p className={styles.hint}>
        Click an icon to copy its <code>{symbol}</code> name.
      </p>

      <div className={styles.status} role="status" aria-live="polite">
        {formatCount(matches.length)} {matches.length === 1 ? "icon" : "icons"}
      </div>

      <div
        ref={gridRef}
        className={styles.grid}
        onClick={onGridClick}
        onKeyDown={onGridKeyDown}
      >
        {shown.map((iconName, i) => (
          <button
            key={iconName}
            id={`${name}.${iconName}`}
            type="button"
            className={styles.tile}
            // Roving tabindex: the grid is a single tab stop and the arrow keys
            // move within it, rather than 8,825 separate stops.
            tabIndex={i === 0 ? 0 : -1}
            data-name={iconName}
            title={`${symbol}.${iconName}`}
          >
            <span aria-hidden="true" className={`${styles.glyph} ${config.fontClass}`}>
              {String.fromCodePoint(codepoints[iconName])}
            </span>
            <span className={styles.label}>{iconName}</span>
          </button>
        ))}
      </div>

      {matches.length === 0 && (
        <p className={styles.empty}>
          No icon matches <code>{query}</code>.
        </p>
      )}

      {limit < matches.length && (
        /* Also a button, not just an IntersectionObserver target: a sentinel
           that only reacts to scrolling strands anyone whose browser does not
           fire the observer, and gives keyboard users nothing to activate. */
        <button
          ref={sentinelRef}
          type="button"
          className={styles.sentinel}
          onClick={() => setLimit((current) => current + BATCH)}
        >
          Showing {formatCount(shown.length)} of {formatCount(matches.length)} — show
          more
        </button>
      )}

      {copied && (
        <div className={`${styles.toast} ${copied.ok ? "" : styles.toastError}`}>
          {copied.ok ? "Copied " : "Copy blocked — "}
          <code>
            {symbol}.{copied.name}
          </code>
        </div>
      )}
    </div>
  );
}
