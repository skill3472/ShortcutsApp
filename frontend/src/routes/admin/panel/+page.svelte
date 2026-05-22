<script lang="ts">
  import { onMount } from 'svelte';
  import KeyRecorder from '$lib/components/KeyRecorder.svelte';
  import KeyBadge from '$lib/components/KeyBadge.svelte';
  import {
    getApplications, createApplication, deleteApplication,
    getCategories, createCategory, deleteCategory,
    getShortcuts, createShortcut, updateShortcut, deleteShortcut,
    type Application, type ShortcutCategory, type Shortcut,
  } from '$lib/api';

  // --- State ---
  let apps = $state<Application[]>([]);
  let categories = $state<ShortcutCategory[]>([]);
  let shortcuts = $state<Shortcut[]>([]);

  let selectedApp = $state<Application | null>(null);
  let selectedCategory = $state<ShortcutCategory | null>(null);

  let loadingApps = $state(true);
  let loadingCategories = $state(false);
  let loadingShortcuts = $state(false);

  let appError = $state('');
  let categoryError = $state('');
  let shortcutError = $state('');

  // --- App form ---
  let newAppName = $state('');
  let newAppColor = $state('#6366f1');
  let submittingApp = $state(false);

  // --- Category form ---
  let newCategoryName = $state('');
  let submittingCategory = $state(false);

  // --- Shortcut form ---
  let newShortcutName = $state('');
  let newShortcutKeys = $state<string[]>([]);
  let submittingShortcut = $state(false);

  // --- Edit shortcut ---
  let editingShortcut = $state<Shortcut | null>(null);
  let editName = $state('');
  let editKeys = $state<string[]>([]);
  let submittingEdit = $state(false);
  let editError = $state('');

  function startEdit(sc: Shortcut) {
    editingShortcut = sc;
    editName = sc.name;
    editKeys = [...sc.keystrokes];
    editError = '';
  }

  function cancelEdit() {
    editingShortcut = null;
    editName = '';
    editKeys = [];
    editError = '';
  }

  async function handleSaveEdit(sc: Shortcut) {
    if (!editName.trim() || editKeys.length === 0) return;
    submittingEdit = true;
    editError = '';
    const res = await updateShortcut(sc.shortcut_id, { name: editName.trim(), keystrokes: editKeys });
    if (res.ok) {
      shortcuts = shortcuts.map(s => s.shortcut_id === sc.shortcut_id ? res.data : s);
      cancelEdit();
    } else {
      editError = res.error;
    }
    submittingEdit = false;
  }

  // --- Load functions ---
  async function loadApps() {
    loadingApps = true;
    const res = await getApplications();
    if (res.ok) apps = res.data;
    else appError = res.error;
    loadingApps = false;
  }

  async function loadCategories(app: Application) {
    loadingCategories = true;
    categories = [];
    shortcuts = [];
    selectedCategory = null;
    const res = await getCategories(app.application_id);
    if (res.ok) categories = res.data;
    else categoryError = res.error;
    loadingCategories = false;
  }

  async function loadShortcuts(category: ShortcutCategory) {
    loadingShortcuts = true;
    shortcuts = [];
    const res = await getShortcuts(category.category_id);
    if (res.ok) shortcuts = res.data;
    else shortcutError = res.error;
    loadingShortcuts = false;
  }

  // --- Select handlers ---
  function selectApp(app: Application) {
    selectedApp = app;
    categoryError = '';
    shortcutError = '';
    loadCategories(app);
  }

  function selectCategory(cat: ShortcutCategory) {
    selectedCategory = cat;
    shortcutError = '';
    loadShortcuts(cat);
  }

  // --- Create handlers ---
  async function handleCreateApp(e: SubmitEvent) {
    e.preventDefault();
    if (!newAppName.trim()) return;
    submittingApp = true;
    appError = '';
    const res = await createApplication(newAppName.trim(), newAppColor);
    if (res.ok) {
      apps = [...apps, res.data];
      newAppName = '';
      newAppColor = '#6366f1';
    } else {
      appError = res.error;
    }
    submittingApp = false;
  }

  async function handleCreateCategory(e: SubmitEvent) {
    e.preventDefault();
    if (!newCategoryName.trim() || !selectedApp) return;
    submittingCategory = true;
    categoryError = '';
    const res = await createCategory(newCategoryName.trim(), selectedApp.application_id);
    if (res.ok) {
      categories = [...categories, res.data];
      newCategoryName = '';
    } else {
      categoryError = res.error;
    }
    submittingCategory = false;
  }

  async function handleCreateShortcut(e: SubmitEvent) {
    e.preventDefault();
    if (!newShortcutName.trim() || !selectedCategory || newShortcutKeys.length === 0) return;
    submittingShortcut = true;
    shortcutError = '';
    const res = await createShortcut(newShortcutName.trim(), newShortcutKeys, selectedCategory.category_id);
    if (res.ok) {
      shortcuts = [...shortcuts, res.data];
      newShortcutName = '';
      newShortcutKeys = [];
    } else {
      shortcutError = res.error;
    }
    submittingShortcut = false;
  }

  // --- Delete handlers ---
  async function handleDeleteApp(app: Application) {
    const res = await deleteApplication(app.application_id);
    if (res.ok) {
      apps = apps.filter(a => a.application_id !== app.application_id);
      if (selectedApp?.application_id === app.application_id) {
        selectedApp = null;
        categories = [];
        shortcuts = [];
        selectedCategory = null;
      }
    }
  }

  async function handleDeleteCategory(cat: ShortcutCategory) {
    const res = await deleteCategory(cat.category_id);
    if (res.ok) {
      categories = categories.filter(c => c.category_id !== cat.category_id);
      if (selectedCategory?.category_id === cat.category_id) {
        selectedCategory = null;
        shortcuts = [];
      }
    }
  }

  async function handleDeleteShortcut(sc: Shortcut) {
    const res = await deleteShortcut(sc.shortcut_id);
    if (res.ok) shortcuts = shortcuts.filter(s => s.shortcut_id !== sc.shortcut_id);
  }

  onMount(loadApps);
