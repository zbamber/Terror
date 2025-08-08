<script lang="ts">
 import CheckIcon from "@lucide/svelte/icons/check";
 import ChevronsUpDownIcon from "@lucide/svelte/icons/chevrons-up-down";
 import { tick } from "svelte";
 import * as Command from "$lib/components/ui/command/index.js";
 import * as Popover from "$lib/components/ui/popover/index.js";
 import { Button } from "$lib/components/ui/button/index.js";
 import { cn } from "$lib/utils.js";
 
 let options = $state<{ value: string; label: string }[]>([]);
 let hasLoaded = $state(false);
 let open = $state(false);
 let { value = $bindable(),  dataType } = $props(); 
 let triggerRef = $state<HTMLButtonElement>(null!);

 let selectedValue = $derived(
  options.find((g) => g.value === value)?.label
 );
 
const reset = function() {
    value = null;
    selectedValue = null;
};

 $effect(() => {
    if (open && !hasLoaded) {
        fetch(`/api/${dataType}`)
        .then(res => res.json())
        .then((data: string[]) => {
            options = data.map(name => ({
            value: name,
            label: name
            }));
            hasLoaded = true;
        })
        .catch(err => {
            console.error(`Failed to load ${dataType}s:`, err);
        });
    }
 });

 // We want to refocus the trigger button when the user selects
 // an item from the list so users can continue navigating the
 // rest of the form with the keyboard.
 function closeAndFocusTrigger() {
  open = false;
  tick().then(() => {
   triggerRef.focus();
  });
 }
</script>
<div class="flex flex-row gap-2 w-[280px]">
<Popover.Root bind:open>
 <Popover.Trigger bind:ref={triggerRef}>
  {#snippet child({ props })}
   <Button
    {...props}
    variant="outline"
    class="w-[200px] justify-between"
    role="combobox"
    aria-expanded={open}
   >
    <span class="truncate overflow-hidden text-ellipsis whitespace-nowrap max-w-[150px]">
        {selectedValue || `Select a ${dataType}...`}
    </span>
    <ChevronsUpDownIcon class="opacity-50" />
   </Button>
  {/snippet}
 </Popover.Trigger>
 <Popover.Content class="w-[200px] p-0">
  <Command.Root>
   <Command.Input placeholder={`Search ${dataType}s...`} />
   <Command.List>
    <Command.Empty>{`Loading ${dataType}s...`}</Command.Empty>
    <Command.Group value={`${dataType}s`}>
     {#each options as option (option.value)}
      <Command.Item
       value={option.value}
       onSelect={() => {
        value = option.value;
        closeAndFocusTrigger();
       }}
      >
       <CheckIcon
        class={cn(value !== option.value && "text-transparent")}
       />
       {option.label}
      </Command.Item>
     {/each}
    </Command.Group>
   </Command.List>
  </Command.Root>
 </Popover.Content>
</Popover.Root>
<Button 
class="flex-grow"
variant="outline"
onclick={reset}
>All</Button>
</div>