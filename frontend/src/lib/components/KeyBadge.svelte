<script lang="ts">
  type Props = { key: string; size?: 'sm' | 'md' };
  let { key, size = 'sm' }: Props = $props();

  const SYMBOLS: Record<string, string> = {
    arrow_up: '↑', arrow_down: '↓', arrow_left: '←', arrow_right: '→',
    shift: '⇧', left_shift: '⇧', right_shift: '⇧',
    ctrl: 'Ctrl', left_ctrl: 'Ctrl', right_ctrl: 'Ctrl',
    alt: 'Alt', left_alt: 'Alt', right_alt: 'Alt',
    meta: '⌘', left_meta: '⌘', right_meta: '⌘',
    enter: '↩', numpad_enter: '↩',
    backspace: '⌫', delete: '⌦',
    tab: '⇥', escape: 'Esc', space: '␣',
    caps_lock: '⇪', num_lock: 'NumLk', scroll_lock: 'ScrLk',
    home: 'Home', end: 'End', page_up: 'PgUp', page_down: 'PgDn', insert: 'Ins',
    print_screen: 'PrtSc', pause: 'Pause', context_menu: '☰',
    mouse_left: 'M1', mouse_right: 'M2', mouse_middle: 'M3',
    mouse_x1: 'M4', mouse_x2: 'M5',
    mouse_wheel_up: 'WheelUp', mouse_wheel_down: 'WheelDn',
    numpad_add: 'Num+', numpad_subtract: 'Num−', numpad_multiply: 'Num×',
    numpad_divide: 'Num÷', numpad_decimal: 'Num.',
  };

  const NUMPAD_DIGITS: Record<string, string> = {
    numpad_0: 'Num0', numpad_1: 'Num1', numpad_2: 'Num2', numpad_3: 'Num3',
    numpad_4: 'Num4', numpad_5: 'Num5', numpad_6: 'Num6', numpad_7: 'Num7',
    numpad_8: 'Num8', numpad_9: 'Num9',
  };

  function display(k: string): string {
    if (SYMBOLS[k]) return SYMBOLS[k];
    if (NUMPAD_DIGITS[k]) return NUMPAD_DIGITS[k];
    if (/^f\d{1,2}$/.test(k)) return k.toUpperCase();
    if (k.length === 1) return k.toUpperCase();
    return k;
  }

  let label = $derived(display(key));

  // Wider badge for longer labels
  let wide = $derived(label.length > 2);
</script>

<kbd
  class="kbd font-mono font-medium {size === 'sm' ? 'kbd-sm' : ''} {wide ? 'px-2' : ''}"
>
  {label}
</kbd>
