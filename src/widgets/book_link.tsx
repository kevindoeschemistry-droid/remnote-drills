// Entry for the book_link widget: load the question bank, then the widget (src/widget-main/book_link.tsx).
import { renderWidget } from "@remnote/plugin-sdk";
import { gate } from "../drills/gate";

renderWidget(gate(() => import(/* webpackMode: "eager" */ "../widget-main/book_link")));
