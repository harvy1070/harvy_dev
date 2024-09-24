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
                // api 객체의 baseURL 설정을 확인하고, 필요하다면 전체 URL을 사용
                const response = await api.signup(formData);

                if (response.data.success) {
                    commit('SET_USER', response.data.user);
                    commit('SET_TOKEN', response.data.access);
                    return { success: true, message: '회원가입 성공' };
                } else {
                    throw new Error(response.data.message || '회원가입에 실패했습니다.');
                }
            } catch (error) {
                console.error('Signup error:', error);

                if (error.response) {
                    // 서버에서 응답은 왔지만 상태 코드가 2xx가 아닌 경우
                    console.error('Server responded with:', error.response.status, error.response.data);
                    return {
                        success: false,
                        message:
                            error.response.data.detail || error.response.data.message || '회원가입에 실패했습니다.',
                    };
                } else if (error.request) {
                    // 요청은 보냈지만 응답을 받지 못한 경우
                    console.error('No response received:', error.request);
                    return {
                        success: false,
                        message: '서버에 연결할 수 없습니다. 네트워크 연결을 확인해 주세요.',
                    };
                } else {
                    // 요청 설정 중 오류가 발생한 경우
                    console.error('Error setting up the request:', error.message);
                    return {
                        success: false,
                        message: '요청 중 오류가 발생했습니다.',
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
