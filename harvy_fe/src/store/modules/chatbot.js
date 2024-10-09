import api from '@/services/api';

export default {
    namespaced: true,
    state: {
        messages: [],
        sessionKey: null,
    },
    mutations: {
        SET_MESSAGES(state, messages) {
            state.messages = messages;
        },
        ADD_MESSAGE(state, message) {
            state.messages.push(message);
        },
        SET_SESSION_KEY(state, sessionKey) {
            // mutations와 actions에서 사용하는 키 통일
            state.sessionKey = sessionKey;
        },
    },
    actions: {
        async initSession({ commit }) {
            try {
                const response = await api.post('chatbot/session/'); // URL 수정
                console.log('Session response:', response);
                if (response.data && response.data.session_key) {
                    commit('SET_SESSION_KEY', response.data.session_key);
                } else {
                    throw new Error('서버로부터 유효한 세션 키를 받지 못함');
                }
            } catch (error) {
                console.error('세션 초기화 오류:', error);
                if (error.response) {
                    console.error('Error response:', error.response.data);
                }
                throw error;
            }
        },
        async sendMessageToBackend({ commit, state }, { message }) {
            if (!state.sessionKey) {
                console.error('세션 키가 없습니다. 세션을 초기화해주세요.');
                return;
            }
            try {
                commit('ADD_MESSAGE', { isUser: true, user_message: message });
                const response = await api.post(`/chatbot/message/${state.sessionKey}/`, { message });
                if (response.data && response.data.response) {
                    commit('ADD_MESSAGE', { isUser: false, gpt_message: response.data.response });
                } else {
                    throw new Error('서버로부터 응답이 잘못됨');
                }
            } catch (error) {
                console.error('메시지 전송 오류:', error);
                commit('ADD_MESSAGE', {
                    isUser: false,
                    gpt_message: '에러가 발생하여 메시지 처리에 오류가 생겼습니다.',
                });
            }
        },
    },
};
