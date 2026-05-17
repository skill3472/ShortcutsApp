export type Binding = {
  label: string;
  keys: string[];
};

export type Category = {
  title: string;
  bindings: Binding[];
};

export type App = {
  id: string;
  label: string;
  labelColor: string;
  categories: Category[];
};