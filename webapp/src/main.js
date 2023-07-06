import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createAuth0 } from '@auth0/auth0-vue';

const app = createApp(App)

app.use(
  createAuth0({
    domain: "dev-e0hn8bw4osg50wqz.us.auth0.com",
    clientId: "gsV2RRopEbPsVoz1R5XcpVPNtXgM1Uhb",
    authorizationParams: {
      redirect_uri: 'http://localhost:5000/callback',
    }
  })
);

app.use(router)

app.mount('#app')
