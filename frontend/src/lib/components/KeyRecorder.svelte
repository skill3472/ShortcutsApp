<script lang="ts">
  import KeyBadge from './KeyBadge.svelte';

  type Props = {
    keys: string[];
    onchange: (keys: string[]) => void;
  };

  let { keys, onchange }: Props = $props();

  let recording = $state(false);

  const KEY_MAP: Record<string, string> = {
    Control: 'ctrl', Shift: 'shift', Alt: 'alt', Meta: 'meta',
    ArrowUp: 'arrow_up', ArrowDown: 'arrow_down', ArrowLeft: 'arrow_left', ArrowRight: 'arrow_right',
    Enter: 'enter', Backspace: 'backspace', Delete: 'delete', Tab: 'tab',
    Escape: 'escape', ' ': 'space', Home: 'home', End: 'end',
    PageUp: 'page_up', PageDown: 'page_down', Insert: 'insert',
    CapsLock: 'caps_lock', NumLock: 'num_lock', ScrollLock: 'scroll_lock',
    PrintScreen: 'print_screen', Pause: 'pause', ContextMenu: 'context_menu',
    '`': '`', '-': '-', '=': '=', '[': '[', ']': ']',
    '\\': '\\', ';': ';', "'": "'", ',': ',', '.': '.', '/': '/',
  };

  function mapKey(e: KeyboardEvent): string | null {
    if (KEY_MAP[e.key]) return KEY_MAP[e.key];
    if (e.key.length === 1) return e.key.toLowerCase();
    if (/^F\d{1,2}$/.test(e.key)) return e.key.toLowerCase();
    if (/^Numpad/.test(e.code)) {
      const digit = e.code.replace('Numpad', '');
      if (/^\d$/.test(digit)) return `numpad_${digit}`;
      const ops: Record<string, string> = {
        Add: 'numpad_add', Subtract: 'numpad_subtract',
        Multiply: 'numpad_multiply', Divide: 'numpad_divide',
        Decimal: 'numpad_decimal', Enter: 'numpad_enter',
      };
      return ops[digit] ?? null;
    }
    return null;
  }

  function handleKeydown(e: KeyboardEvent) {
    if (!recording) return;
    e.preventDefault();
    e.stopPropagation();
    const key = mapKey(e);
    if (key && !keys.includes(key)) {
      onchange([...keys, key]);
    }
  }

  function remove(key: string) {
    onchange(keys.filter(k => k !== key));
  }

  let customKey = $state('');

  function addCustomKey() {
    const val = customKey.trim();
    if (val && !keys.includes(val)) {
      onchange([...keys, val]);
    }
    customKey = '';
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="flex flex-col gap-2">
  <div class="flex flex-wrap gap-1 min-h-8">
    {#each keys as key}
      <div class="flex items-center gap-0.5">
        <KeyBadge {key} />
        <button
          type="button"
          class="text-xs opacity-40 hover:opacity-100 leading-none px-0.5"
          onclick={() => remove(key)}
        >✕</button>
      </div>
    {/each}
    {#if keys.length === 0}
      <span class="text-sm text-base-content/40 self-center">No keys recorded</span>
    {/if}
  </div>

  <div class="flex gap-2">
    <button
      type="button"
      class="btn btn-sm {recording ? 'btn-error' : 'btn-outline'}"
      onclick={() => recording = !recording}
    >
      {recording ? '⏹ Stop recording' : '⏺ Record keys'}
    </button>
    {#if keys.length > 0}
      <button
        type="button"
        class="btn btn-sm btn-ghost"
        onclick={() => onchange([])}
      >Clear</button>
    {/if}
  </div>

  {#if recording}
    <p class="text-xs text-base-content/50">Press keys to add them to the sequence…</p>
  {/if}

  <div class="flex gap-2 items-center">
    <input
      type="text"
      placeholder="Or type a key name (e.g. leader, SPC, gg)"
      class="input input-xs input-bordered flex-1"
      bind:value={customKey}
      onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addCustomKey(); } }}
    />
    <button type="button" class="btn btn-xs btn-outline" onclick={addCustomKey} disabled={!customKey.trim()}>
      Add
    </button>
  </div>
</div>
