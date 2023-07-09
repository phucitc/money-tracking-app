import {useAuth0} from "@auth0/auth0-vue";
import store from "@/ultils/store";

const auth = {
    authenticate: async function() {
        const auth0 = useAuth0()
        await auth0.checkSession();
        const accessToken = await auth0.getAccessTokenSilently()
        const isAuth = await auth0.isAuthenticated.value
        if (isAuth) {
            const token = auth0.idTokenClaims.value.__raw
            store.dispatch('updateIsAuth', true)
            store.dispatch('updateAccessToken', accessToken)
            store.dispatch('updateToken', token)
            return true
        }
        return false
    }
}

export default auth
