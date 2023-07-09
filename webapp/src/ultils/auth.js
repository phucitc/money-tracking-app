import {useAuth0} from "@auth0/auth0-vue";

const auth = {
    autheticate: async function(user, cb) {
        const auth0 = useAuth0()
        await auth0.checkSession();
        await auth0.getAccessTokenSilently()
        if (await auth0.isAuthenticated.value) {

        }
    }
}

export default auth
