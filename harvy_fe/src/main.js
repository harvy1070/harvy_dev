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
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');
