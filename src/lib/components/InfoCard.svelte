<script>
    import * as Card from "$lib/components/ui/card/index.js";
    import Button from '$lib/components/ui/button/button.svelte';
    import { Inspect } from "lucide-svelte";
    let { selectedPoint } = $props();
    import { Separator } from "$lib/components/ui/separator/index.js";
    console.log(selectedPoint.city)
</script>

<Card.Root class="absolute right-0 mr-20 mt-20 w-full  max-w-sm">
<Card.Header>
    <Card.Title class="text-lg">{selectedPoint.city}, {selectedPoint.city}</Card.Title>
    <Card.Description>
        {selectedPoint.country} &middot; {new Date(selectedPoint.eventDate).toLocaleDateString()}
    </Card.Description>
</Card.Header>
<Card.Content class="space-y-3">
    <p class="text-sm text-muted-foreground">
        {selectedPoint.summary.split(/:\s(.+)/)[1] || ""}
    </p>
    <Separator />
    <div class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
      <div>
        <span class="font-semibold">Attack Type:</span><br />
        {selectedPoint.attackType}
      </div>
      <div>
        <span class="font-semibold">Target:</span><br />
        {selectedPoint.targetType}
      </div>
      <div>
        <span class="font-semibold">Group:</span><br />
        {selectedPoint.groupName || "Unknown"}
      </div>
      <div>
        <span class="font-semibold">Fatalities:</span><br />
        {selectedPoint.numKilled}
      </div>
    </div>
</Card.Content>
<Card.Footer class="flex justify-between text-xs text-muted-foreground">
    <span>Event ID: {selectedPoint.id}</span>
    <span>Created {new Date(selectedPoint.createdAt).toLocaleDateString()}</span>
</Card.Footer>
</Card.Root>