import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUser, faPhone, faEnvelope, faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faUser, faPhone, faEnvelope, faMapMarkerAlt);

const app = createApp(App);

app.use(store).use(router);

// 초기 인증상태로 복원
store.dispatch('auth/initializeAuth');
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');
