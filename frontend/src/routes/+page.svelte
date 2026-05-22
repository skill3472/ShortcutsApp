<script lang="ts">
  import { onMount } from 'svelte';
  import AppSection from '$lib/components/AppSection.svelte';
  import { getApplications, getCategories, getShortcuts, type Application } from '$lib/api';
  import type { AppData } from '$lib/bindings/bindings.types';

  let apps = $state<Application[]>([]);
  let activeId = $state<number | null>(null);
  let loadedApp = $state<AppData | null>(null);
  let loading = $state(true);
  let loadingApp = $state(false);
  let query = $state('');
  let theme = $state('dim');

  let activeApp = $derived(apps.find(a => a.application_id === activeId) ?? null);

  async function loadApp(app: Application) {
    loadingApp = true;
    loadedApp = null;

    const catsRes = await getCategories(app.application_id);
    if (!catsRes.ok) { loadingApp = false; return; }

    const categories = await Promise.all(
      catsRes.data.map(async (cat) => {
        const scRes = await getShortcuts(cat.category_id);
        return { id: cat.category_id, name: cat.name, shortcuts: scRes.ok ? scRes.data : [] };
      })
    );

    loadedApp = { id: app.application_id, name: app.name, color: app.color, categories };
    loadingApp = false;
  }

  function selectApp(app: Application) {
    activeId = app.application_id;
    loadApp(app);
  }

  onMount(async () => {
    const res = await getApplications();
    if (res.ok) {
      apps = res.data;
      if (apps.length > 0) selectApp(apps[0]);
    }
    loading = false;
  });
</script>

<div data-theme={theme} style="min-height: 100vh;">
  <div class="navbar bg-base-200 px-4 border-b border-base-300">
    <div class="flex-1 gap-2 items-center flex-wrap">
      <span class="text-lg font-medium">keybinds</span>
      {#each apps as app}
        <button
          class="badge cursor-pointer transition-colors"
          class:badge-ghost={app.application_id !== activeId}
          style={app.application_id === activeId ? `background-color:${app.color}; border-color:${app.color}; color:white;` : ''}
          onclick={() => selectApp(app)}
        >
          {app.name}
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

  {#if loading}
    <div class="flex justify-center items-center p-16">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else if apps.length === 0}
    <div class="flex flex-col items-center justify-center p-16 gap-2 text-base-content/40">
      <p>No applications yet.</p>
      <a href="/admin/panel" class="link text-sm">Add some in the admin panel →</a>
    </div>
  {:else if loadingApp}
    <div class="flex justify-center items-center p-16">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else if loadedApp}
    <AppSection app={loadedApp} {query} />
  {/if}

  <footer class="border-t border-base-300 px-4 py-3 flex items-center justify-between text-xs text-base-content/40">
    <span>made with &lt;3 by <a class="text-[cadetblue] hover:text-[cadetblue]/70 transition-colors" href="https://cv.mtym.me/">skill</a></span>
    <a href="/admin" class="hover:text-base-content transition-colors">admin</a>
  </footer>
</div>
