// Entry for the anchor widget: load the question bank, then the widget (src/widget-main/anchor.tsx).
import { renderWidget } from "@remnote/plugin-sdk";
import { gate } from "../drills/gate";

renderWidget(gate(() => import(/* webpackMode: "eager" */ "../widget-main/anchor")));
