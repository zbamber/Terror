import prisma from "$lib/server/prisma.js";
import { json } from '@sveltejs/kit';

const MAX_TAKE = 5000;

export async function POST({ request }) {
    const { start, end } = await request.json();
    console.log('Received dates:', { start, end });

    const attacksFromDb = await prisma.attack.findMany({
        where: {
            eventDate: {
                gte: new Date(start),
                lte: new Date(end)
            }
        },
        orderBy: { eventDate: 'desc' },
        take: MAX_TAKE
    });

    const attacks = attacksFromDb.map(attack => ({
        ...attack,
        eventDate: attack.eventDate ? attack.eventDate.toISOString() : null,
        createdAt: attack.createdAt ? attack.createdAt.toISOString() : null
    }));

    return json(attacks)
}