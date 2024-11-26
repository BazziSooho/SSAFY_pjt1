<template>
  <div>
    <div class="Navbar"><Navbar /></div>
    <h1>메인 페이지</h1>

    <!-- 내 적금 상품 조회 컴포넌트 -->
    <MySavings />

    <!-- 추천 컴포넌트 -->
    <Recommendation />
  </div>
</template>

<script>
import Recommendation from "@/components/Recommends/Recommendation.vue";
import MySavings from "@/components/Recommends/MySavings.vue";
import Navbar from "@/components/Navbar/HomeNavbar.vue";

export default {
  components: {
    Navbar,
    Recommendation,
    MySavings,
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}
</style>