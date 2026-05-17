<script lang="ts">
  type Binding = {
    label: string;
    keys: string[];
  };

  type Props = {
    title: string;
    bindings: Binding[];
    query?: string;
  };

  let { title, bindings, query = '' }: Props = $props();

  let visible = $derived(
    bindings.filter(b => b.label.toLowerCase().includes(query.toLowerCase()))
  );
</script>

{#if visible.length > 0}
  <div class="card bg-base-200 border border-base-300">
    <div class="card-body p-4 gap-3">
      <h2 class="card-title text-sm text-base-content/60 uppercase tracking-widest">
        {title}
      </h2>
      <div class="flex flex-col gap-2">
        {#each visible as binding}
          <div class="flex items-center justify-between">
            <span class="text-sm text-base-content">{binding.label}</span>
            <div class="flex gap-1">
              {#each binding.keys as key}
                <kbd class="kbd kbd-sm">{key}</kbd>
              {/each}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
{/if}