import { createStore } from 'vuex';

const store = createStore({
  state: {
    myVariable: 'Hello, world!', // Define your global variable here
    isAuth: false,
    accessToken: '',
  },
  mutations: {
    setMyVariable(state, value) {
      state.myVariable = value;
    },
    setIsAuth(state, value) {
      state.isAuth = value;
    },
    setAccessToken(state, value) {
      state.accessToken = value;
    },
  },
  actions: {
    updateMyVariable({ commit }, value) {
      commit('setMyVariable', value);
    },
    updateIsAuth({ commit }, value) {
      commit('setIsAuth', value);
    },
    updateAccessToken({ commit }, value) {
      commit('setAccessToken', value);
    },
  },
  getters: {
    getMyVariable: (state) => state.myVariable,
    getIsAuth: (state) => state.isAuth,
    getAccessToken: (state) => state.accessToken,
  },
});

export default store;