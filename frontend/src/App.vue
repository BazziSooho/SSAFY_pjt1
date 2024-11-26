<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore(); // Pinia 스토어 가져오기

const logout = () => {
  alert("로그아웃 되었습니다."),
  authStore.logout(); // 로그아웃 처리
  window.location.reload();
};
</script>

<template>
  <header class="header">
    <div class="left-section">
      <RouterLink to="/">
        <img src="@/assets/images/nhmall_logo.png" alt="농협몰 로고" class="logo" />
      </RouterLink>
      <div class="buttons">
        <RouterLink to="/"><button class="btn">산지직송</button></RouterLink>
        <RouterLink to="/nhmall"><button class="btn">농협몰</button></RouterLink>
        <RouterLink to="/mart"><button class="btn">마트배송</button></RouterLink>
      </div>
    </div>

    <nav class="right-section">
      <img src="@/assets/images/nh_logo.png" style="width: 130px; height: auto;" />

      <!-- 로그인 상태에 따라 UI 변경 -->
      <template v-if="authStore.isLoggedIn">
        <RouterLink to="#">마이페이지</RouterLink>
        <a href="/" @click.prevent="logout">로그아웃</a>
      </template>
      <template v-else>
        <RouterLink to="/accounts/login">로그인</RouterLink>
        <RouterLink to="/accounts/signup">회원가입</RouterLink>
      </template>

      <RouterLink to="/articles/">문의게시판</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
/* 전체 헤더 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: white;
}

/* 왼쪽 섹션 (로고와 버튼) */
.left-section {
  display: flex;
  align-items: center;
}

.logo {
  width: 150px;
  margin-right: 1rem;
}

.buttons {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background-color: #f0f0f0;
  border: none;
  font-size: 0.9rem;
}

/* 오른쪽 섹션 (네비게이션과 아이콘) */
.right-section {
  display: flex;
  align-items: center;
}

.right-section a {
  margin-left: 1rem;
  text-decoration: none;
  color: #333;
}

.right-section a:hover {
  color: #007bff;
}
</style>