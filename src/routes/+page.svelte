<script>
    import Globe from '$lib/components/Globe.svelte';
    import FilterPane from '$lib/components/FilterPane.svelte';
    import * as Alert from "$lib/components/ui/alert/index.js";
    import Loader from "@lucide/svelte/icons/loader"
    import Button from '$lib/components/ui/button/button.svelte';
    import { CalendarDate } from '@internationalized/date';
    import groupLookup from '$lib/data/groupLookup.json'
    import { json } from '@sveltejs/kit';
    import { onMount } from 'svelte';

    let { data } = $props();
    let attacks = $state(data.attacks ?? []);
    // console.log('Loaded attacks:', attacks);
    let previousStartDate = new CalendarDate(2017, 12, 25)
    let previousEndDate = new CalendarDate(2017, 12, 31)
    let startDate = $state(previousStartDate);
    let endDate = $state(previousEndDate);
    let selectedGroupCategory = $state(null);
    let selectedTargetType = $state(null);
    let selectedAttackType = $state(null);
    let fatalityRange = $state([0,201]);

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
     
    $effect(() => {
        if (startDate === previousStartDate && endDate === previousEndDate) {
            return;
        }

        const start = calToISO(startDate)
        const end = calToISO(endDate)

        const MAX_DAYS = 365 * 2
        const daysRequested = Math.floor((new Date(end) - new Date(start)) / (24 * 3600 * 1000)) + 1;

        if (daysRequested > MAX_DAYS) {
            startDate = previousStartDate;
            endDate = previousEndDate;
            loading = false;
            return;
        }

        previousStartDate = startDate
        previousEndDate = endDate

        const fetchData = async () => {
            loading = true;
            try {
                const result = await getAttacks(start, end);
                attacks = result;
            } catch (error) {
                console.error('Failed to fetch attacks:', error);
                attacks = [];
            } finally {
                loading = false;
            }
        };

        fetchData();
    });
        
    async function getAttacks(start, end) {
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

            return await response.json();
        } catch (error) {
            console.error('Fetch failed:', error);
            return [];
        }
    }

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
        bind:selectedGroupCategory
        bind:selectedTargetType
        bind:selectedAttackType
        bind:fatalityRange
        filteredCount={filteredData.length}
        totalCount={attacks.length}
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
    {:else}
        <div class="flex h-screen w-screen items-center justify-center text-white">
            <p class="text-xl">Loading earthquake data...</p>
        </div>
    {/if}
</main>