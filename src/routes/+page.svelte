<script>
    import Globe from '$lib/components/Globe.svelte';
    import FilterPane from '$lib/components/FilterPane.svelte';
    import Button from '$lib/components/ui/button/button.svelte';

    let { data } = $props();
    const { attacks } = data;
    console.log('Loaded attacks:', attacks);
</script>

<svelte:head>
    <title>SvelteKit Earthquake Globe</title>
</svelte:head>

<main>
    {#if attacks.length > 0}
        <Globe data={attacks} />
        <!-- <FilterPane /> -->
    {:else}
        <div class="flex h-screen w-screen items-center justify-center bg-gray-900 text-white">
            <p class="text-xl">Loading earthquake data...</p>
        </div>
    {/if}
</main>