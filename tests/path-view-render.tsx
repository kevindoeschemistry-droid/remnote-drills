// Mounts the Path tab in a stand-in browser with a fake RemNote and fails on any render error.
// Three states: never built, built before framework choice existed, built with a saved choice.
import { JSDOM } from "jsdom";
const dom = new JSDOM("<!doctype html><html><body><div id='root'></div></body></html>", { pretendToBeVisual: true });
const g: any = globalThis;
g.window = dom.window; g.document = dom.window.document; g.navigator = dom.window.navigator;
g.HTMLElement = dom.window.HTMLElement; g.Node = dom.window.Node; g.requestAnimationFrame = (f: any) => setTimeout(f, 0); g.cancelAnimationFrame = clearTimeout;

const Module = require("module");
const store: Record<string, any> = {};
const known: any = {
  storage: {
    getSynced: async (k: string) => store[k] ?? null, // RemNote answers null, not undefined, for a key never set
    setSynced: async (k: string, v: any) => void (store[k] = v),
    getLocal: async () => undefined,
    setLocal: async () => {},
  },
  rem: { findOne: async () => undefined },
};
// anything else the widgets call on RemNote (settings, toasts, queue…) resolves to undefined
const namespace = (real: any = {}) => new Proxy(real, { get: (t, k) => (k in t ? t[k] : async () => undefined) });
const plugin: any = new Proxy(known, { get: (t, k) => namespace(t[k as string]) });
const realLoad = Module._load;
Module._load = function (request: string, ...rest: any[]) {
  if (request === "@remnote/plugin-sdk") return { usePlugin: () => plugin, QueueInteractionScore: {}, renderWidget: () => {}, AppEvents: {}, WidgetLocation: {} };
  if (/\.css$/.test(request)) return {};
  return realLoad.call(this, request, ...rest);
};

const React = require("react");
const ReactDOM = require("react-dom");
const { act } = require("react-dom/test-utils");
const { PathView } = require("../src/components/PathView");

const fail = (m: string) => { console.log("FAIL:", m); process.exitCode = 1; };
const errors: string[] = [];
const origError = console.error;
console.error = (...a: any[]) => { errors.push(a.map(String).join(" ").slice(0, 300)); };

async function mount(label: string, seed: Record<string, any>, expect: string[]) {
  for (const k of Object.keys(store)) delete store[k];
  Object.assign(store, seed);
  errors.length = 0;
  const root = document.getElementById("root")!;
  try {
    await act(async () => { ReactDOM.render(React.createElement(PathView), root); });
    await act(async () => { await new Promise((r) => setTimeout(r, 400)); });
  } catch (e: any) {
    fail(`${label}: threw ${String(e?.stack ?? e).slice(0, 600)}`);
  }
  const html = root.innerHTML;
  if (html.length < 200) fail(`${label}: rendered almost nothing (${html.length} characters)`);
  for (const want of expect) if (!html.includes(want)) fail(`${label}: missing "${want}"`);
  if (errors.length) fail(`${label}: console errors: ${errors.slice(0, 3).join(" | ")}`);
  console.log(`${label}: ${html.length} characters`);
  ReactDOM.unmountComponentAtNode(root);
}

(async () => {
  await mount("never built", {}, ["Build the Library", "Heat Transfer", "cards"]);
  await mount("built before the choice existed", { "library.root": "r1", "library.signature": "old" }, ["Update the Library", "Drill cards:"]);
  await mount("built with a saved choice", { "library.root": "r1", "library.cardFrameworks": ["heat-transfer"] }, ["Drill cards: 1 of"]);
  console.error = origError;
  process.exit(process.exitCode ?? 0);
})();
