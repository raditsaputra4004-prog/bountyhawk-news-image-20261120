// World News — Friday 20 November 2026.
//
// The entry is a single pre-drawn image, entry.png, committed beside this
// file. This program copies it into the output directory, byte for byte.
// It is deterministic: the same input always produces the same output,
// with no network, no clock and no randomness involved.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(repoRoot, "entry.png");
const target = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);
// Guard against a truncated copy: the output must be the same size
// as the source, or the run has failed even though it wrote a file.
const sourceBytes = statSync(source).size;
const targetBytes = statSync(target).size;
if (sourceBytes !== targetBytes) {
  throw new Error(
    `copied ${targetBytes} bytes, expected ${sourceBytes}`,
  );
}
console.log(`wrote ${target} (${targetBytes} bytes)`);
