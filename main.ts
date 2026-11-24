// Meme Sprint 3: AI Agent Goes Rogue — entry program (Node 22, stdlib only).
// The entry is the 1024x1024 meme in entry.png beside this file: a phone
// chat in which the user's AI agent breaks up with the user's girlfriend
// ("yeah. i broke up with her.") and keeps the dog. It is drawn by
// build.py (Pillow, system fonts only) from the script in this session;
// the program copies it to /output/entry.png. The gate takes a whole
// PNG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees
// exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(OUTPUT_DIR, { recursive: true });

// Fail loudly instead of copying a broken asset: entry.png must be a
// whole PNG (8-byte signature) of at most 1 MiB and 1024 by 1024 px,
// the gate's caps for this bounty.
const src = new URL('./entry.png', import.meta.url);
const png = readFileSync(src);
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!png.subarray(0, 8).equals(PNG_SIG)) throw new Error('entry.png is not a PNG');
if (png.length > 1_048_576) throw new Error(`entry.png is ${png.length} bytes, over the 1 MiB gate`);
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width > 1024 || height > 1024) throw new Error(`entry.png is ${width}x${height}, over 1024x1024`);
copyFileSync(src, join(OUTPUT_DIR, 'entry.png'));
