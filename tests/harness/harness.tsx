import React from "react";
import ReactDOM from "react-dom";
import { DrillPanel } from "../../src/components/DrillPanel";
import { LIVE_SKILLS } from "../../src/drills/skills";
import "../../src/drills.css";
const only = new URLSearchParams(location.search).get("skills");
const ids = only ? only.split(",") : LIVE_SKILLS.map((s) => s.id);
ReactDOM.render(
  <div style={{ maxWidth: 680, margin: "16px auto", fontFamily: "system-ui, sans-serif" }}>
    {ids.map((s) => <DrillPanel key={s} skill={s} mode="card" />)}
  </div>,
  document.getElementById("root")
);
