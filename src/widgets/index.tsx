// Plugin entry: load the question bank (src/drills/content.ts), then the plugin (src/widget-main/index.tsx).
import { declareIndexPlugin, ReactRNPlugin } from "@remnote/plugin-sdk";
import { loadContent } from "../drills/content";
import { settingOnline } from "../drills/gate";

async function onActivate(plugin: ReactRNPlugin) {
  const s = await loadContent({ online: await settingOnline(plugin) });
  console.log(`[Drills] question bank: ${s.source} ${s.hash}${s.built ? ` (built ${s.built})` : ""}${s.note ? ` — ${s.note}` : ""}`);
  const main = await import(/* webpackMode: "eager" */ "../widget-main/index");
  await main.onActivate(plugin);
}

async function onDeactivate(plugin: ReactRNPlugin) {
  const main = await import(/* webpackMode: "eager" */ "../widget-main/index");
  await main.onDeactivate(plugin);
}

declareIndexPlugin(onActivate, onDeactivate);
