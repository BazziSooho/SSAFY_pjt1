<template>
    <div class="my-savings">
      <h2>내 적금 상품</h2>
      <ul v-if="mySavings.length">
        <li v-for="saving in mySavings" :key="saving.id">
          <p>상품명: {{ saving.product }}</p>
          <p>은행명: {{ saving.bank }}</p>
          <p>저축 기간: {{ saving.save_trm }}개월</p>
          <p>금리: {{ saving.intr }}%</p>
        </li>
      </ul>
      <p v-else>등록된 적금 상품이 없습니다.</p>
    </div>
  </template>
  
  <script>
  import apiClient from "@/plugins/axios";
  
  export default {
    data() {
      return {
        mySavings: [], // 내 적금 상품 목록
      };
    },
    async created() {
      try {
        const response = await apiClient.get("/savings/my-savings/");
        this.mySavings = response.data; // 데이터 저장
      } catch (error) {
        console.error("내 적금 데이터를 가져오는 중 오류가 발생했습니다.", error);
      }
    },
  };
  </script>
  
  <style scoped>
  .my-savings {
    margin-bottom: 20px;
  }
  </style>