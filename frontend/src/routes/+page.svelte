<script lang="ts">
  import AppSection from '$lib/components/AppSection.svelte';
  import { neovim } from '$lib/bindings/neovim';
  import { tmux } from '$lib/bindings/tmux';
  import type { App } from '$lib/bindings/bindings.types';

  const apps: App[] = [neovim, tmux];

  let theme = $state('dim');
  let query = $state('');
  let activeId = $state(apps[0].id);

  let activeApp = $derived(apps.find(a => a.id === activeId)!);
</script>

<div data-theme={theme} style="min-height: 100vh;">
  <div class="navbar bg-base-200 px-4 border-b border-base-300">
    <div class="flex-1 gap-2 items-center flex-wrap">
      <span class="text-lg font-medium">keybinds</span>
      {#each apps as app}
        <button
          class="badge cursor-pointer {app.id === activeId ? app.labelColor : 'badge-ghost'}"
          onclick={() => activeId = app.id}
        >
          {app.label}
        </button>
      {/each}
    </div>
    <div class="flex gap-2 items-center">
      <input
        type="checkbox"
        class="toggle toggle-sm"
        onchange={e => theme = e.currentTarget.checked ? 'light' : 'dim'}
      />
      <input
        type="text"
        placeholder="search bindings…"
        class="input input-sm input-bordered w-48"
        bind:value={query}
      />
    </div>
  </div>

  <AppSection app={activeApp} {query} />
</div>