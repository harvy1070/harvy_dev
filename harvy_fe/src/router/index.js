import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/Home.vue';
import AboutPage from '../views/About.vue';
import PortfolioPage from '../views/Portfolio.vue';
import ProjectHistoryPage from '../views/ProjectHistory.vue';
import QnAPage from '../views/QnA.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
    },
    {
        path: '/about',
        name: 'About',
        component: AboutPage,
    },
    {
        path: '/portfolio',
        name: 'Portfolio',
        component: PortfolioPage,
    },
    {
        path: '/project-history',
        name: 'ProjectHistory',
        component: ProjectHistoryPage,
    },
    {
        path: '/qna',
        name: 'QnA',
        component: QnAPage,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
