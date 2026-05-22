export type AppShortcut = {
  id: number;
  name: string;
  keystrokes: string[];
};

export type AppCategory = {
  id: number;
  name: string;
  shortcuts: AppShortcut[];
};

export type AppData = {
  id: number;
  name: string;
  color: string;
  categories: AppCategory[];
};
