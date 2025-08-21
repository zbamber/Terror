import prisma from "../src/lib/server/prisma.js";

async function getMaxKilled() {
  const result = await prisma.attack.aggregate({
    _max: {
      numKilled: true,
    },
  });
  console.log(`max killed: ${result._max.numKilled}`);
}

getMaxKilled()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
