<script lang="ts">
	export let style: string = '';
</script>

<p class="after:content-[''] after:absolute after:animate-dots {style}">
	<slot />
</p>
