<template>
    <div class="signup-page">
        <div class="signup-container">
            <h2>회원가입</h2>
            <form @submit.prevent="signup">
                <div class="form-row">
                    <div class="form-group half-width">
                        <label for="user_id">사용자 ID:</label>
                        <input type="text" id="user_id" v-model="formData.user_id" required />
                    </div>
                    <div class="form-group half-width">
                        <label for="user_name">이름:</label>
                        <input type="text" id="user_name" v-model="formData.user_name" required />
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group half-width">
                        <label for="password1">비밀번호:</label>
                        <input type="password" id="password1" v-model="formData.password1" required />
                    </div>
                    <div class="form-group half-width">
                        <label for="password2">비밀번호 확인:</label>
                        <input type="password" id="password2" v-model="formData.password2" required />
                    </div>
                </div>
                <div class="form-group">
                    <label for="user_email">이메일:</label>
                    <input type="email" id="user_email" v-model="formData.user_email" required />
                </div>
                <div class="form-group">
                    <label for="user_tel2">휴대폰 번호:</label>
                    <input type="tel" id="user_tel2" v-model="formData.user_tel2" required />
                </div>
                <div class="form-row">
                    <div class="form-group half-width">
                        <label for="user_corpname">소속회사:</label>
                        <input type="text" id="user_corpname" v-model="formData.user_corpname" required />
                    </div>
                    <div class="form-group half-width">
                        <label for="user_corpdept">소속부서:</label>
                        <input type="text" id="user_corpdept" v-model="formData.user_corpdept" required />
                    </div>
                </div>
                <div class="form-group">
                    <label for="user_corptype">회사유형:</label>
                    <input type="text" id="user_corptype" v-model="formData.user_corptype" required />
                </div>
                <button type="submit" class="submit-btn">가입하기</button>
            </form>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
    name: 'SignupPage',
    setup() {
        const store = useStore();
        const router = useRouter();
        const formData = ref({
            user_id: '',
            user_email: '',
            user_name: '',
            user_tel2: '',
            user_corpname: '',
            user_corpdept: '',
            user_corptype: '',
            password1: '',
            password2: '',
        });

        const signup = async () => {
            if (formData.value.password1 !== formData.value.password2) {
                alert('비밀번호가 일치하지 않습니다.');
                return;
            }
            try {
                await store.dispatch('signup', formData.value);
                router.push('/login');
            } catch (error) {
                console.error('Signup failed:', error);
                // 에러 처리 로직
            }
        };

        return {
            formData,
            signup,
        };
    },
};
</script>

<style scoped>
.signup-page {
    font-family: 'NanumSquare', sans-serif;
    max-width: 800px;
    margin: 50px auto;
    padding: 2rem;
    color: #333;
}

.signup-container {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    max-width: 600px;
    margin: 0 auto;
}

h2 {
    color: #2c3e50;
    font-size: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
}

.form-row {
    display: flex;
    gap: 1rem;
}

.form-group {
    margin-bottom: 1rem;
}

.half-width {
    flex: 1;
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

.address-input {
    display: flex;
    gap: 0.5rem;
}

.address-input input {
    flex: 1;
}

.address-search-btn {
    padding: 0.75rem;
    background-color: #95a5a6;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.3s ease;
}

.address-search-btn:hover {
    background-color: #7f8c8d;
}

.submit-btn {
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
    margin-top: 1rem;
}

.submit-btn:hover {
    background-color: #2980b9;
}

@media (max-width: 768px) {
    .signup-container {
        padding: 1rem;
    }

    .form-row {
        flex-direction: column;
        gap: 0;
    }

    input,
    .address-search-btn {
        padding: 0.5rem;
    }
}
</style>
