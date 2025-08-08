import prisma from "../src/lib/server/prisma.js";

async function getEarliestDate() {
  const result = await prisma.attack.findFirst({
    orderBy: [
      { year: 'asc' },
      { month: 'asc' },
      { day: 'asc' },
    ],
    select: {
      day: true,
      month: true,
      year: true,
    },
  });

  if (result) {
    console.log(`Earliest date found: Day: ${result.day}, Month: ${result.month}, Year: ${result.year}`);
  } else {
    console.log("No attack data found in the database.");
  }
}

getEarliestDate()
  .catch(console.error)
  .finally(() => prisma.$disconnect());