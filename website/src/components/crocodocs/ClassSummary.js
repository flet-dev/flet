import React from "react";

import ClassBlock from "./ClassBlock";

/**
 * Renders the docstring, base-class list, and member summary table for an API class.
 * Hides the full per-member detail sections.
 */
export default function ClassSummary(props) {
  return <ClassBlock {...props} showMembers={false} />;
}
