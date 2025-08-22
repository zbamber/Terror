<script>
    import Globe from '@/lib/components/Globe.svelte';
    import NewGlobe from '@/lib/components/NewGlobe.svelte';
    import FilterPane from '$lib/components/FilterPane.svelte';
    import InfoCard from '@/lib/components/InfoCard.svelte';
    import * as Alert from "$lib/components/ui/alert/index.js";
    import Loader from "@lucide/svelte/icons/loader"
    import Button from '$lib/components/ui/button/button.svelte';
    import { CalendarDate } from '@internationalized/date';
    import groupLookup from '$lib/data/groupLookup.json'
    import { json } from '@sveltejs/kit';
    import { onMount } from 'svelte';
    import * as Card from "$lib/components/ui/card/index.js";
    import AlertDialog from '@/lib/components/AlertDialog.svelte';
    import { get } from 'svelte/store';

    let { data } = $props();
    let attacks = $state(data.attacks ?? []);
    // console.log('Loaded attacks:', attacks);
    let dataStartDate = new CalendarDate(2017, 12, 25)
    let dataEndDate = new CalendarDate(2017, 12, 31)
    console.log(dataEndDate.toString())
    let startDate = $state(dataStartDate);
    let endDate = $state(dataEndDate);
    let selectedGroupCategory = $state(null);
    let selectedTargetType = $state(null);
    let selectedAttackType = $state(null);
    let fatalityRange = $state([0,201]);
    let alerting = $state(false);

    const msInOneDay = 1000 * 60 * 60 * 24

    let rotating = $state(false);
    let selectedPoint = $state(null);

    let filteredData = $derived(attacks.filter(d => {
        const groupPass = !selectedGroupCategory || groupLookup[selectedGroupCategory].includes(d.groupName)
        
        const targetPass = !selectedTargetType || d.targetType === selectedTargetType

        const methodPass = !selectedAttackType || d.attackType === selectedAttackType

        const fatalitiesPass = fatalityRange[0] <= d.numKilled && (fatalityRange[1] === 201 || d.numKilled <= fatalityRange[1])
        
        return groupPass && targetPass && methodPass && fatalitiesPass
    }));

    let loading = $state(false);

    function calToISO(cd) {
        return `${String(cd.year).padStart(4,'0')}-${String(cd.month).padStart(2,'0')}-${String(cd.day).padStart(2,'0')}`;
    }

    function handleSubmit () {
        if (startDate >= dataStartDate && endDate <= dataEndDate) {
            return;
        }

        const start = calToISO(startDate);
        const end = calToISO(endDate)

        const MAX_DAYS = 365 * 2
        const daysRequested = Math.floor((new Date(end) - new Date(start)) / msInOneDay) + 1;
        console.log(daysRequested)
        if (daysRequested > MAX_DAYS) {
            alerting = true;
            return;
        }
        
        getAttacks(start,end)
    };
     
    async function getAttacks(start, end) {
        loading = true
        try {
            const response = await fetch('/api/data', {
                method: 'POST',
                body: JSON.stringify({ start, end }),
                headers: {
                    'content-type': 'application/json'
                }
            });
            
            if (!response.ok) {
                console.error('API Error:', await response.text());
                return [];
            }

            attacks = await response.json();
        } catch (error) {
            console.error('Fetch failed:', error);
            loading = false
            return [];
        } finally {
            loading = false
            dataStartDate = startDate;
            dataEndDate = endDate;
        }
    }

</script>

<svelte:head>
    <title>Global Terrorism</title>
</svelte:head>

<main class="relative h-screen w-screen">
    <AlertDialog
    bind:open={alerting}
    bind:startDate
    bind:endDate
    {getAttacks}
    {calToISO}
    />
    {#if attacks.length > 0}
        <div class="absolute inset-0 z-0 bg-black">
            <NewGlobe
            data={filteredData}
            bind:rotating={rotating}
            bind:selectedPoint/>
        </div>
        <FilterPane
        bind:startDate
        bind:endDate
        bind:selectedGroupCategory
        bind:selectedTargetType
        bind:selectedAttackType
        bind:fatalityRange
        bind:rotating
        filteredCount={filteredData.length}
        totalCount={attacks.length}
        submitCallback={handleSubmit}
        />
        {#if loading}
            <div class="absolute bottom-0 left-1/2 -translate-x-1/2 mb-20 w-full max-w-xl">
                <Alert.Root>
                    <Loader class="animate-spin"/>
                    <Alert.Title>Loading!</Alert.Title>
                    <Alert.Description
                    >Loading records between {startDate} and {endDate}</Alert.Description
                    >
                </Alert.Root>
            </div>
        {/if}
        {#if selectedPoint}
            <InfoCard {selectedPoint}/>
        {/if}
    {:else}
        <div class="flex h-screen w-screen items-center justify-center text-white">
            <p class="text-xl">Loading earthquake data...</p>
        </div>
    {/if}
</main>