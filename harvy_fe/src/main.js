import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUser, faPhone, faEnvelope, faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faUser, faPhone, faEnvelope, faMapMarkerAlt);

const app = createApp(App);

app.component('font-awesome-icon', FontAwesomeIcon);

app.use(router).mount('#app');
