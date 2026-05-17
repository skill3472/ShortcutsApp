import type { App } from './bindings.types';

export const tmux: App = {
  id: 'tmux',
  label: 'tmux',
  labelColor: 'bg-blue-500 text-white border-blue-500',
  categories: [
    {
      title: 'Sessions',
      bindings: [
        { label: 'new session',    keys: ['prefix', ':new'] },
        { label: 'list sessions',  keys: ['prefix', 's'] },
        { label: 'rename session', keys: ['prefix', '$'] },
        { label: 'detach',         keys: ['prefix', 'd'] },
      ],
    },
    {
      title: 'Windows',
      bindings: [
        { label: 'new window',     keys: ['prefix', 'c'] },
        { label: 'next window',    keys: ['prefix', 'n'] },
        { label: 'prev window',    keys: ['prefix', 'p'] },
        { label: 'rename window',  keys: ['prefix', ','] },
        { label: 'close window',   keys: ['prefix', '&'] },
      ],
    },
    {
      title: 'Panes',
      bindings: [
        { label: 'split horizontal', keys: ['prefix', '"'] },
        { label: 'split vertical',   keys: ['prefix', '%'] },
        { label: 'close pane',       keys: ['prefix', 'x'] },
        { label: 'move between panes', keys: ['prefix', 'arrow'] },
        { label: 'zoom pane',        keys: ['prefix', 'z'] },
      ],
    },
  ],
};