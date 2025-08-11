<script>
	import "../app.css";
	import favicon from "$lib/assets/favicon.svg";
	import Github from "@lucide/svelte/icons/github";
	import { Separator } from "$lib/components/ui/separator/index.js";

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<!-- Title -->
<div class="absolute top-4 left-1/2 -translate-x-1/2 z-50 text-center">
	<div class="leading-tight">
		<h1 class="m-0 text-4xl font-extrabold tracking-tight">
			Global Terrorism
		</h1>
		<p class="m-0 text-muted-foreground text-xs">
			Visualising terrorist incidents worldwide from 1970 to 2017
		</p>
	</div>
</div>

<!-- Render the actual page content -->
{@render children?.()}

<!-- Footer -->
<div class="absolute bottom-4 left-1/2 -translate-x-1/2 z-50 flex gap-x-3 text-sm text-muted-foreground">
	<div class="flex h-5 items-center space-x-4 text-sm">
		<p>
			Data source:{' '}
			<a href="https://www.start.umd.edu/data-tools/GTD" target="_blank" class="hover:underline">
				Global Terrorism Database (GTD)
			</a>
		</p>
		<Separator orientation="vertical" />
		<a href="https://github.com/zbamber/Terror" target="_blank" class="hover:underline flex items-center">
			<Github class="mr-2 size-4"/>
			GitHub
		</a>
		<Separator orientation="vertical" />
		<p>© 2025 Zakary Bamber</p>
	</div>
</div>
