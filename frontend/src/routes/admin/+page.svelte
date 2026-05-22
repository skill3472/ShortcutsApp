<script lang="ts">
  import { login } from '$lib/api';

  let username = $state('');
  let password = $state('');
  let error = $state('');
  let loading = $state(false);

  async function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    error = '';
    loading = true;

    const result = await login(username, password);
    if (result.ok) {
      window.location.href = '/admin/panel';
    } else {
      error = result.error;
    }

    loading = false;
  }
</script>

<div data-theme="dim" style="min-height: 100vh;" class="flex items-center justify-center bg-base-200">
  <div class="card w-full max-w-sm bg-base-100 shadow-xl">
    <div class="card-body gap-4">
      <h2 class="card-title text-xl justify-center">Admin Login</h2>

      <form onsubmit={handleSubmit} class="flex flex-col gap-3">
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Username</span></div>
          <input
            type="text"
            placeholder="admin"
            class="input input-bordered w-full"
            autocomplete="username"
            bind:value={username}
            required
          />
        </label>

        <label class="form-control w-full">
          <div class="label"><span class="label-text">Password</span></div>
          <input
            type="password"
            placeholder="••••••••"
            class="input input-bordered w-full"
            autocomplete="current-password"
            bind:value={password}
            required
          />
        </label>

        {#if error}
          <div class="alert alert-error py-2 text-sm">{error}</div>
        {/if}

        <button type="submit" class="btn btn-primary w-full mt-1" disabled={loading}>
          {#if loading}
            <span class="loading loading-spinner loading-sm"></span>
          {/if}
          Sign in
        </button>
      </form>
    </div>
  </div>
</div>