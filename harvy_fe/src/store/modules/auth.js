import api from '@/services/api';

export default {
    namespaced: true,
    state: {
        user: null,
        isAuthenticated: false,
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
            state.isAuthenticated = !!user;
        },
    },
    actions: {
        async signup({ commit }, userData) {
            try {
                const response = await api.post('users/', userData);
                commit('SET_USER', response.data.user);
                return { success: true, data: response.data };
            } catch (error) {
                console.error('Signup error:', error.response?.data);
                return {
                    success: false,
                    message: error.response?.data?.message || '회원가입에 실패했습니다.',
                    errors: error.response?.data || {},
                };
            }
        },
    },
    getters: {
        isAuthenticated: (state) => !!state.user,
        currentUser: (state) => state.user,
    },
};
