<script lang="ts">
  import BindingCard from './BindingCard.svelte';
  import type { AppData } from '$lib/bindings/bindings.types';

  type Props = {
    app: AppData;
    query?: string;
  };

  let { app, query = '' }: Props = $props();
</script>

<div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
  {#each app.categories as category}
    <BindingCard title={category.name} shortcuts={category.shortcuts} {query} />
  {/each}
</div>
