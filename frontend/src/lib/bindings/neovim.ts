import type { App } from './bindings.types';

export const neovim: App = {
  id: 'neovim',
  label: 'Neovim',
  labelColor: 'bg-green-500 text-white border-green-500',
  categories: [
    {
      title: 'Navigation',
      bindings: [
        { label: 'move left / down / up / right', keys: ['h', 'j', 'k', 'l'] },
        { label: 'jump to line start',             keys: ['0'] },
        { label: 'jump to line end',               keys: ['$'] },
        { label: 'go to file top',                 keys: ['gg'] },
        { label: 'go to file bottom',              keys: ['G'] },
        { label: 'next word',                      keys: ['w'] },
        { label: 'previous word',                  keys: ['b'] },
      ],
    },
    {
      title: 'Editing',
      bindings: [
        { label: 'insert mode',           keys: ['i'] },
        { label: 'insert at end of line', keys: ['A'] },
        { label: 'new line below',        keys: ['o'] },
        { label: 'delete char',           keys: ['x'] },
        { label: 'delete line',           keys: ['dd'] },
        { label: 'yank line',             keys: ['yy'] },
        { label: 'paste below',           keys: ['p'] },
      ],
    },
    {
      title: 'Buffers & Windows',
      bindings: [
        { label: 'next buffer',       keys: [']', 'b'] },
        { label: 'close buffer',      keys: ['leader', 'bd'] },
        { label: 'split horizontal',  keys: ['ctrl', 'w', 's'] },
        { label: 'split vertical',    keys: ['ctrl', 'w', 'v'] },
        { label: 'focus next window', keys: ['ctrl', 'w', 'w'] },
      ],
    },
    {
      title: 'Search & Replace',
      bindings: [
        { label: 'search forward',     keys: ['/'] },
        { label: 'search backward',    keys: ['?'] },
        { label: 'next match',         keys: ['n'] },
        { label: 'prev match',         keys: ['N'] },
        { label: 'substitute in line', keys: [':s/old/new'] },
        { label: 'substitute in file', keys: [':%s/old/new/g'] },
      ],
    },
  ],
};