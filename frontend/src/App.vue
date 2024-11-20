<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="header">
    <!-- 왼쪽 로고와 버튼 -->
    <div class="left-section">
      <RouterLink to="/">
        <img src="@/assets/images/nhmall_logo.png" alt="농협몰 로고" class="logo">
      </RouterLink>
      <div class="buttons">
        <RouterLink to="/"><button class="btn">산지직송</button></RouterLink>
        <RouterLink to="/nhmall"><button class="btn">농협몰</button></RouterLink>
        <RouterLink to="/mart"><button class="btn">마트배송</button></RouterLink>
      </div>
    </div>

    <!-- 오른쪽 네비게이션 및 아이콘 -->
    <nav class="right-section">
      <img src="@/assets/images/nh_logo.png" style="width: 130px; height: auto;">
      <RouterLink to="/login">로그인</RouterLink>
      <RouterLink to="/signup">회원가입</RouterLink>
      <RouterLink to="/support">문의게시판</RouterLink>

    </nav>
  </header>

  <RouterView />
  
</template>



<style scoped>
/* 전체 헤더 */
.header {
  display: flex;
  justify-content: space-between; /* 좌우 섹션을 양 끝에 배치 */
  align-items: center; /* 세로 중앙 정렬 */
  padding: 1rem 2rem;
  background-color: white; /* 배경색 설정 */
}

/* 왼쪽 섹션 (로고와 버튼) */
.left-section {
  display: flex;
  align-items: center;
}

.logo {
  width: 150px; /* 로고 크기 조정 */
  margin-right: 1rem; /* 로고와 버튼 사이 간격 */
}

.buttons {
  display: flex;
  gap: 0.5rem; /* 버튼 간의 간격 설정 */
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
  margin-left: 1rem; /* 링크 간의 간격 */
  text-decoration: none;
  color: #333; /* 텍스트 색상 */
}

.right-section a:hover {
  color: #007bff; /* 호버 시 색상 변경 */
}

/* 아이콘 섹션 */
.icons {
  display: flex;
  align-items: center;
}

.icons i {
  font-size: 1.2rem; /* 아이콘 크기 조정 */
}

.icons a {
  margin-left: 1rem; /* 아이콘 링크 간의 간격 */
}
</style>
