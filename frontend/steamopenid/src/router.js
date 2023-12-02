import Login from './views/Login.vue';
import FourOFour from './views/404.vue';
import Dashboard from './views/Dashboard.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter: (to, from, next) => {
        if (!checkIfLoggedIn()) {
          next();
        } else {
          next({ name: 'dashboard' });
        }
      },
    },
    {
      path: '/404',
      name: '404',
      component: FourOFour,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      beforeEnter: (to, from, next) => {
        if (checkIfLoggedIn()) {
          next();
        } else {
          next({ name: 'login' });
        }
      },
    },
  ],
});

function checkIfLoggedIn() {
  return !!localStorage.getItem('access_token');
}

export default router;
