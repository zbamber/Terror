<script>
	import { onMount } from 'svelte';

	// let props = $props();
    let { data,
        rotating = $bindable()
     } = $props();

    let container;
	let globe = $state(null);
    let hoveredPoint = $state(null);

	onMount(async () => {
		const THREE = await import('three');
		const { default: Globe } = await import('globe.gl');

		const localGlobe = new Globe(container)
			.globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
			.bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
			.pointLat((d) => d.lat)
			.pointLng((d) => d.lng)
			.pointAltitude(0)
			.pointRadius(0.5)
			.pointColor(d => 'red')
			.pointsData(data)
            .backgroundColor('#000000')
            .atmosphereColor('ghostwhite')
            .atmosphereAltitude('0.1')
            .onPointHover(obj => {hoveredPoint = obj})
            .pointsTransitionDuration(300);

		const scene = localGlobe.scene();
		const camera = localGlobe.camera();
		const renderer = localGlobe.renderer();
		const controls = localGlobe.controls();
        controls.autoRotate = rotating;

        // console.log(scene.children)

        // scene.children.forEach((child, index) => {
		// 	console.log(`Child ${index}:`, child.type, child);
		// 	if (child.type === 'Mesh' && child !== localGlobe) {
		// 		console.log('Removing mysterious mesh:', child);
		// 		scene.remove(child);
		// 	}
		// });

        // console.log(scene.children)
		// scene.add(new THREE.AmbientLight(0xbbbbbb, 0.1));
		// scene.add(new THREE.DirectionalLight(0xffffff, 0.4));

		camera.position.z = 400;

		// controls.enableDamping = true;
		// controls.minDistance = 150;
		// controls.maxDistance = 400;
		// controls.autoRotate = true;
		// controls.autoRotateSpeed = 0.5;

		// renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

		// const handleResize = () => {
		// 	localGlobe.width(window.innerWidth).height(window.innerHeight);
		// };
		// window.addEventListener('resize', handleResize);
        
        globe = localGlobe;

		return () => {
			window.removeEventListener('resize', handleResize);
			localGlobe.pauseAnimation();
            globe = null;
		};
	});

	$effect(() => {
		if (globe && data) {
            // console.log('Updating globe data');
			globe.pointsData(data);
		}
	});

    $effect(() => {
        if (globe) {
            const controls = globe.controls();
            controls.autoRotate = rotating;
        }
    });

    $effect(() => {
        const currentHoveredPoint = hoveredPoint
		if (globe && data) {
			globe.pointAltitude(d => d === hoveredPoint ? 0.05 : 0);
            globe.pointColor(d => d === hoveredPoint ? 'white': 'red');
            globe.pointRadius(d => d === hoveredPoint ? '1': '0.5');
			globe.pointsData(data);
		}
	});
</script>

<div bind:this={container} class="fixed inset-0"></div>