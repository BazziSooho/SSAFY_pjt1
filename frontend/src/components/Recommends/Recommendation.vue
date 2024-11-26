<template>
    <div class="recommendation">
      <h2>추천 적금 상품</h2>
      <ul v-if="recommendations.length">
        <li v-for="product in recommendations" :key="product.id">
          <p>상품명: {{ product.fin_prdt_nm }}</p>
          <p>은행명: {{ product.kor_co_nm }}</p>
          <p>최대 한도: {{ product.max_limit }}</p>
          <p>금리 유형: {{ product.intr_rate_type }}</p>
          <p>적립 유형: {{ product.rsrv_type }}</p>
        </li>
      </ul>
      <p v-else>추천 상품이 없습니다.</p>
    </div>
  </template>
  
  <script>
  import apiClient from "@/plugins/axios";
  
  export default {
    data() {
      return {
        recommendations: [], // 추천 상품 목록
      };
    },
    async created() {
      try {
        const response = await apiClient.get("/savings/recommendation/");
        this.recommendations = response.data;
      } catch (error) {
        console.error("추천 데이터를 가져오는 중 오류가 발생했습니다.", error);
      }
    },
  };
  </script>
  
  <style scoped>
  .recommendation {
    margin-bottom: 20px;
  }
  </style>