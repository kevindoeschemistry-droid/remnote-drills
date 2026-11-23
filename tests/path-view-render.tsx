// Mounts the Path tab in a stand-in browser with a fake RemNote and fails on any render error.
// States: never built, built before framework choice existed, built with a saved choice, and an old saved choice.
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
const { DRILLED_FRAMEWORKS, DEFAULT_CARD_FRAMEWORKS } = require("../src/drills/library-path");
const ReactDOM = require("react-dom");
const { act } = require("react-dom/test-utils");
const { PathView } = require("../src/components/PathView");

const fail = (m: string) => { console.log("FAIL:", m); process.exitCode = 1; };
const errors: string[] = [];
const origError = console.error;
console.error = (...a: any[]) => { errors.push(a.map(String).join(" ").slice(0, 300)); };

const { WarmMix } = require("../src/components/WarmMix");
const { PATH_LOS } = require("../src/drills/library-path");
let View: any = PathView;
let local: Record<string, any> = {};
known.storage.getLocal = async (k: string) => local[k];

async function mount(label: string, seed: Record<string, any>, expect: string[], absent: string[] = []) {
  for (const k of Object.keys(store)) delete store[k];
  Object.assign(store, seed);
  errors.length = 0;
  const root = document.getElementById("root")!;
  try {
    await act(async () => { ReactDOM.render(React.createElement(View), root); });
    await act(async () => { await new Promise((r) => setTimeout(r, 400)); });
  } catch (e: any) {
    fail(`${label}: threw ${String(e?.stack ?? e).slice(0, 600)}`);
  }
  const html = root.innerHTML;
  if (html.length < 200) fail(`${label}: rendered almost nothing (${html.length} characters)`);
  for (const want of expect) if (!html.includes(want)) fail(`${label}: missing "${want}"`);
  for (const not of absent) if (html.includes(not)) fail(`${label}: should not show "${not}"`);
  if (errors.length) fail(`${label}: console errors: ${errors.slice(0, 3).join(" | ")}`);
  console.log(`${label}: ${html.length} characters`);
  ReactDOM.unmountComponentAtNode(root);
}

(async () => {
  await mount("never built", {}, ["Build the Library", "Heat Transfer", "cards"]);
  await mount("built before the choice existed", { "library.root": "r1", "library.signature": "old" }, ["Update the Library", "Drill cards:"]);
  const drilledIds = DRILLED_FRAMEWORKS.map((f) => f.id);
  await mount("built with a saved choice", { "library.root": "r1", "library.cardFrameworks": ["heat-transfer"], "library.cardFrameworksSeen": drilledIds }, ["Drill cards: 1 of"]);
  // a choice saved before the plugin recorded what was on offer: frameworks other than school maths count as new and are on
  await mount("an old saved choice", { "library.root": "r1", "library.cardFrameworks": ["heat-transfer"] }, [`Drill cards: ${DEFAULT_CARD_FRAMEWORKS.length} of`]);
  // objectives without drills are hidden until asked for: no empty tracks, no "no drills" dead end
  const firstUndrilledMath = PATH_LOS.find((l: any) => l.fw.track === "math" && !l.drills.length) ?? PATH_LOS.find((l: any) => !l.drills.length);
  const known0: Record<string, string> = {};
  for (const l of PATH_LOS) { if (l === firstUndrilledMath) break; known0[l.code] = "known"; }
  local = { "path.track": firstUndrilledMath.fw.track };
  await mount("undrilled hidden", { "library.root": "r1", "path.mastery": known0 }, ["objectives without drills", "warm"], ["No drills for this objective yet", "Athletics", "mastered"]);
  local = { "path.showUndrilled": true, "path.track": firstUndrilledMath.fw.track };
  await mount("whole map shown", { "library.root": "r1", "path.mastery": known0 }, ["Hide objectives without drills", "No drills for this objective yet", "Athletics"]);
  local = {};

  View = WarmMix;
  await mount("warm mix, nothing warm", {}, ["Nothing is warm yet"]);
  const lo = PATH_LOS.find((l: any) => l.drills.length);
  await mount("warm mix, one cleared and one known", {
    [`odeDrill.progress.lo:${lo.code}`]: { consecutive: 5, cleared: true, attempts: 12, correct: 11, lastPracticed: Date.now() - 3 * 86400000 },
  }, ["Warm-up mix", "1 warm", "Warm ✓ · 11 reps · last 3 days ago"]);
  console.error = origError;
  process.exit(process.exitCode ?? 0);
})();
