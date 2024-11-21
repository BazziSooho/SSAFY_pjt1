import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null, // 초기 상태는 localStorage에서 가져옴
  }),
  getters: {
    isLoggedIn: (state) => !!state.token, // 로그인 여부 확인
  },
  actions: {
    login(token) {
      this.token = token;
      localStorage.setItem("token", token); // localStorage에 토큰 저장
    },
    logout() {
      this.token = null;
      localStorage.removeItem("token"); // localStorage에서 토큰 제거
    },
  },
});