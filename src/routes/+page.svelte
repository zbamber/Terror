<script>
    import Globe from '$lib/components/Globe.svelte';
    import FilterPane from '$lib/components/FilterPane.svelte';
    import Button from '$lib/components/ui/button/button.svelte';
    import { CalendarDate } from '@internationalized/date';

    let { data } = $props();
    const { attacks } = data;
    console.log('Loaded attacks:', attacks);

    let startDate = $state(new CalendarDate(2017, 12, 25));
    let endDate = $state(new CalendarDate(2017, 12, 31));
    let selectedGroup = $state(null);
    let selectedTargetType = $state(null);
    let selectedAttackType = $state(null);
    let fatalityRange = $state([0,201]);

    let filteredData = $derived(attacks.filter(d => {
        const groupPass = !selectedGroup || d.groupName === selectedGroup
        
        const targetPass = !selectedTargetType || d.targetType === selectedTargetType

        const methodPass = !selectedAttackType || d.attackType === selectedAttackType

        const fatalitiesPass = fatalityRange[0] <= d.numKilled && (fatalityRange[1] === 201 || d.numKilled <= fatalityRange[1])
        
        return groupPass && targetPass && methodPass && fatalitiesPass
    }));

</script>

<svelte:head>
    <title>SvelteKit Earthquake Globe</title>
</svelte:head>

<main class="relative h-screen w-screen">
    {#if attacks.length > 0}
        <div class="absolute inset-0 z-0 bg-black">
            <Globe data={filteredData} />
            
        </div>
        <FilterPane
        bind:startDate
        bind:endDate
        bind:selectedGroup
        bind:selectedTargetType
        bind:selectedAttackType
        bind:fatalityRange
        filteredCount={filteredData.length}
        totalCount={attacks.length}
        />
    {:else}
        <div class="flex h-screen w-screen items-center justify-center bg-gray-900 text-white">
            <p class="text-xl">Loading earthquake data...</p>
        </div>
    {/if}
</main>