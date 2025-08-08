import groupNames from "$lib/data/groupNames.json";

export async function GET() {
  return new Response(JSON.stringify(groupNames), {
    headers: {
      "Content-Type": "application/json",
    },
  });
}
