<template>
  <div class = "Navbar"><Navbar /> </div>
  <section v-if="currentTab === 'add'" class="add-savings-section">
    <h3>내 적금 추가</h3>

    <!-- 적금 상품 선택 -->
    <label for="product-select">적금 상품 선택:</label><br>
    <select id="product-select" @change="fillSavingsDetails($event)">
      <option value="" disabled selected>상품 선택...</option>
      <option v-for="product in availableProducts" :key="product.id" :value="product.id">
        {{ product.name }}
      </option>
    </select>

    <!-- 적금 정보 입력 -->
    <form @submit.prevent="addSavings">
      <ul>
        <li><input v-model="newSavings.name" placeholder="적금 이름" required /></li><br>
        <li><input v-model="newSavings.amount" type="number" placeholder="가입 금액" required /></li><br>
        <li><input v-model="newSavings.interestRate" type="number" placeholder="이율 (%)" required /></li><br>
        <li><input v-model="newSavings.maturity" type="number" placeholder="만기 기간(개월)" required /></li><br>
      </ul><br>
      <button type="submit">적금 추가</button>
    </form>
  </section>
</template>

<script>
import Navbar from "@/components/Navbar/HomeNavbar.vue"
import apiClient from "@/plugins/axios"

export default {
  name: 'SavingView',
  components: {
      Navbar, // Navbar 컴포넌트 등록
    },
  data() {
    return {
      currentTab: 'add',
      newSavings: {
        name: '',
        amount: '',
        interestRate: '',
        maturity: ''
      },
      availableProducts: []
    };
  },
  mounted() {
    this.fetchAvailableProducts();
  },
  methods: {
    async fetchAvailableProducts() {
      try {
        const response = await axios.get('/api/savings-products');
        this.availableProducts = response.data;
      } catch (error) {
        console.error('적금 상품 목록 불러오기 중 오류 발생:', error);
      }
    },
    fillSavingsDetails(event) {
      const selectedProductId = event.target.value;
      const selectedProduct = this.availableProducts.find(
        product => product.id === parseInt(selectedProductId)
      );

      if (selectedProduct) {
        this.newSavings.name = selectedProduct.name;
        this.newSavings.amount = selectedProduct.amount;
        this.newSavings.interestRate = selectedProduct.interest_rate;
        this.newSavings.maturity = selectedProduct.maturity;
      }
    },
  },
};
</script>

<style scoped>

/* 적금 상품 선택 박스 스타일 */
#product-select {
  min-width: 250px; /* 최소 너비 */
  max-width: 400px; /* 최대 너비 */
  height: 45px; /* 높이 */
  padding: 10px; /* 내부 여백 */
  background-color: #ffffff; /* 배경색 */
  border: 2px solid #007bff; /* 테두리 색상 */
  border-radius: 5px; /* 모서리 둥글게 */
  font-size: 16px; /* 글자 크기 */
  color: #333; /* 글자 색상 */
  cursor: pointer; /* 커서 모양 */
}

/* 옵션 스타일 */
#product-select option {
  padding: 8px; /* 옵션 내부 여백 */
  background-color: #f9f9f9; /* 옵션 배경색 */
  color: #333; /* 옵션 글자 색상 */
}

/* 호버 효과 (선택 박스 위에 마우스를 올렸을 때) */
#product-select:hover {
  border-color: #0056b3; /* 테두리 색상 변경 */
}

/* 선택된 옵션 강조 효과 (선택된 항목) */
#product-select option:checked {
  background-color: #e6f7ff; /* 선택된 옵션 배경색 */
}
</style>