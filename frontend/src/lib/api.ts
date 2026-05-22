import type { components } from './api.types';

// Types derived from generated OpenAPI schema — run `pnpm gen:types` to regenerate
export type Application = components['schemas']['Application'];
export type ShortcutCategory = components['schemas']['ShortcutCategory'];
export type Shortcut = components['schemas']['Shortcut'];
export type UpdateShortcut = components['schemas']['UpdateShortcut'];

type ApiResult<T = void> =
  | { ok: true; data: T }
  | { ok: false; error: string };

async function request<T = void>(
  method: string,
  path: string,
  body?: unknown
): Promise<ApiResult<T>> {
  try {
    const res = await fetch(`/api${path}`, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (res.status === 401) {
      window.location.href = '/admin';
      return { ok: false, error: 'Unauthorized' };
    }

    if (res.ok) {
      const data = res.status === 204 ? undefined : await res.json().catch(() => undefined);
      return { ok: true, data: data as T };
    }

    if (res.status >= 500) {
      return { ok: false, error: 'Could not reach the server. Is the API running?' };
    }

    const data = await res.json().catch(() => ({}));
    return { ok: false, error: data.detail ?? 'Request failed.' };
  } catch {
    return { ok: false, error: 'Could not reach the server. Is the API running?' };
  }
}

const post = <T = void>(path: string, body: unknown) => request<T>('POST', path, body);
const get = <T>(path: string) => request<T>('GET', path);
const del = (path: string) => request('DELETE', path);

// Auth
export const login = (username: string, password: string) =>
  post('/admin/login', { username, password });

// Applications
export const getApplications = () => get<Application[]>('/shortcuts/applications');
export const createApplication = (name: string, color: string) =>
  post<Application>('/shortcuts/applications', { name, color });
export const deleteApplication = (id: number) => del(`/shortcuts/applications/${id}`);

// Categories
export const getCategories = (appId: number) =>
  get<ShortcutCategory[]>(`/shortcuts/applications/${appId}/categories`);
export const createCategory = (name: string, app_id: number) =>
  post<ShortcutCategory>('/shortcuts/categories', { name, app_id });
export const deleteCategory = (categoryId: number) => del(`/shortcuts/categories/${categoryId}`);

// Shortcuts
export const getShortcuts = (categoryId: number) =>
  get<Shortcut[]>(`/shortcuts/categories/${categoryId}/shortcuts`);
export const createShortcut = (name: string, keystrokes: string[], category_id: number) =>
  post<Shortcut>('/shortcuts/shortcuts', { name, keystrokes, category_id });
export const updateShortcut = (shortcutId: number, body: UpdateShortcut) =>
  request<Shortcut>('PATCH', `/shortcuts/shortcuts/${shortcutId}`, body);
export const deleteShortcut = (shortcutId: number) => del(`/shortcuts/shortcuts/${shortcutId}`);
