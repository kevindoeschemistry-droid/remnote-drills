// Fails when the version is not the same everywhere RemNote or npm reads it.
// On a tag build (GITHUB_REF_NAME = v0.28.0) the tag has to match too.
import { readFileSync } from 'node:fs';

const pkg = JSON.parse(readFileSync('package.json', 'utf8'));
const manifest = JSON.parse(readFileSync('public/manifest.json', 'utf8'));
const v = manifest.version;
const found = {
  'package.json version': pkg.version,
  'package.json pluginManifest.version': pkg.pluginManifest?.version,
  'public/manifest.json version': `${v.major}.${v.minor}.${v.patch}`,
};
if (process.env.GITHUB_REF_TYPE === 'tag') {
  found[`tag ${process.env.GITHUB_REF_NAME}`] = process.env.GITHUB_REF_NAME.replace(/^v/, '');
}

const distinct = new Set(Object.values(found));
for (const [where, version] of Object.entries(found)) console.log(`${version}  ${where}`);
if (distinct.size !== 1) {
  console.error('Versions disagree. Bump them together.');
  process.exit(1);
}
if (pkg.pluginManifest?.id !== manifest.id || manifest.id !== 'wiki-sync') {
  console.error(`Plugin id must stay "wiki-sync" (found ${pkg.pluginManifest?.id} / ${manifest.id}).`);
  process.exit(1);
}
