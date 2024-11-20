<template>
    <div class="home-view">
      <Navbar />  
    </div>
    <div class="login-container">
      <h1>서비스를 이용하기 위해서는 로그인이 필요합니다. 로그인 해 주세요.</h1>
      <h2>Login</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="input-group">
          <input 
            type="text" 
            v-model="username" 
            id="username" 
            placeholder="아이디 또는 이메일을 입력하세요" 
            required 
          />
        </div>
        <div class="input-group">
          <input 
            type="password" 
            v-model="password" 
            id="password" 
            placeholder="비밀번호를 입력하세요" 
            required 
          />
        </div>
        <button type="submit" class="login-btn">로그인</button>
        <p><RouterLink to='/signup/'>회원가입</RouterLink></p>
  
        <p v-if="errorMessage">{{ errorMessage }}</p>
  
      </form>
    </div>
  </template>
  
  <script>
  import { RouterLink, RouterView } from 'vue-router'
  import axios from 'axios';
  import Navbar from '@/components/Navbar/HomeNavbar.vue';
  
  export default {
    name: 'LoginView', // 컴포넌트 이름
    components: {
      Navbar, // Navbar 컴포넌트 등록
    },
    data() {
      return {
        username: '',
        password: '',
        rememberId: false,
        autoLogin: false,
        errorMessage: null,
      };
    },
    methods: {
      async login() {
        try {
          // 서버로 로그인 요청 전송
          const response = await axios.post('http://localhost:8000/api/login/', {
            username: this.username,
            password: this.password,
          });
          
          // 토큰 저장 (JWT 예시)
          localStorage.setItem('token', response.data.token);
  
          // 성공 시 페이지 이동
          this.$router.push('/main');
        } catch (error) {
          console.error(error);
          this.errorMessage = '로그인에 실패했습니다. 다시 시도해주세요.';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .login-form {
    width: 300px;
  }
  
  .input-group {
    margin-bottom: 15px;
  }
  
  input[type="text"], input[type="password"] {
    width: calc(100% - 20px); /* 양쪽 패딩을 고려한 너비 */
    padding: 10px;
    font-size: 14px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  .login-btn {
    width: 100%;
    padding: 10px;
    background-color: #006a44; /* Green color */
    color: white;
    font-size: 16px;
    border-radius: 4px;
    border: none;
  }
  
  </style>