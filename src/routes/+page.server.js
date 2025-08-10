import prisma from "$lib/server/prisma.js";

const DEFAULT_START = '2017-12-25';
const DEFAULT_END   = '2017-12-31';
const MAX_TAKE = 5000;

export async function load() {
    try {
        const attacks = await prisma.attack.findMany({
            where: {
                eventDate: {
                    gte: new Date(DEFAULT_START),
                    lte: new Date(DEFAULT_END)
                }
            },
            orderBy: { eventDate: 'desc' }
        });
        return { attacks };
    } catch (error) {
        console.error("Error loading data from Prisma:", error);
        return { attacks: [] };
    }
}

