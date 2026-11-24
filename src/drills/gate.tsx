// Every widget entry renders through this gate: it loads the question bank (src/drills/content.ts) first
// and only then imports the widget's real module, so the modules that read the bank see the newest one.
import React, { useEffect, useState } from "react";
import { usePlugin } from "@remnote/plugin-sdk";
import { loadContent, ONLINE_SETTING } from "./content";

export async function settingOnline(plugin: { settings: { getSetting<T>(id: string): Promise<T> } }): Promise<boolean> {
  try {
    const v = await plugin.settings.getSetting<boolean | undefined>(ONLINE_SETTING);
    return v !== false;
  } catch {
    return true;
  }
}

export function gate(load: () => Promise<{ default: React.ComponentType<any> }>) {
  return function Gated() {
    const plugin = usePlugin();
    const [Comp, setComp] = useState<React.ComponentType<any> | null>(null);
    useEffect(() => {
      let live = true;
      (async () => {
        await loadContent({ online: await settingOnline(plugin) });
        const m = await load();
        if (live) setComp(() => m.default);
      })().catch((e) => console.error("[Drills] widget failed to load", e));
      return () => {
        live = false;
      };
    }, []);
    return Comp ? <Comp /> : null;
  };
}