</script>

<svelte:head>
  <title>keystrokes — admin</title>
</svelte:head>

<div data-theme="dim" style="min-height: 100vh;" class="flex flex-col">
  <!-- Navbar -->
  <div class="navbar bg-base-200 border-b border-base-300 px-4">
    <div class="flex-1 flex items-center gap-2">
      <span class="text-lg font-medium">keybinds</span>
      <span class="text-base-content/40 text-sm">admin panel</span>
    </div>
    <a href="/" class="btn btn-ghost btn-sm">View site</a>
    <a href="/admin" class="btn btn-ghost btn-sm">Logout</a>
  </div>

  <!-- 3-column layout -->
  <div class="flex flex-1 divide-x divide-base-300 overflow-hidden">

    <!-- Applications -->
    <div class="flex flex-col w-72 min-w-72 overflow-y-auto">
      <div class="p-4 border-b border-base-300">
        <h2 class="font-semibold text-sm uppercase tracking-widest text-base-content/60 mb-3">
          Applications
        </h2>
        <form onsubmit={handleCreateApp} class="flex flex-col gap-2">
          <input
            type="text"
            placeholder="App name"
            class="input input-sm input-bordered w-full"
            bind:value={newAppName}
            required
          />
          <div class="flex gap-2 items-center">
            <input type="color" class="w-8 h-8 rounded cursor-pointer border border-base-300" bind:value={newAppColor} />
            <span class="text-xs text-base-content/50">Color</span>
          </div>
          {#if appError}
            <p class="text-error text-xs">{appError}</p>
          {/if}
          <button type="submit" class="btn btn-sm btn-primary w-full" disabled={submittingApp}>
            {#if submittingApp}<span class="loading loading-spinner loading-xs"></span>{/if}
            Add application
          </button>
        </form>
      </div>

      <div class="flex flex-col p-2 gap-1">
        {#if loadingApps}
          <div class="flex justify-center p-4"><span class="loading loading-spinner"></span></div>
        {:else}
          {#each apps as app}
            <div
              role="button"
              tabindex="0"
              class="flex items-center justify-between px-3 py-2 rounded-lg text-sm cursor-pointer transition-colors
                {selectedApp?.application_id === app.application_id ? 'bg-primary/20 text-primary' : 'hover:bg-base-200'}"
              onclick={() => selectApp(app)}
              onkeydown={(e) => e.key === 'Enter' && selectApp(app)}
            >
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full shrink-0" style="background:{app.color}"></span>
                <span class="truncate">{app.name}</span>
              </div>
              <button
                class="btn btn-ghost btn-xs opacity-40 hover:opacity-100 hover:btn-error"
                onclick={(e) => { e.stopPropagation(); handleDeleteApp(app); }}
              >✕</button>
            </div>
          {:else}
            <p class="text-xs text-base-content/40 text-center py-4">No applications yet</p>
          {/each}
        {/if}
      </div>
    </div>

    <!-- Categories -->
    <div class="flex flex-col w-72 min-w-72 overflow-y-auto">
      <div class="p-4 border-b border-base-300">
        <h2 class="font-semibold text-sm uppercase tracking-widest text-base-content/60 mb-3">
          Categories {#if selectedApp}<span class="normal-case font-normal">— {selectedApp.name}</span>{/if}
        </h2>
        {#if selectedApp}
          <form onsubmit={handleCreateCategory} class="flex flex-col gap-2">
            <input
              type="text"
              placeholder="Category name"
              class="input input-sm input-bordered w-full"
              bind:value={newCategoryName}
              required
            />
            {#if categoryError}
              <p class="text-error text-xs">{categoryError}</p>
            {/if}
            <button type="submit" class="btn btn-sm btn-primary w-full" disabled={submittingCategory}>
              {#if submittingCategory}<span class="loading loading-spinner loading-xs"></span>{/if}
              Add category
            </button>
          </form>
        {:else}
          <p class="text-xs text-base-content/40">Select an application first</p>
        {/if}
      </div>

      <div class="flex flex-col p-2 gap-1">
        {#if loadingCategories}
          <div class="flex justify-center p-4"><span class="loading loading-spinner"></span></div>
        {:else if selectedApp}
          {#each categories as cat}
            <div
              role="button"
              tabindex="0"
              class="flex items-center justify-between px-3 py-2 rounded-lg text-sm cursor-pointer transition-colors
                {selectedCategory?.category_id === cat.category_id ? 'bg-primary/20 text-primary' : 'hover:bg-base-200'}"
              onclick={() => selectCategory(cat)}
              onkeydown={(e) => e.key === 'Enter' && selectCategory(cat)}
            >
              <span class="truncate">{cat.name}</span>
              <button
                class="btn btn-ghost btn-xs opacity-40 hover:opacity-100 hover:btn-error"
                onclick={(e) => { e.stopPropagation(); handleDeleteCategory(cat); }}
              >✕</button>
            </div>
          {:else}
            <p class="text-xs text-base-content/40 text-center py-4">No categories yet</p>
          {/each}
        {/if}
      </div>
    </div>

    <!-- Shortcuts -->
    <div class="flex flex-col flex-1 overflow-y-auto">
      <div class="p-4 border-b border-base-300">
        <h2 class="font-semibold text-sm uppercase tracking-widest text-base-content/60 mb-3">
          Shortcuts {#if selectedCategory}<span class="normal-case font-normal">— {selectedCategory.name}</span>{/if}
        </h2>
        {#if selectedCategory}
          <form onsubmit={handleCreateShortcut} class="flex flex-col gap-3">
            <input
              type="text"
              placeholder="Shortcut name"
              class="input input-sm input-bordered w-full"
              bind:value={newShortcutName}
              required
            />
            <div class="bg-base-200 rounded-lg p-3">
              <p class="text-xs text-base-content/50 mb-2">Keystrokes</p>
              <KeyRecorder
                keys={newShortcutKeys}
                onchange={(k) => newShortcutKeys = k}
              />
            </div>
            {#if shortcutError}
              <p class="text-error text-xs">{shortcutError}</p>
            {/if}
            <button
              type="submit"
              class="btn btn-sm btn-primary"
              disabled={submittingShortcut || newShortcutKeys.length === 0}
            >
              {#if submittingShortcut}<span class="loading loading-spinner loading-xs"></span>{/if}
              Add shortcut
            </button>
          </form>
        {:else}
          <p class="text-xs text-base-content/40">Select a category first</p>
        {/if}
      </div>

      <div class="p-4 flex flex-col gap-2">
        {#if loadingShortcuts}
          <div class="flex justify-center p-4"><span class="loading loading-spinner"></span></div>
        {:else if selectedCategory}
          {#each shortcuts as sc}
            {#if editingShortcut?.shortcut_id === sc.shortcut_id}
              <div class="flex flex-col gap-2 bg-base-200 rounded-lg px-3 py-3">
                <input
                  type="text"
                  class="input input-sm input-bordered w-full"
                  bind:value={editName}
                />
                <div class="bg-base-300 rounded-lg p-3">
                  <p class="text-xs text-base-content/50 mb-2">Keystrokes</p>
                  <KeyRecorder
                    keys={editKeys}
                    onchange={(k) => editKeys = k}
                  />
                </div>
                {#if editError}
                  <p class="text-error text-xs">{editError}</p>
                {/if}
                <div class="flex gap-2">
                  <button
                    class="btn btn-sm btn-primary flex-1"
                    disabled={submittingEdit || editKeys.length === 0 || !editName.trim()}
                    onclick={() => handleSaveEdit(sc)}
                  >
                    {#if submittingEdit}<span class="loading loading-spinner loading-xs"></span>{/if}
                    Save
                  </button>
                  <button class="btn btn-sm btn-ghost" onclick={cancelEdit}>Cancel</button>
                </div>
              </div>
            {:else}
              <div class="flex items-center justify-between bg-base-200 rounded-lg px-3 py-2">
                <div class="flex flex-col gap-1">
                  <span class="text-sm">{sc.name}</span>
                  <div class="flex gap-1 flex-wrap">
                    {#each sc.keystrokes as key}
                      <KeyBadge {key} />
                    {/each}
                  </div>
                </div>
                <div class="flex gap-1">
                  <button
                    class="btn btn-ghost btn-xs opacity-40 hover:opacity-100"
                    onclick={() => startEdit(sc)}
                  >✎</button>
                  <button
                    class="btn btn-ghost btn-xs opacity-40 hover:opacity-100 hover:btn-error"
                    onclick={() => handleDeleteShortcut(sc)}
                  >✕</button>
                </div>
              </div>
            {/if}
          {:else}
            <p class="text-xs text-base-content/40 text-center py-4">No shortcuts yet</p>
          {/each}
        {/if}
      </div>
    </div>
  </div>
</div>
