import React from "react";

import ClassBlock from "./ClassBlock";

/**
 * Renders a full API class block (docstring, bases, summary, and members).
 * Passes all props directly to ClassBlock with no overrides.
 */
export default function ClassAll(props) {
  return <ClassBlock {...props} />;
}
