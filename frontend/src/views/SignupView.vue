<template>
    <Navbar />
    <div class="signup-container">
      <h2>회원가입</h2>
      <form @submit.prevent="submitForm" class="signup-form">
        <div class="input-group">
          ID : <input
            type="text"
            v-model="form.username"
            placeholder="아이디를 입력하세요"
            required
          />
        </div>
        <div class="input-group">
            Password : 
          <input
            type="password"
            v-model="form.password"
            placeholder="비밀번호를 입력하세요"
            required
          />
        </div>
        <div class="input-group">
            email : 
          <input
            type="email"
            v-model="form.email"
            placeholder="이메일을 입력하세요"
            required
          />
        </div>
        <button type="submit" class="signup-btn">회원가입</button>
        <p v-if="errorMessage">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  import Navbar from '@/components/Navbar/HomeNavbar.vue'

  export default {
    name: 'SignupView', // 컴포넌트 이름
    components: {
      Navbar, // Navbar 컴포넌트 등록
    },
    data() {
      return {
        form: {
          username: "",
          email: "",
          password: "",
        },
        errorMessage: "",
        successMessage: "",
      };
    },
    methods: {
      async submitForm() {
        if (!this.form.username || !this.form.password || !this.form.email) {
          this.errorMessage = "모든 정보를 입력해주세요.";
          return;
        }
  
        const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
        if (!emailPattern.test(this.form.email)) {
          this.errorMessage = "유효한 이메일을 입력해주세요.";
          return;
        }
  
        try {
          const response = await fetch("http://localhost:8000/api/signup/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.form),
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            this.errorMessage = errorData.message || "회원가입 실패.";
          } else {
            this.successMessage = "회원가입 성공!";
            this.errorMessage = "";
            this.form = { username: "", password: "", email: "" }; // 폼 초기화
          }
        } catch (error) {
          this.errorMessage = "서버와의 통신 중 오류가 발생했습니다.";
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
    width: calc(100% - 20px); /* 양쪽 패딩을 고려한 너비 */
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