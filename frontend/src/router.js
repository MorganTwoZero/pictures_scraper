import { createRouter, createWebHashHistory } from 'vue-router'
import { useStore } from '@/store'

import PostsView from './views/PostsView.vue'
import AboutView from './views/AboutView.vue'

const routes = [
  {
    path: '',
    redirect: 'honkai',
  },
  {
    path: '/honkai',
    name: 'honkai',
    component: PostsView,
    meta: {title: 'Honkai'},
  },
  {
    path: '/homeline',
    name: 'homeline',
    component: PostsView,
    meta: {title: 'Homeline'},
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: {title: 'About'},
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('./views/LoginView.vue'),
    meta: {title: 'Login'},
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('./views/RegisterView.vue'),
    meta: {title: 'Register'},
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('./views/UserView.vue'),
    meta: {title: 'User'},
  },
  {
    path: '/:catchAll(.*)', redirect: '/' 
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

const DEFAULT_TITLE = 'Картиночки';
router.afterEach((to) => {
    // Use next tick to handle router history correctly
    // see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
        document.title = to.meta.title || DEFAULT_TITLE;
});

export default router

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/user'];
  const authRequired = publicPages.includes(to.path);
  const store = useStore();
  const loggedIn = store.isAuthenticated;

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
})