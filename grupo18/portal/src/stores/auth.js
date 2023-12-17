const { apiService } = await import("../api");

const state = {
  user: {}, //trabaja con el usuario "completo"
  isLoggedIn: false,
};

const getters = {
  isLoggedIn: (state) => state.isLoggedIn,
  user: (state) => state.user,
};

const actions = {
  async login({ dispatch }, user) {
    const response = await apiService.post("/api/auth/login_jwt", user);
      await dispatch("fetchUser");
      const accessToken = response.data.access_token;
      localStorage.setItem("access_token", accessToken);
  },
  async fetchUser({ commit }) {
    await apiService.get("/api/me/profile").then(({ data }) => commit("setUser", data));
  },
  async logout({ commit }) {
    await apiService.get("/api/auth/logout_jwt");
    commit("logoutUserState");
    localStorage.removeItem('access_token')
  },
};

const mutations = {
  setUser(state, user) {
    state.user = user;
    state.isLoggedIn = true;
  },
  logoutUserState(state) {
    state.user = {};
    state.isLoggedIn = false;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};