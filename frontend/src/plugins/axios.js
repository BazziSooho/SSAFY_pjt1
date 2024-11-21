import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000/", // Django API 기본 URL
  headers: {
    "Content-Type": "application/json",
  },
});

// 요청 인터셉터: Authorization 헤더 추가
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // localStorage에서 토큰 가져오기
  if (token) {
    config.headers.Authorization = `Token ${token}`; // Authorization 헤더 추가
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
