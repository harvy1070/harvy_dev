<template>
    <div class="signup-page">
        <div class="signup-container">
            <h2>회원가입</h2>
            <form @submit.prevent="signup">
                <div class="form-row">
                    <div class="form-group half-width">
                        <div class="input-container">
                            <input type="text" id="user_id" v-model="formData.user_id" required placeholder=" " />
                            <label for="user_id">사용자 ID</label>
                        </div>
                    </div>
                    <div class="form-group half-width">
                        <div class="input-container">
                            <input type="text" id="user_name" v-model="formData.user_name" required placeholder=" " />
                            <label for="user_name">이름</label>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group half-width">
                        <div class="input-container">
                            <input
                                type="password"
                                id="password1"
                                v-model="formData.password1"
                                required
                                placeholder=" "
                            />
                            <label for="password1">비밀번호</label>
                        </div>
                    </div>
                    <div class="form-group half-width">
                        <div class="input-container">
                            <input
                                type="password"
                                id="password2"
                                v-model="formData.password2"
                                required
                                placeholder=" "
                            />
                            <label for="password2">비밀번호 확인</label>
                        </div>
                    </div>
                </div>
                <div class="form-group form-group-full">
                    <div class="input-container">
                        <input type="email" id="user_email" v-model="formData.user_email" required placeholder=" " />
                        <label for="user_email">이메일</label>
                    </div>
                </div>
                <div class="form-group form-group-full">
                    <div class="input-container">
                        <input type="tel" id="user_tel2" v-model="formData.user_tel2" required placeholder=" " />
                        <label for="user_tel2">휴대폰 번호</label>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group half-width">
                        <div class="input-container">
                            <input
                                type="text"
                                id="user_corpname"
                                v-model="formData.user_corpname"
                                required
                                placeholder=" "
                            />
                            <label for="user_corpname">소속회사</label>
                        </div>
                    </div>
                    <div class="form-group half-width">
                        <div class="input-container">
                            <input
                                type="text"
                                id="user_corpdept"
                                v-model="formData.user_corpdept"
                                required
                                placeholder=" "
                            />
                            <label for="user_corpdept">소속부서</label>
                        </div>
                    </div>
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
        console.log('Store:', store);
        const router = useRouter();
        const formData = ref({
            user_id: '',
            user_email: '',
            user_name: '',
            user_tel2: '',
            user_corpname: '',
            user_corpdept: '',
            password1: '',
            password2: '',
        });

        const signup = async () => {
            if (formData.value.password1 !== formData.value.password2) {
                alert('비밀번호가 일치하지 않습니다.');
                return;
            }
            try {
                const { success, message, data } = await store.dispatch('auth/signup', formData.value);
                console.log('Signup response:', { success, message, data }); // 응답 로깅
                if (success) {
                    alert('회원가입이 완료되었습니다.');
                    router.push('/login');
                } else {
                    alert(message);
                }
            } catch (error) {
                console.error('Signup failed:', error);
                if (error.message.includes('dispatch')) {
                    console.error('Store dispatch error. Store state:', store);
                }
                alert('회원가입 중 예기치 않은 오류가 발생했습니다. 나중에 다시 시도해주세요.');
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
    margin-top: 70px !important;
    font-family: 'NanumSquare', sans-serif;
    max-width: 800px;
    margin: 30px auto;
    padding: 1rem;
    color: #333;
}

.signup-container {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    box-sizing: border-box;
}

h2 {
    color: #2c3e50;
    font-size: 1.8rem;
    margin-bottom: 1.2rem;
    text-align: center;
}

.form-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1rem;
}

.form-group {
    flex: 1 1 calc(50% - 0.5rem);
    min-width: 0;
    margin-bottom: 1rem;
}

.form-group-full {
    flex: 1 1 100%;
    margin-bottom: 1rem;
}

.input-container {
    position: relative;
    width: 100%;
    height: 100%;
}

.half-width {
    flex: 1;
}

input {
    width: 100%;
    padding: 1rem 0.8rem 0.8rem;
    border: 1px solid #e0e6ed;
    border-radius: 4px;
    font-size: 0.9rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    box-sizing: border-box;
    height: 3.2rem;
}

input:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}

label {
    position: absolute;
    left: 0.8rem;
    top: 1rem;
    color: #7f8c8d;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    pointer-events: none;
    background-color: transparent;
}

input:focus + label,
input:not(:placeholder-shown) + label {
    top: 0.2rem;
    font-size: 0.7rem;
    color: #3498db;
    background-color: white;
    padding: 0 0.2rem;
}

.submit-btn {
    width: 100%;
    padding: 0.7rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: background-color 0.3s ease;
    margin-top: 0.8rem;
}

.submit-btn:hover {
    background-color: #2980b9;
}

@media (max-width: 600px) {
    .form-row {
        flex-direction: column;
        gap: 0.5rem;
    }

    .form-group {
        flex: 1 1 100%;
    }

    input {
        padding: 0.7rem 0.5rem 0.5rem;
    }
}
</style>
