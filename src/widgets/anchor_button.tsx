// Entry for the anchor_button widget: load the question bank, then the widget (src/widget-main/anchor_button.tsx).
import { renderWidget } from "@remnote/plugin-sdk";
import { gate } from "../drills/gate";

renderWidget(gate(() => import(/* webpackMode: "eager" */ "../widget-main/anchor_button")));
