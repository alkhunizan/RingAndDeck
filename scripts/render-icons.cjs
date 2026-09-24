// Batch rendering avoids starting a Node process for each native ring icon.
const fs = require('node:fs');
const sharp = require('sharp');

async function main() {
  const jobs = JSON.parse(fs.readFileSync(0, 'utf8'));
  const results = {};
  for (const [name, svg] of Object.entries(jobs)) {
    const input = Buffer.from(svg);
    const png = await sharp(input, { density: 192 })
      .resize(288, 288)
      .png({ compressionLevel: 9, adaptiveFiltering: false })
      .toBuffer();
    results[name] = png.toString('base64');
  }
  process.stdout.write(JSON.stringify(results));
}

main().catch((error) => {
  process.stderr.write(`Icon rendering failed: ${error.message}\n`);
  process.exitCode = 1;
});
