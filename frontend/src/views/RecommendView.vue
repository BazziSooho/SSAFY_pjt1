<template>
  <div>
    <div class="Navbar"><Navbar /></div>
    <h1>메인 페이지</h1>

    <div class="app-container">
      <!-- 좌측: 내 적금 상품 조회 컴포넌트 -->
      <div class="left-panel">
        <MySavings @select-saving="handleSelectSaving" />
      </div>

      <!-- 중간: 추천하기 버튼 -->
      <div class="center-panel">
        <button @click="fetchRecommendations" :disabled="!selectedSaving">
          추천하기
        </button>
      </div>

      <!-- 우측: 추천 컴포넌트 -->
      <div class="right-panel">
        <Recommendation :recommendations="recommendations" />
      </div>
    </div>
  </div>
</template>

<script>
import Recommendation from "@/components/Recommends/Recommendation.vue";
import MySavings from "@/components/Recommends/MySavings.vue";
import Navbar from "@/components/Navbar/HomeNavbar.vue";
import apiClient from "@/plugins/axios";

export default {
  components: {
    Navbar,
    Recommendation,
    MySavings,
  },
  data() {
    return {
      selectedSaving: null, // 선택된 적금 상품
      recommendations: [], // 추천 결과
    };
  },
  methods: {
    handleSelectSaving(saving) {
      this.selectedSaving = saving; // 선택된 적금 상품 저장
    },
    async fetchRecommendations() {
      if (!this.selectedSaving) return;

      try {
        const response = await apiClient.post("/savings/recommendation/", {
          saving_id: this.selectedSaving.id, // 선택된 적금 상품 ID 전송
        });
        this.recommendations = response.data; // 추천 결과 저장
      } catch (error) {
        console.error("추천 데이터를 가져오는 중 오류가 발생했습니다.", error);
      }
    },
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  gap: 20px;
}

.left-panel,
.center-panel,
.right-panel {
  flex: 1;
}

.center-panel {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>