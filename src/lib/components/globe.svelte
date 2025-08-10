<script>
	import { onMount } from 'svelte';

	let props = $props();
    let container;
	let globe = $state(null);

	onMount(async () => {
        const THREE = await import('three');
        const { default: ThreeGlobe } = await import('three-globe');
		// const { default: Globe } = await import('globe.gl');
        const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js');

		const localGlobe = new ThreeGlobe()
			.globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
			.bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
			.pointLat((d) => d.lat)
			.pointLng((d) => d.lng)
			.pointAltitude(0)
			.pointRadius(0.5)
			.pointColor(d => 'red');

		const scene = new THREE.Scene();
		scene.add(localGlobe);
		scene.add(new THREE.AmbientLight(0xbbbbbb));
		scene.add(new THREE.DirectionalLight(0xffffff, 0.6));

		const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
		camera.position.z = 250;

		const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
		renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
		container.appendChild(renderer.domElement);

		const controls = new OrbitControls(camera, renderer.domElement);
		controls.enableDamping = true;
        controls.minDistance = 150;
        controls.maxDistance = 400;
        // controls.autoRotate = true;
        // controls.autoRotateSpeed = 0.5;

		const animate = () => {
            if (!localGlobe) return;
			controls.update();
			renderer.render(scene, camera);
			requestAnimationFrame(animate);
		};
		animate();

		const handleResize = () => {
			camera.aspect = window.innerWidth / window.innerHeight;
			camera.updateProjectionMatrix();
			renderer.setSize(window.innerWidth, window.innerHeight);
		};
		window.addEventListener('resize', handleResize);
        
        globe = localGlobe;

		return () => {
			window.removeEventListener('resize', handleResize);
            if (container && renderer.domElement) {
			    container.removeChild(renderer.domElement);
            }
            globe = null;
		};
	});

	$effect(() => {
		if (globe) {
            console.log('Updating globe data');
			globe.pointsData(props.data);
		}
	});

</script>

<div bind:this={container} class="fixed inset-0"></div>