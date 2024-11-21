<template>
  <div class="Navbar"><Navbar /></div>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="register">
      <div class="input-group">
        ID : <br>
        <input
          type="text"
          v-model="username"
          placeholder="아이디를 입력하세요"
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
      <div class="input-group">
        Confirm : <br>
        <input
          type="password"
          v-model="passwordConfirm"
          placeholder="비밀번호를 다시 입력하세요"
          required
        />
      </div>
      <div class="input-group">
        Email : <br>
        <input
          type="email"
          v-model="email"
          placeholder="이메일을 입력해주세요"
          required
        />
      </div>
      <button type="submit" class="signup-btn">
        <span v-if="isLoading">회원가입 진행 중...</span>
        <span v-else>회원가입</span>
      </button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import apiClient from "@/plugins/axios"; // Axios 설정 파일 불러오기
import Navbar from '@/components/Navbar/HomeNavbar.vue'


export default {
  name: 'SignupView',
  components: {
      Navbar, // Navbar 컴포넌트 등록
    },
  data() {
    return {
      username: "",
      password: "",
      passwordConfirm: "",
      email: "",
      isLoading: false,
      errorMessage: null,
    };
  },
  methods: {
    async register() {
      // 비밀번호 확인
      if (this.password !== this.passwordConfirm) {
        this.errorMessage = "비밀번호가 일치하지 않습니다.";
        return;
      }

      this.isLoading = true; // 로딩 상태 시작
      try {
        // 회원가입 요청
        const response = await apiClient.post("accounts/signup/", {
          username: this.username,
          email: this.email,
          password1: this.password,
          password2: this.passwordConfirm,
        });

        // 회원가입 성공 메시지 처리
        console.log(response.data.message);
        alert("회원가입이 완료되었습니다!");
        this.$router.push("/"); // 회원가입 후 메인 페이지로 이동
      } catch (error) {
        console.error("회원가입 실패:", error.response?.data);
        this.errorMessage =
          error.response?.data?.detail || "회원가입에 실패했습니다. 다시 시도해주세요.";
      } finally {
        this.isLoading = false; // 로딩 상태 종료
      }
    },
  },
};
</script>

  <style scoped>
  .signup-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    height: 100vh; /* 화면 전체를 차지하도록 설정 */
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .signup-form {
    width: 300px; /* 로그인 페이지와 동일한 너비 */
  }
  
  .input-group {
    margin-bottom: 15px;
  }
  
  input[type="text"],
  input[type="email"],
  input[type="password"] {
    width: 300px; /* 양쪽 패딩을 고려한 너비 */
    padding: 10px;
    font-size: 14px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  .signup-btn {
    width: 100%;
    padding: 10px;
    background-color: #006a44; /* 동일한 초록색 */
    color: white;
    font-size: 16px;
    border-radius: 4px;
    border: none;
    cursor: pointer;
  }
  
  .signup-btn:hover {
    background-color: #005a3c; /* Hover 시 약간 어두운 색상 */
  }
  
  .success-message {
    color: green;
    margin-top: 1rem;
  }
  
  .error-message {
    color: red;
    margin-top: 1rem;
  }
  </style>