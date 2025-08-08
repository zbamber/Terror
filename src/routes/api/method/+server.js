import methods from "$lib/data/methods.json";

export async function GET() {
  return new Response(JSON.stringify(methods), {
    headers: {
      "Content-Type": "application/json",
    },
  });
}