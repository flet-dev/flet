import React from "react";

import ClassBlock from "./ClassBlock";

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
