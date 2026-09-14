import React, {useCallback, useEffect, useMemo, useRef, useState} from "react";

import materialCodepoints from "@site/src/data/material-icon-codepoints.json";
import cupertinoCodepoints from "@site/src/data/cupertino-icon-codepoints.json";

import styles from "./styles.module.css";

const SETS = {
  material: {
    codepoints: materialCodepoints,
    fontClass: styles.glyphMaterial,
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
    // Cupertino names use _FILL/_CIRCLE/_SOLID rather than a consistent
    // four-style scheme, so there is no coherent facet to offer.
    variants: null,
  },
};

const STYLE_SUFFIXES = ["_OUTLINED", "_ROUNDED", "_SHARP"];

/** Return the `ft.`-prefixed expression a reader would paste into their app. */
function displaySymbol(symbol) {
  return symbol.replace(/^flet\./, "ft.");
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
 * Every tile is server-rendered, including its `id`, so that existing deep
 * links of the form `#flet.Icons.ARROW_UPWARD` keep resolving and the page
 * still says something useful without JavaScript.
 *
 * @param {string} name - Fully qualified symbol, e.g. `flet.Icons`.
 * @param {"material"|"cupertino"} set - Which icon set to render.
 */
export default function IconGallery({name, set = "material"}) {
  // Resolved before any hook runs: bailing out early here would change the
  // hook call order between renders.
  const config = SETS[set] ?? SETS.material;
  const symbol = displaySymbol(name);
  const entries = useMemo(() => Object.entries(config.codepoints), [config]);

  const gridRef = useRef(null);
  const [query, setQuery] = useState("");
  const [variant, setVariant] = useState(null);
  const [status, setStatus] = useState("");
  const [copied, setCopied] = useState(null);
  const [pendingAnchor, setPendingAnchor] = useState(null);

  /**
   * The tiles are built once and never re-rendered.
   *
   * At 8,825 tiles, re-rendering the list on every keystroke costs hundreds of
   * milliseconds, so filtering instead toggles `hidden` on the existing nodes
   * (see the effect below). Keeping this array referentially stable is what
   * stops React from touching them.
   */
  const tiles = useMemo(
    () =>
      entries.map(([iconName, codepoint]) => (
        <button
          key={iconName}
          id={`${name}.${iconName}`}
          type="button"
          className={styles.tile}
          tabIndex={-1}
          data-name={iconName}
          title={`${symbol}.${iconName}`}
        >
          <span aria-hidden="true" className={`${styles.glyph} ${config.fontClass}`}>
            {String.fromCodePoint(codepoint)}
          </span>
          <span className={styles.label}>{iconName}</span>
        </button>
      )),
    [entries, name, symbol, config]
  );

  /** Apply the current query and variant filter directly to the rendered tiles. */
  useEffect(() => {
    const grid = gridRef.current;
    if (!grid) {
      return;
    }

    const needle = query.trim().toLowerCase();
    let visible = 0;
    let firstVisible = null;

    for (const tile of grid.children) {
      const iconName = tile.dataset.name;
      let match = !needle || iconName.toLowerCase().includes(needle);
      if (match && variant !== null) {
        const suffix = STYLE_SUFFIXES.find((s) => iconName.endsWith(s)) ?? "";
        match = suffix === variant;
      }
      tile.hidden = !match;
      if (match) {
        visible += 1;
        if (!firstVisible) {
          firstVisible = tile;
        }
      }
      // Roving tabindex: the grid is a single tab stop, and arrow keys move
      // within it. Without this every tile would be its own stop.
      tile.tabIndex = -1;
    }

    if (firstVisible) {
      firstVisible.tabIndex = 0;
    }
    setStatus(`${visible.toLocaleString()} of ${entries.length.toLocaleString()} icons`);
  }, [query, variant, entries, tiles]);

  /**
   * Honour an incoming `#flet.Icons.NAME` deep link.
   *
   * The tile ids are real, so the browser scrolls to one on its own - but
   * filtering the grid down to the match then shortens the page out from under
   * that scroll position, which is why `pendingAnchor` re-scrolls afterwards.
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
        setPendingAnchor(iconName);
      }
    }

    applyHash();
    window.addEventListener("hashchange", applyHash);
    return () => window.removeEventListener("hashchange", applyHash);
  }, [name]);

  /** Bring a deep-linked tile back into view once filtering has resized the page. */
  useEffect(() => {
    if (!pendingAnchor) {
      return;
    }
    const tile = gridRef.current?.querySelector(
      `[data-name="${CSS.escape(pendingAnchor)}"]`
    );
    if (tile && !tile.hidden) {
      tile.scrollIntoView({block: "center"});
      tile.focus({preventScroll: true});
    }
    setPendingAnchor(null);
  }, [pendingAnchor, status]);

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
      setStatus(ok ? `Copied ${text}` : `Could not copy - the name is ${text}`);
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

  /** Move focus between visible tiles with the arrow keys, Home and End. */
  const onGridKeyDown = useCallback((event) => {
    const grid = gridRef.current;
    const current = event.target.closest("button[data-name]");
    if (!grid || !current) {
      return;
    }

    const shown = Array.from(grid.children).filter((tile) => !tile.hidden);
    const index = shown.indexOf(current);
    if (index === -1) {
      return;
    }

    // One row's worth of tiles, so Up/Down move vertically in the wrapped grid.
    const perRow = Math.max(
      1,
      shown.filter((tile) => tile.offsetTop === shown[0].offsetTop).length
    );

    const moves = {
      ArrowRight: index + 1,
      ArrowLeft: index - 1,
      ArrowDown: index + perRow,
      ArrowUp: index - perRow,
      Home: 0,
      End: shown.length - 1,
    };

    const next = moves[event.key];
    if (next === undefined) {
      return;
    }

    event.preventDefault();
    const target = shown[Math.min(Math.max(next, 0), shown.length - 1)];
    if (target) {
      current.tabIndex = -1;
      target.tabIndex = 0;
      target.focus();
      target.scrollIntoView({block: "nearest"});
    }
  }, []);

  const inputId = `${set}-icon-search`;

  return (
    <div className={styles.gallery}>
      <div className={styles.toolbar}>
        <div className={styles.searchField}>
          <label className={styles.searchLabel} htmlFor={inputId}>
            Search {entries.length.toLocaleString()} icons
          </label>
          <input
            id={inputId}
            className={styles.search}
            type="search"
            value={query}
            autoComplete="off"
            placeholder="delete, arrow, wifi…"
            onChange={(event) => setQuery(event.target.value)}
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
        {status}
      </div>

      <div
        ref={gridRef}
        className={styles.grid}
        onClick={onGridClick}
        onKeyDown={onGridKeyDown}
      >
        {tiles}
      </div>

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
