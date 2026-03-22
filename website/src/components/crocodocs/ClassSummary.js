import React from "react";

import ClassBlock from "./ClassBlock";

export default function ClassSummary(props) {
  return <ClassBlock {...props} showMembers={false} />;
}
