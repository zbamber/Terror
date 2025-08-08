import prisma from "../src/lib/server/prisma.js";
import fs from "fs";
import path from "path";

async function extractMethods() {
  const batchSize = 10000;
  let skip = 0;
  const seen = new Set();

  console.log("Fetching attack types from database in batches...");

  while (true) {
    const batch = await prisma.attack.findMany({
      select: { attackType: true },
      skip,
      take: batchSize,
    });

    if (batch.length === 0) break;

    for (const a of batch) {
      const method = a.attackType?.trim();
      if (method && method !== "Unknown") {
        seen.add(method);
      }
    }

    skip += batchSize;
    console.log(`Processed ${skip} records...`);
  }

  const methods = Array.from(seen).sort();
  const outPath = path.resolve("./src/lib/data/methods.json");
  fs.writeFileSync(outPath, JSON.stringify(methods, null, 2));

  console.log(`Extracted ${methods.length} unique methods`);
  console.log(`Written to: ${outPath}`);

  await prisma.$disconnect();
}

extractMethods();
