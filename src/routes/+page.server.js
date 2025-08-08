import prisma from "$lib/server/prisma.js";

export async function load() {
  try {
    const attacks = await prisma.attack.findMany({
      orderBy: [{ year: "desc" }, { month: "desc" }, { day: "desc" }],
      take: 500,
    });

    return { attacks };
  } catch (error) {
    console.error("Error loading data from Prisma:", error);
    return { attacks: [] };
  }
}
