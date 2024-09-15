<template>
    <div class="login-container">
        <h2>로그인</h2>
        <form @submit.prevent="login">
            <div class="form-group">
                <label for="user_id">사용자 ID:</label>
                <input type="text" id="user_id" v-model="user_id" required />
            </div>
            <div class="form-group">
                <label for="password">비밀번호:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">로그인</button>
            <p>계정이 없으신가요? <router-link to="/signup">회원가입</router-link></p>
        </form>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
    name: 'LoginPage',
    setup() {
        const store = useStore();
        const router = useRouter();
        const user_id = ref('');
        const password = ref('');

        const login = async () => {
            try {
                const result = await store.dispatch('auth/login', {
                    user_id: user_id.value,
                    password: password.value,
                });
                if (result.success) {
                    router.push('/'); // 로그인 성공 시 홈페이지로 이동
                } else {
                    alert(result.message || '로그인에 실패했습니다.');
                }
            } catch (error) {
                console.error('Login failed:', error);
                alert('로그인 중 오류가 발생했습니다.');
            }
        };

        return {
            user_id,
            password,
            login,
        };
    },
};
</script>

<style scoped>
.login-page {
    /* font-family: 'NanumSquare', sans-serif; */
    max-width: 800px;
    margin: 50px auto;
    padding: 2rem;
    color: #333;
}

.login-container {
    margin-top: 100px !important;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    max-width: 400px;
    margin: 0 auto;
}

h2 {
    color: #2c3e50;
    font-size: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
}

.form-group {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    color: #2c3e50;
    font-weight: 600;
}

input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e6ed;
    border-radius: 4px;
    font-size: 1rem;
}

button {
    width: 100%;
    padding: 0.75rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #2980b9;
}

.signup-link {
    text-align: center;
    margin-top: 1rem;
    font-size: 0.9rem;
}

.signup-link a {
    color: #3498db;
    text-decoration: none;
    font-weight: 600;
}

.signup-link a:hover {
    text-decoration: underline;
}
</style>
