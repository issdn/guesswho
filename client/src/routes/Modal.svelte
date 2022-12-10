<script lang="ts">
	export let modalOpen: boolean;
	export let closeModal: () => void;
	import blobs from '$lib/assets/bgblobs.svg';
</script>

{#if modalOpen}
	<div
		class="fixed top-0 left-0 z-20 flex h-screen w-screen flex-col content-center justify-center"
	>
		<div class="flex flex-row justify-center">
			<div class="relative z-[21] flex h-96 w-96 flex-col gap-8 rounded-xl bg-lemon py-8 px-16">
				<img
					src={blobs}
					class="absolute top-0 left-0 -z-[5] h-full w-full rounded-xl object-cover"
					alt="bg blobs"
				/>
				<slot />
			</div>
		</div>
		<div on:mousedown={closeModal} class="fixed top-0 left-0 h-full w-full bg-black opacity-75" />
	</div>
{/if}
