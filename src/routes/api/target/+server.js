import targetTypes from "$lib/data/targetTypes.json";

export async function GET() {
  return new Response(JSON.stringify(targetTypes), {
    headers: {
      "Content-Type": "application/json",
    },
  });
}
