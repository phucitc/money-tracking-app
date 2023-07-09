import {createStore} from 'vuex';

const store = createStore({
    state: {
        myVariable: 'Hello, world!', // Define your global variable here
        isAuth: false,
        token: '',
        accessToken: '',
    },
    mutations: {
        setMyVariable(state, value) {
            state.myVariable = value;
        },
        setIsAuth(state, value) {
            state.isAuth = value;
        },
        setToken(state, value) {
            state.token = value;
        },
        setAccessToken(state, value) {
            state.accessToken = value;
        }
    },
    actions: {
        updateMyVariable({commit}, value) {
            commit('setMyVariable', value);
        },
        updateIsAuth({commit}, value) {
            commit('setIsAuth', value);
        },
        updateToken({commit}, value) {
            commit('setToken', value);
        },
        updateAccessToken({commit}, value) {
            commit('setAccessToken', value);
        }
    },
    getters: {
        getMyVariable: (state) => state.myVariable,
        getIsAuth: (state) => state.isAuth,
        getToken: (state) => state.token,
        getAuth0AccessToken: (state) => state.auth0AccessToken,
    },
});

export default store;