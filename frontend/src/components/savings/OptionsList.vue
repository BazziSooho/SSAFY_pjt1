<template>
    <div>
      <h2>선택된 상품 옵션</h2>
      <ul v-if="options.length">
        <li v-for="option in options" :key="option.id">
          금리: {{ option.intr_rate }}% ~ {{ option.intr_rate2 }}%, 기간: {{ option.save_trm }}개월
        </li>
      </ul>
      <p v-else>옵션 데이터가 없습니다.</p>
    </div>
  </template>
  
  <script>
  import apiClient from "@/plugins/axios";
  
  export default {
    props: {
      id: {
        type: [Number, String],
        required: true,
      },
    },
    data() {
      return {
        options: [], // 옵션 데이터
      };
    },
    async created() {
      try {
        const response = await apiClient.get(`/savings/list/${this.id}/options`);
        this.options = response.data.options; // API 응답에서 options 배열 추출
      } catch (error) {
        console.error("옵션 데이터를 가져오는 중 오류가 발생했습니다.", error);
      }
    },
  };
  </script>
  
  <style scoped>
  /* 필요에 따라 스타일 추가 */
  </style>