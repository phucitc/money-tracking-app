// CSS
import '../scss/bootstrap.scss'
import './assets/style.css'

// JS
// import * as bootstrap from 'bootstrap'
// import 'bootstrap/dist/js/bootstrap.bundle.min.js'
// import '@popperjs/core/dist/umd/popper.min.js'

import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './ultils/store'
import {createAuth0} from '@auth0/auth0-vue';

const app = createApp(App)
app.config.globalProperties.msg = 'Hello, world!'
app.config.globalProperties.appData = {}

app.use(
    createAuth0({
        domain: import.meta.env.VITE_AUTH0_DOMAIN,
        clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
        authorizationParams: {
            redirect_uri: import.meta.env.VITE_AUTH0_REDIRECT_URI,
        }
    })
);

app.use(router)
app.use(store)

app.mount('#app')
