<template>
  <div>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="상품명을 검색하세요"
    />
    <ul>
      <li
        v-for="product in filteredProducts"
        :key="product.id"
        @click="selectProduct(product.id)"
      >
        {{ product.fin_prdt_nm }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    products: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      searchQuery: "", // 검색어
    };
  },
  computed: {
    // 검색어에 따라 필터링된 상품 목록 반환
    filteredProducts() {
      return this.products.filter((product) =>
        product.fin_prdt_nm.includes(this.searchQuery)
      );
    },
  },
  methods: {
    selectProduct(productId) {
      // 상품 선택 시 옵션 페이지로 이동
      this.$router.push(`/savings/list/${productId}/options`);
    },
  },
};
</script>

<style scoped>
/* 필요에 따라 스타일 추가 */
</style>