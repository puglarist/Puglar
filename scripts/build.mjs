import { cp, mkdir, rm } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const sourceDir = path.join(root, "web");
const distDir = path.join(root, "dist");

await rm(distDir, { recursive: true, force: true });
await mkdir(distDir, { recursive: true });
await cp(sourceDir, distDir, { recursive: true });

console.log("Built PWA assets into dist/");
