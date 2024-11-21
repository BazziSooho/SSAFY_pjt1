<script>
import { useAuthStore } from "@/stores/auth"; // Pinia 스토어 가져오기
import apiClient from "@/plugins/axios";
import Navbar from "@/components/Navbar/HomeNavbar.vue"

export default {
  name: "LoginView",
  components : {
    Navbar,
  },
  data() {
    return {
      username: "",
      password: "",
      errorMessage: null,
      isLoading: false,
    };
  },
  methods: {
    async login() {
      this.isLoading = true;
      const authStore = useAuthStore(); // Pinia 스토어 인스턴스

      try {
        // Django 서버로 로그인 요청
        const response = await apiClient.post("accounts/login/", {
          username: this.username,
          password: this.password,
        });

        if (response.data.key) {
          // 토큰을 localStorage에 저장 및 Pinia 상태 업데이트
          localStorage.setItem("token", response.data.key);
          authStore.login(response.data.key); // Pinia 상태 업데이트

          // 로그인 성공 후 리다이렉트
          this.$router.push("/");
        } else {
          this.errorMessage = "로그인에 실패했습니다.";
        }
      } catch (error) {
        console.error("로그인 실패:", error.response?.data || error.message);
        this.errorMessage = "로그인에 실패했습니다.";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<template>
  <div class="Navbar"><Navbar /></div>
  <div class="login-container">
    <h1>로그인</h1>
    <form @submit.prevent="login">
      <div class="input-group">
        ID : <br>
        <input
          type="text"
          v-model="username"
          placeholder="아이디 또는 이메일을 입력하세요"
          required
        />
      </div>
      <div class="input-group">
        Password : <br>
        <input
          type="password"
          v-model="password"
          placeholder="비밀번호를 입력하세요"
          required
        />
      </div>
      <button type="submit" class="login-btn">
        <span v-if="isLoading">로그인 중...</span>
        <span v-else>로그인</span>
      </button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center; /* 수평 가운데 정렬 */
  justify-content: flex-start; /* 수직 가운데 정렬 */
  height: 100vh; /* 화면 전체 높이를 사용하여 중앙 정렬 */
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
  width: 100%; /* 부모 컨테이너 너비에 맞춤 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start; 
}

input[type='text'],
input[type='password'] {
  width: 300px; /* 고정된 너비 설정 */
  padding: 10px;
  font-size: 14px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.login-btn {
  width: 100%; /* 버튼 너비를 입력 필드와 동일하게 설정 */
  padding: 10px;
  background-color: #006a44; /* 농협 초록 */
  color: white;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}
</style>