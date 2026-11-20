const { copyFileSync, mkdirSync } = require('node:fs');
const { join } = require('node:path');

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });
copyFileSync(join(__dirname, 'entry.png'), join(outputDir, 'entry.png'));
