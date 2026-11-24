// Entry for the drill_session widget: load the question bank, then the widget (src/widget-main/drill_session.tsx).
import { renderWidget } from "@remnote/plugin-sdk";
import { gate } from "../drills/gate";

renderWidget(gate(() => import(/* webpackMode: "eager" */ "../widget-main/drill_session")));
