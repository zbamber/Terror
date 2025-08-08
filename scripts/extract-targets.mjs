import prisma from "../src/lib/server/prisma.js";
import fs from "fs";
import path from "path";

async function extractTargetTypes() {
  const batchSize = 10000;
  let skip = 0;
  const seen = new Set();

  console.log("Fetching target types from database in batches...");

  while (true) {
    const batch = await prisma.attack.findMany({
      select: { targetType: true },
      skip,
      take: batchSize,
    });

    if (batch.length === 0) break;

    for (const a of batch) {
      const name = a.targetType?.trim();
      if (name && name !== "Unknown") {
        seen.add(name);
      }
    }

    skip += batchSize;
    console.log(`Processed ${skip} records...`);
  }

  const groups = Array.from(seen).sort();
  const outPath = path.resolve("./src/lib/data/targetTypes.json");
  fs.writeFileSync(outPath, JSON.stringify(groups, null, 2));

  console.log(`Extracted ${groups.length} unique target types`);
  console.log(`Written to: ${outPath}`);

  await prisma.$disconnect();
}

extractTargetTypes();
