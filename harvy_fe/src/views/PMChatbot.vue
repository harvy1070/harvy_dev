<template>
    <div class="pm-chatbot">
        <h1>PM Chatbot</h1>
        <div class="chat-container">
            <div class="chat-messages" ref="chatMessages">
                <div
                    v-for="(message, index) in messages"
                    :key="index"
                    :class="['message', message.isUser ? 'user' : 'bot']"
                >
                    {{ message.text }}
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
        ...mapState('chatbot', ['messages']),
    },
    methods: {
        ...mapActions('chatbot', ['sendMessageToBackend', 'initSession']),
        async sendMessage() {
            if (this.userInput.trim()) {
                await this.sendMessageToBackend(this.userInput);
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
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
</style>
