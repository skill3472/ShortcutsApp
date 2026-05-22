<script lang="ts">
  import type { AppShortcut } from '$lib/bindings/bindings.types';
  import KeyBadge from './KeyBadge.svelte';

  type Props = {
    title: string;
    shortcuts: AppShortcut[];
    query?: string;
  };

  let { title, shortcuts, query = '' }: Props = $props();

  let visible = $derived(
    shortcuts.filter(s => s.name.toLowerCase().includes(query.toLowerCase()))
  );
</script>

{#if visible.length > 0}
  <div class="card bg-base-200 border border-base-300">
    <div class="card-body p-4 gap-3">
      <h2 class="card-title text-sm text-base-content/60 uppercase tracking-widest">
        {title}
      </h2>
      <div class="flex flex-col gap-2">
        {#each visible as shortcut}
          <div class="flex items-center justify-between">
            <span class="text-sm text-base-content">{shortcut.name}</span>
            <div class="flex gap-1">
              {#each shortcut.keystrokes as key}
                <KeyBadge {key} />
              {/each}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
{/if}
