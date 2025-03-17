import axios from 'axios';
import store from '@/store';

// 환경에 따라 API 기본 URL 설정
const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || 'https://harvy-dev-f064f0b3b0ee.herokuapp.com/api/';
// const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || 'https://www.harvy.kr/api/';
// 임시 세팅
// const API_BASE_URL =
//     process.env.VUE_APP_API_BASE_URL || window.location.protocol + '//' + window.location.host + '/api/';
console.log('Current Environment:', process.env.NODE_ENV);
console.log('API_BASE_URL:', API_BASE_URL);

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
    },
});

// 요청 인터셉터
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        console.log('Request URL:', config.url);
        console.log('Full URL:', config.baseURL + config.url);
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
        if (error.response && error.response.status === 401 && error.config && !error.config.__isRetryRequest) {
            try {
                await store.dispatch('auth/refreshToken');
                error.config.__isRetryRequest = true;
                return api(error.config);
            } catch (refreshError) {
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

// API 함수들은 그대로 유지
api.login = async (credentials) => {
    const response = await api.post('auth/login/', credentials);
    if (response.data.access) {
        localStorage.setItem('token', response.data.access);
    }
    return response.data;
};

api.signup = async (formData) => {
    const response = await api.post('signup/', formData);
    return response.data;
};

api.checkAdmin = async () => {
    const response = await api.get('check-admin/');
    return response.data.isAdmin;
};

export default api;
