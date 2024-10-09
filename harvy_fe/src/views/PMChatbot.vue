<template>
    <div class="pm-chatbot">
        <div class="pm-intro">
            <h1 class="h1">PM Chatbot이란?</h1>
            <h3 class="h3">
                Portfolio Matching Chatbot으로 사용자가 챗봇과의 상호작용을 통해<br />
                사용자가 원하는 포트폴리오를 추천받을 수 있도록 하는 시스템입니다.<br />
            </h3>
        </div>
        <div class="chat-container">
            <div class="chat-messages" ref="chatMessages">
                <div
                    v-for="(message, index) in messages"
                    :key="index"
                    :class="['message', message.isUser ? 'user' : 'bot']"
                >
                    {{ message.isUser ? message.user_message : message.gpt_message }}
                </div>
            </div>
            <div class="chat-input">
                <input v-model="userInput" @keyup.enter="sendMessage" placeholder="메시지를 입력하세요..." />
                <button @click="sendMessage">전송</button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
    name: 'PMChatbot',
    data() {
        return {
            userInput: '',
        };
    },
    computed: {
        ...mapState('chatbot', ['messages', 'sessionId']),
    },
    methods: {
        ...mapActions('chatbot', ['sendMessageToBackend', 'initSession']),
        async sendMessage() {
            if (this.userInput.trim()) {
                await this.sendMessageToBackend({ message: this.userInput });
                this.userInput = '';
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            }
        },
        scrollToBottom() {
            const chatMessages = this.$refs.chatMessages;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        },
    },
    mounted() {
        this.initSession();
    },
};
</script>

<style scoped>
.pm-chatbot {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.pm-intro {
    margin-top: 70px;
    margin-bottom: 30px;
    text-align: center;
}

.h1 {
    font-size: 1.2em;
    margin-bottom: -10px;
    font-weight: 1000;
    color: #466bda;
}

.h3 {
    font-size: 1em;
    line-height: 1.5;
    color: #9a9a9a;
    font-weight: 500;
    margin-bottom: -10px;
}

.chat-container {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.chat-messages {
    height: 400px;
    overflow-y: auto;
    padding: 10px;
}

.message {
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 8px;
    max-width: 70%;
}

.user {
    background-color: #e6f2ff;
    align-self: flex-end;
    margin-left: auto;
}

.bot {
    background-color: #f1f0f0;
    align-self: flex-start;
}

.chat-input {
    display: flex;
    padding: 10px;
    background-color: #f9f9f9;
}

input {
    flex-grow: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    margin-left: 10px;
    padding: 8px 15px;
    background-color: #738ce0;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
</style>
