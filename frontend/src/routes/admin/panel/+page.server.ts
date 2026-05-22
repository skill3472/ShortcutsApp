import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = ({ cookies }) => {
  if (!cookies.get('session')) {
    redirect(302, '/admin');
  }
};
