import api from '@/services/api';

export default {
    namespaced: true,
    state: {
        user: JSON.parse(localStorage.getItem('user')) || null,
        token: localStorage.getItem('token') || null,
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
            localStorage.setItem('user', JSON.stringify(user));
        },
        SET_TOKEN(state, token) {
            state.token = token;
            if (token) {
                localStorage.setItem('token', token);
            } else {
                localStorage.removeItem('token');
            }
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
        },
        async refreshToken({ commit, state }) {
            if (!state.token) return { success: false };
            try {
                const response = await api.post('auth/token/refresh/', {
                    refresh: state.token,
                });
                commit('SET_TOKEN', response.data.access);
                return { success: true };
            } catch (error) {
                console.error('Token refresh error:', error);
                commit('SET_USER', null);
                commit('SET_TOKEN', null);
                return { success: false };
            }
        },
        setTokenRefreshTimer({ dispatch }) {
            setInterval(() => {
                dispatch('refreshToken');
            }, 30 * 60 * 1000); // 4분마다 갱신 (토큰 만료 시간에 따라 조정 필요)
        },
        async checkAuth({ commit, state, dispatch }) {
            if (!state.token) return;
            try {
                const response = await api.get('user/me'); // 사용자 정보를 가져오는 API 엔드포인트
                commit('SET_USER', response.data);
                dispatch('setTokenRefreshTimer');
            } catch (error) {
                console.error('Auth check error:', error);
                commit('SET_USER', null);
                commit('SET_TOKEN', null);
            }
        },
    },
    getters: {
        isAuthenticated: (state) => !!state.token,
        currentUser: (state) => state.user,
    },
};
