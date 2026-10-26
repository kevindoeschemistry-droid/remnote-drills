// Minimal stand-in for @remnote/plugin-sdk so the drill UI can be rendered in a plain browser page.
const store: Record<string, any> = {};
const plugin = {
  settings: { getSetting: async () => undefined },
  storage: {
    getSynced: async (k: string) => store[k],
    setSynced: async (k: string, v: any) => void (store[k] = v),
    getLocal: async (k: string) => store["l:" + k],
    setLocal: async (k: string, v: any) => void (store["l:" + k] = v),
  },
  queue: { rateCurrentCard: async (s: number) => console.log("rate", s) },
  app: { toast: async (m: string) => console.log("toast", m) },
};
export const usePlugin = () => plugin;
export enum QueueInteractionScore { AGAIN = 0, HARD = 0.5, GOOD = 1, EASY = 1.5 }
export enum BuiltInPowerupCodes { UploadedFile = "f", PDFHighlight = "n" }
import * as React_ from "react";
import * as ReactDOM_ from "react-dom";
/** Renders a widget into #root, so a widget file can be previewed on its own. */
export const renderWidget = (C: any) => ReactDOM_.render(React_.createElement(C), document.getElementById("root"));
