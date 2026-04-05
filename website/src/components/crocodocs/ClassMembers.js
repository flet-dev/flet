import React from "react";

import ClassBlock from "./ClassBlock";

/**
 * Renders only the members section (properties, events, methods) of an API class.
 * Hides the docstring, base-class list, and summary table.
 */
export default function ClassMembers(props) {
  return (
    <ClassBlock
      {...props}
      showDocstring={false}
      showBases={false}
      showSummary={false}
    />
  );
}
