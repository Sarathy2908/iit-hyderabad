import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
    },
    {
      path: '/case/new',
      name: 'new-case',
      component: () => import('../views/NewCase.vue'),
    },
    {
      path: '/case/:id',
      name: 'case-detail',
      component: () => import('../views/CaseDetail.vue'),
      children: [
        {
          path: 'notes',
          name: 'case-notes',
          component: () => import('../views/QualitativeNotes.vue'),
        },
        {
          path: 'cam',
          name: 'case-cam',
          component: () => import('../views/CAMViewer.vue'),
        }
      ]
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminPanel.vue'),
    }
  ],
})

export default router
