<template>
  <div class="Navbar"><Navbar /></div>
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
        <li>은행 이름 : <br><input v-model="newSavings.bank" placeholder="은행 이름" required /></li><br>
        <li>적금 이름 : <br><input v-model="newSavings.product" placeholder="적금 이름" required /></li><br>
        <li>만기 기간 : <br><input v-model="newSavings.mtrt" type="number" placeholder="만기 기간 (개월)" required /></li><br>
        <li>가입 불가 조건 : <br><input v-model="newSavings.join_deny" type="number" placeholder="가입 불가 조건" required /></li><br>
        <li>가입 가능 조건 : <br><input v-model="newSavings.join_member" placeholder="가입 가능 조건" required /></li><br>
        <li>최대 한도 : <br><input v-model="newSavings.max_limit" type="number" placeholder="최대 한도" required /></li><br>
      </ul><br>
      <button type="submit">적금 추가</button>
    </form>
  </section>
</template>

<script>
import Navbar from "@/components/Navbar/HomeNavbar.vue";
import apiClient from "@/plugins/axios";

export default {
  name: "SavingView",
  components: {
    Navbar,
  },
  data() {
    return {
      currentTab: "add",
      newSavings: {
        bank: "",
        product: "",
        mtrt: "",
        join_deny: "",
        join_member: "",
        max_limit: "",
      },
      availableProducts: [],
    };
  },
  mounted() {
    this.fetchAvailableProducts();
  },
  methods: {
    async fetchAvailableProducts() {
      try {
        const response = await apiClient.get("/savings/add/"); // Django API 호출
        this.availableProducts = response.data;
      } catch (error) {
        console.error("적금 상품 목록 불러오기 중 오류 발생:", error);
      }
    },
    fillSavingsDetails(event) {
      const selectedProductId = event.target.value;
      const selectedProduct = this.availableProducts.find(
        (product) => product.id === parseInt(selectedProductId)
      );

      if (selectedProduct) {
        this.newSavings.bank = "농협은행"; // 예시 값
        this.newSavings.product = selectedProduct.name;
        this.newSavings.mtrt = selectedProduct.maturity || ""; // 만기 기간 예시 값
        this.newSavings.join_deny = 0; // 기본값
        this.newSavings.join_member = "모든 회원"; // 기본값
        this.newSavings.max_limit = selectedProduct.amount || ""; // 최대 한도
      }
    },
    async addSavings() {
      try {
        const response = await apiClient.post('/savings/add/', {
          bank: this.newSavings.bank,
          product: this.newSavings.product,
          mtrt: this.newSavings.mtrt,
          join_deny: this.newSavings.join_deny,
          join_member: this.newSavings.join_member,
          max_limit: this.newSavings.max_limit,
        });

        alert('적금이 성공적으로 추가되었습니다!');
        this.newSavings = {
          bank: "",
          product: "",
          mtrt: "",
          join_deny: "",
          join_member: "",
          max_limit: "",
        };
      } catch (error) {
        console.error('적금 추가 중 오류 발생:', error.response?.data || error.message);
        alert('적금 추가에 실패했습니다.');
      }
    },
  },
};
</script>

<style scoped>
/* 적금 상품 선택 박스 스타일 */
#product-select {
  min-width: 250px;
  max-width: 400px;
  height: 45px;
  padding: 10px;
  background-color: #ffffff;
  border: 2px solid #007bff;
  border-radius: 5px;
  font-size: 16px;
  color: #333;
  cursor: pointer;
}

#product-select option {
  padding: 8px;
  background-color: #f9f9f9;
  color: #333;
}

#product-select:hover {
  border-color: #0056b3;
}

#product-select option:checked {
  background-color: #e6f7ff;
}
</style>