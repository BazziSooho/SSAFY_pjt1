<template>
  <div class="recommendation">
    <h2>추천 적금 상품</h2>
    <ul v-if="recommendations.length">
      <li v-for="(item, index) in recommendations" :key="index">
        <h3>{{ item.type === 'high_score' ? '가중치 추천' : item.type === 'random' ? '랜덤 추천' : '최대 이익 추천' }}</h3>
        <p v-if="item.data">상품명: {{ item.data.fin_prdt_nm }}</p>
        <p v-if="item.data">은행명: {{ item.data.kor_co_nm }}</p>
        <p v-if="item.data">최대 한도: {{ item.data.max_limit }}</p>
      </li>
    </ul>
    <p v-else>추천 결과가 없습니다.</p>
  </div>
</template>

<script>
export default {
  props: {
    recommendations: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.recommendation {
  margin-bottom: 20px;
}
</style>