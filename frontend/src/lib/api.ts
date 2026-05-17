type ApiResult<T = void> =
  | { ok: true; data: T }
  | { ok: false; error: string };

async function post<T = void>(path: string, body: unknown): Promise<ApiResult<T>> {
  try {
    const res = await fetch(`/api${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

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

export async function login(username: string, password: string) {
  return post('/login', { username, password });
}
