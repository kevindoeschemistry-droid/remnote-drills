# Roadmap: off the wiki, off localhost

The drill plugin started as "Wiki Sync": a way to pull wiki flashcards into RemNote. It now stands on its own.
This is the plan to finish that split.

## Where things live (v0.15)

- **Cards** sit in your subject documents: `Heat Transfer › Drills › Heat transfer › Fins`, `Linear Algebra › Drills › …`,
  `Engineering Math (ODEs) › Drills › …`. Moving a group keeps its review history. The domain → subject map is
  `drills/library.yaml`.
- **Textbook PDFs** sit beside them, in the same subject document (from *Drills: Organize textbook PDFs*).
- **Book contents** ("By textbook": chapter → section → drill groups, with 📖 anchors) sit in a top-level `Drills` document.
- **Method notes** (`drills/methods.yaml`) and **PDF anchors** replace the wiki chapter links.
- **The wiki** is still used for two things only: *Sync Wiki Cards* (flashcards.json) and the last-resort "open the chapter
  summary" fallback when a book has no PDF linked.

## Steps

1. **Hosting off localhost.** Upload `PluginZip.zip` through RemNote → Plugins → Build → Upload plugin (unlisted).
   The repo is public and the manifest already says `"unlisted": true`, so RemNote reviews it. After approval, install it
   from the link and stop the localhost servers. Every release after that is a version bump plus a new upload.
2. **Rename the display name** from "Wiki Sync" to "Drills". Keep the id `wiki-sync`, because the card map, streaks and
   anchors are keyed to it.
3. **Make the wiki optional.**
   - A setting, *Wiki flashcards*, off by default for new installs, hides *Sync Wiki Cards*.
   - The wiki fallback link turns into "link a PDF for this book".
   - Then nothing in the drill path calls the wiki.
4. **Split the wiki sync** into its own small plugin, or retire it, once the wiki cards are migrated or no longer wanted.
5. **Drop the legacy migration code** (Wiki Flashcards › Drills, "ODE Drills — Level 1") after a release or two.
