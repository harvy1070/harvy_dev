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
        async login({ commit, dispatch }, credentials) {
            try {
                const data = await api.login(credentials);
                commit('SET_USER', data.user);
                commit('SET_TOKEN', data.access);
                dispatch('setTokenRefreshTimer');
                return { success: true };
            } catch (error) {
                console.error('Login error:', error.response?.data || error.message);
                return {
                    success: false,
                    message: error.response?.data?.error || '로그인에 실패했습니다.',
                };
            }
        },
        async signup({ commit }, formData) {
            try {
                console.log('Sending signup data:', formData);
                const response = await api.signup(formData);

                console.log('Full server response:', response);

                if (response && response.user) {
                    // 서버 응답 구조에 따라 수정 필요
                    commit('SET_USER', response.user);
                    if (response.access) {
                        commit('SET_TOKEN', response.access);
                    }
                    return { success: true, message: '회원가입 성공' };
                } else {
                    throw new Error(response.message || '회원가입에 실패했습니다.');
                }
            } catch (error) {
                console.error('Signup error:', error);

                if (error.response) {
                    console.error('Server error response:', error.response.data);
                    return {
                        success: false,
                        message:
                            error.response.data.detail || error.response.data.message || '회원가입에 실패했습니다.',
                        errors: error.response.data,
                    };
                } else if (error.request) {
                    console.error('No response received:', error.request);
                    return {
                        success: false,
                        message: '서버에 연결할 수 없습니다. 네트워크 연결을 확인해 주세요.',
                    };
                } else {
                    console.error('Error:', error.message);
                    return {
                        success: false,
                        message: '요청 중 오류가 발생했습니다: ' + error.message,
                    };
                }
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
