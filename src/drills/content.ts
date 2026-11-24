// The question bank: skills, problems-as-data, frameworks and the Library path.
//
// A copy is compiled into the plugin (the three *.generated.json files). On start, every entry point
// (the index plugin and each widget) calls loadContent() before it imports anything that reads the bank;
// it fetches the bank CI publishes on the `content` branch after every green build of main, and uses it
// when it is newer and compatible. So new drills arrive without uploading the plugin again; only code
// changes (new coded generators, figure types, answer kinds) need a new upload.
//
// Safety: a published bank is used only when
//   - its contract equals this build's (src/drills/content-contract.json; bump it when code changes what
//     a bank may contain),
//   - every coded template it names is one this build compiles in (content-meta.generated.json `coded`),
//   - its hash matches the manifest and it parses with the expected top-level shape.
// Anything else (offline, refused, slow) falls back to the last good bank in the browser cache, then to
// the compiled copy. Modules read the bank through graphData()/loDrillsData()/pathData() at their own
// evaluation time, which is after loadContent() resolves, so they see whichever bank won.
import bundledGraph from "./skills.generated.json";
import bundledLo from "./lo-drills.generated.json";
import bundledPath from "./path.generated.json";
import meta from "./content-meta.generated.json";
import contractJson from "./content-contract.json";

export const CONTENT_CONTRACT: number = (contractJson as any).contract;
export const CONTENT_BASE = "https://raw.githubusercontent.com/kevindoeschemistry-droid/remnote-drills/content";
export const ONLINE_SETTING = "drills-online-content";
const CACHE = "drills-content-v1";

export interface Bank {
  graph: any;
  lo: any;
  path: any;
}
export interface Manifest {
  contract: number;
  hash: string;
  built: string;
  version: string;
  coded: string[];
}
export interface ContentStatus {
  source: "bundled" | "online" | "cached";
  hash: string;
  built?: string;
  version?: string;
  note?: string;
}

const BUNDLED_HASH: string = (meta as any).hash;
const BUILD_CODED = new Set<string>((meta as any).coded ?? []);

let bank: Bank = { graph: bundledGraph, lo: bundledLo, path: bundledPath };
let status: ContentStatus = { source: "bundled", hash: BUNDLED_HASH };
let applied = false;

export const graphData = (): any => bank.graph;
export const loDrillsData = (): any => bank.lo;
export const pathData = (): any => bank.path;
export const contentStatus = (): ContentStatus => status;

/** Why a manifest cannot be used by this build, or undefined if it can. */
export function refuseReason(m: Manifest | undefined): string | undefined {
  if (!m || typeof m.hash !== "string") return "no manifest";
  if (m.contract !== CONTENT_CONTRACT) return `needs plugin contract ${m.contract} (this plugin has ${CONTENT_CONTRACT}); upload the newer plugin`;
  const missing = (m.coded ?? []).filter((t) => !BUILD_CODED.has(t));
  if (missing.length) return `uses ${missing.length} generator(s) this plugin lacks (${missing.slice(0, 3).join(", ")}); upload the newer plugin`;
  return undefined;
}

function shapeOk(b: any): b is Bank {
  return !!b && Array.isArray(b.graph?.skills) && Array.isArray(b.graph?.problems) && typeof b.lo === "object" && Array.isArray(b.path?.frameworks);
}

/** Swap in a bank before any reader module is evaluated (tests call this directly). */
export function applyBank(b: Bank, s: ContentStatus): void {
  if (applied) throw new Error("the question bank was already read; apply a new one before importing readers");
  bank = b;
  status = s;
}

/** Call once readers start evaluating, so a late applyBank is caught. */
export function markApplied(): void {
  applied = true;
}

async function fetchJson<T>(url: string, ms: number, cache: Cache | undefined, fresh: boolean): Promise<{ data: T; from: "online" | "cached" } | undefined> {
  try {
    const ctl = typeof AbortController !== "undefined" ? new AbortController() : undefined;
    const timer = setTimeout(() => ctl?.abort(), ms);
    const res = await fetch(url, { signal: ctl?.signal, cache: fresh ? "no-cache" : "default" });
    clearTimeout(timer);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();
    const data = JSON.parse(text) as T;
    try {
      await cache?.put(url, new Response(text, { headers: { "content-type": "application/json" } }));
    } catch {
      /* cache full or unavailable: fine */
    }
    return { data, from: "online" };
  } catch {
    try {
      const hit = await cache?.match(url);
      if (hit) return { data: JSON.parse(await hit.text()) as T, from: "cached" };
    } catch {
      /* no cache */
    }
    return undefined;
  }
}

let loading: Promise<ContentStatus> | undefined;

/**
 * Load the newest compatible question bank. Never throws and never takes longer than a few seconds on a
 * slow network: on any failure the compiled bank stays in place.
 */
export function loadContent(opts: { online?: boolean } = {}): Promise<ContentStatus> {
  loading ??= (async () => {
    if (opts.online === false) {
      status = { source: "bundled", hash: BUNDLED_HASH, note: "online question bank turned off in settings" };
      return status;
    }
    if (typeof fetch === "undefined") return status;
    let cache: Cache | undefined;
    try {
      cache = typeof caches !== "undefined" ? await caches.open(CACHE) : undefined;
    } catch {
      cache = undefined;
    }
    // the bank is ~8 MB on a phone on a slow line, so allow it time, but the manifest must be quick
    const mf = await fetchJson<Manifest>(`${CONTENT_BASE}/manifest.json`, 4000, cache, true);
    if (!mf) {
      status = { source: "bundled", hash: BUNDLED_HASH, note: "could not reach the online question bank" };
      return status;
    }
    const m = mf.data;
    const why = refuseReason(m);
    if (why) {
      status = { source: "bundled", hash: BUNDLED_HASH, built: m.built, version: m.version, note: why };
      return status;
    }
    if (m.hash === BUNDLED_HASH) {
      status = { source: "bundled", hash: BUNDLED_HASH, built: m.built, version: m.version, note: "the plugin already has the newest question bank" };
      return status;
    }
    const bf = await fetchJson<Bank & { hash?: string }>(`${CONTENT_BASE}/bank-${m.hash}.json`, 30000, cache, false);
    if (!bf || !shapeOk(bf.data) || (bf.data.hash && bf.data.hash !== m.hash)) {
      status = { source: "bundled", hash: BUNDLED_HASH, note: "the online question bank did not download in full" };
      return status;
    }
    applyBank({ graph: bf.data.graph, lo: bf.data.lo, path: bf.data.path }, { source: bf.from === "online" && mf.from === "online" ? "online" : "cached", hash: m.hash, built: m.built, version: m.version });
    return status;
  })();
  return loading;
}
