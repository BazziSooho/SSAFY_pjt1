// src/plugins/axios.js
import axios from 'axios';

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/', // Django 백엔드 API 기본 URL
  headers: {
    'Content-Type': 'application/json', // 모든 요청에 JSON 형식 사용
  },
});

// 요청 인터셉터: 토큰 추가
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token'); // 로컬 스토리지에 저장된 JWT 토큰 가져오기
  if (token) {
    config.headers.Authorization = `Bearer ${token}`; // Authorization 헤더 추가
  }
  return config;
});

// 응답 인터셉터: 오류 처리
apiClient.interceptors.response.use(
  (response) => response, // 성공적인 응답 그대로 반환
  (error) => {
    console.error('API 오류:', error.response);
    return Promise.reject(error); // 오류를 호출한 컴포넌트로 전달
  }
);

export default apiClient;