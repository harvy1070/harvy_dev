import api from '@/services/api';

export default {
    namespaced: true,
    state: {
        user: null,
        token: null,
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
        },
        SET_TOKEN(state, token) {
            state.token = token;
        },
    },
    actions: {
        async signup(_, userData) {
            try {
                const response = await api.post('users/', userData);
                return { success: true, data: response.data, message: '회원가입이 완료되었습니다.' };
            } catch (error) {
                console.error('Signup error:', error.response?.data);
                return {
                    success: false,
                    message: error.response?.data?.message || '회원가입에 실패했습니다.',
                };
            }
        },
        async login({ commit, dispatch }, { user_id, password }) {
            try {
                console.log('Attempting login with:', { user_id });
                const response = await api.post('auth/login/', { user_id, password });
                console.log('Login response:', response.data);
                if (response.data.access) {
                    commit('SET_USER', response.data.user);
                    commit('SET_TOKEN', response.data.access);
                    localStorage.setItem('token', response.data.access);
                    dispatch('setTokenRefreshTimer');
                    return { success: true };
                } else {
                    throw new Error('Access token not found in response');
                }
            } catch (error) {
                console.error('Login error:', error.response?.data || error.message);
                return {
                    success: false,
                    message: error.response?.data?.error || '로그인에 실패했습니다.',
                };
            }
        },
        logout({ commit }) {
            commit('SET_USER', null);
            commit('SET_TOKEN', null);
            localStorage.removeItem('token');
        },
        async refreshToken({ commit }) {
            try {
                const response = await api.post('auth/token/refresh/', {
                    refresh: localStorage.getItem('refresh_token'),
                });
                commit('SET_TOKEN', response.data.access);
                localStorage.setItem('token', response.data.access);
                return { success: true };
            } catch (error) {
                console.error('Token refresh error:', error);
                return { success: false };
            }
        },
        setTokenRefreshTimer({ dispatch }) {
            setInterval(() => {
                dispatch('refreshToken');
            }, 30 * 60 * 1000);
        },
        initializeAuth({ commit, dispatch }) {
            const token = localStorage.getItem('token');
            if (token) {
                commit('SET_TOKEN', token);
                dispatch('setTokenRefreshTimer');
            }
        },
    },
    getters: {
        isAuthenticated: (state) => !!state.token,
        currentUser: (state) => state.user,
    },
};
