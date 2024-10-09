import api from '@/services/api';

export default {
    namespaced: true,
    state: {
        messages: [],
        sessionId: null,
    },
    mutations: {
        SET_MESSAGES(state, messages) {
            state.messages = messages;
        },
        ADD_MESSAGE(state, message) {
            state.messages.push(message);
        },
        SET_SESSION_ID(state, sessionId) {
            state.sessionId = sessionId;
        },
    },
    actions: {
        async initSession({ commit }) {
            try {
                const response = await api.post('/chatbot/session/');
                commit('SET_SESSION_ID', response.data.session_id);
            } catch (error) {
                console.error('세션 초기화 오류:', error);
            }
        },
        async sendMessageToBackend({ commit, state }, { message }) {
            try {
                commit('ADD_MESSAGE', { isUser: true, user_message: message });
                const response = await api.post(`/chatbot/message/${state.sessionId}/`, { message });
                commit('ADD_MESSAGE', { isUser: false, gpt_message: response.data.response });
            } catch (error) {
                console.error('메시지 전송 오류 발생:', error);
            }
        },
    },
};
