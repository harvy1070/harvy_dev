import axios from 'axios';

const api = axios.create({
    baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api/',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 요청 인터셉터
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('jwt_token'); // 토큰 저장 방식에 따라 수정
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 응답 인터셉터
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response && error.response.status === 401) {
            // 토큰 갱신 로직 또는 로그아웃 처리
            // 예: store.dispatch('auth/refreshToken') 또는 store.dispatch('auth/logout')
            console.log('Unauthorized, token might be expired');
            // 여기에 토큰 갱신 로직을 추가하거나 로그아웃 처리를 진행함
        }
        return Promise.reject(error);
    }
);

export default api;
