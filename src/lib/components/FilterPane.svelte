<script lang="ts">
    import { buttonVariants } from "$lib/components/ui/button/index.js";
    import * as Popover from "$lib/components/ui/popover/index.js";
    import FilterCalendar from "./FilterCalendar.svelte";
    import Combo from "./Combo.svelte";
    import LockIcon from "@lucide/svelte/icons/lock";
    import OpenLockIcon from "@lucide/svelte/icons/lock-open"
    import { Slider } from "$lib/components/ui/slider/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import Button from "./ui/button/button.svelte";

    let {
        startDate = $bindable(),
        endDate = $bindable(),
        selectedGroup = $bindable(),
        selectedTargetType = $bindable(),
        selectedAttackType = $bindable(),
        fatalityRange = $bindable(),
        filteredCount,
        totalCount
    } = $props();

    let locked = $state(false);

    const toggleLock = function() {
        locked = !locked
    };

</script>
<div class="absolute top-5 left-5 z-10 w-80">
    <Popover.Root>
    <Popover.Trigger class={buttonVariants({ variant: "outline" })}
    >Options</Popover.Trigger
    >
    <Popover.Content class="w-80" align="start" interactOutsideBehavior={locked ? "ignore" : undefined}>
    <div class="grid gap-6">
    <div class="space-y-2">
        <div class="flex flex-row gap-2">
            <h4 class="font-large leading-none">Filters</h4>
            {#if locked}
            <LockIcon class="mr-2 size-4 right-5" onclick={toggleLock}></LockIcon>
            {:else}
            <OpenLockIcon class="mr-2 size-4 right-5" onclick={toggleLock}></OpenLockIcon>
            {/if}
        </div>
        <p class="text-muted-foreground text-sm">
        Filter the data you wish to see.
        </p>
    </div>
    <div class="grid gap-4">
        <FilterCalendar prompt='Pick a start Date' bind:value={startDate}/>
        <FilterCalendar prompt='Pick an end Date' bind:value={endDate}/>
        <Combo
        bind:value={selectedGroup}
        dataType="group"/>
        <Combo
        bind:value={selectedTargetType}
        dataType="target"/>
        <Combo
        bind:value={selectedAttackType}
        dataType="method"/>
        <Label class="font-medium leading-none">{`Fatalities between ${fatalityRange[0]} and ${fatalityRange[1] === 201 ? "200+": fatalityRange[1]}`}</Label>
        <Slider type="multiple" bind:value={fatalityRange} max={201} step={1}/>
    </div>
    <div class="mt-2 border-t border-white/20 pt-4">
        <p class="text-sm text-gray-300">
            Showing <strong>{filteredCount}</strong> of <strong>{totalCount}</strong> loaded attacks
        </p>
    </div>
    </div>
    </Popover.Content>
    </Popover.Root>
</div>