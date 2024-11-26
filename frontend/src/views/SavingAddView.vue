<template>
  <div class="Navbar"><Navbar /></div>
  <div class="app-container">
    <!-- 좌측: 적금 상품 목록 -->
    <div class="product-list">
      <h2>적금 상품 목록</h2>
      <ul v-if="products.length">
        <!-- 단일 선택 라디오 버튼 -->
        <li v-for="product in products" :key="product.id">
          <input
            type="radio"
            :value="product"
            v-model="selectedProduct"
          />
          {{ product.fin_prdt_nm }}
          <button @click="fetchOptions(product.id)" :disabled="!selectedProduct || selectedProduct !== product">옵션 보기</button>
        </li>
        <!-- 직접 입력 옵션 -->
        <li>
          <input
            type="radio"
            :value="{ id: 'custom', name: '직접 입력' }"
            v-model="selectedProduct"
          />
          직접 입력
        </li>
      </ul>
      <p v-else>상품 데이터를 불러오는 중입니다...</p>
    </div>

    <!-- 우측: 선택된 상품의 옵션 -->
    <div class="product-options" v-if="selectedProduct">
      <h2>선택된 상품 옵션</h2>
      <!-- 옵션 목록 -->
      <ul v-if="options.length && selectedProduct.id !== 'custom'">
        <li v-for="option in options" :key="option.id">
          <input
            type="radio"
            :value="option"
            v-model="selectedOption"
          />
          기간: {{ option.save_trm }}개월<br>
          금리 유형 : {{ option.intr_rate_type_nm }}<br>
          적립 유형 : {{ option.rsrv_type_nm }}<br>
          금리:
          <input type="number" step="0.01" v-model.lazy.number="option.customIntr" />
        </li>
      </ul>

      <!-- 직접 입력 폼 -->
      <div v-else-if="selectedProduct.id === 'custom'">
        <h3>직접 입력</h3>
        <label>은행명:</label>
        <input type="text" v-model.lazy.trim="customInput.bank" /><br />
        <label>상품명:</label>
        <input type="text" v-model.lazy.trim="customInput.product" /><br />
        <label>만기후 이자율:</label>
        <input type="number" step="0.01" v-model.lazy.number="customInput.mtrt" /><br />
        <label>금리:</label>
        <input type="number" step="0.01" v-model.lazy.number="customInput.intr" /><br />
        <label>가입제한:</label>
        <input type="number" v-model.lazy.number="customInput.join_deny" /><br />
        <label>가입대상:</label>
        <input type="text" v-model.lazy.trim="customInput.join_member" /><br />
        <label>최대한도:</label>
        <input type="number" step="0.01" v-model.lazy.number="customInput.max_limit" /><br />
        <label>금리 유형:</label>
        <input type="text" v-model.lazy.trim="customInput.intr_rate_type" /><br />
        <label>적립 유형:</label>
        <input type="text" v-model.lazy.trim="customInput.rsrv_type" /><br />
      </div>
    </div>

    <!-- 하단 저장 버튼 -->
    <div class="selected-data">
      <h2>선택된 데이터</h2>
      <!-- 선택된 데이터 확인 -->
      <textarea v-model.lazy.trim="formattedSelectedData" readonly></textarea><br />
      <!-- 저장 버튼 -->
      <button @click.prevent.stop="saveSelectedData">저장하기</button>
    </div>
  </div>
</template>

<script>
// Vue 컴포넌트
import apiClient from "@/plugins/axios";
import Navbar from "@/components/Navbar/HomeNavbar.vue";

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      products: [], // 전체 적금 상품 목록
      options: [], // 선택된 상품의 옵션 목록
      selectedProduct: null, // 단일 선택된 적금 상품
      selectedOption: null, // 단일 선택된 옵션
      customInput: {
        bank: "",
        product: "",
        mtrt: null,
        intr: null,
        join_deny: null,
        join_member: "",
        max_limit: null,
        intr_rate_type: "",
        rsrv_type: "",
      }, // 직접 입력 데이터
    };
  },
  computed: {
    formattedSelectedData() {
      // 선택된 데이터를 JSON 형식으로 포맷팅
      return JSON.stringify(
        {
          product: this.selectedProduct,
          option:
            this.selectedOption && this.selectedProduct.id !== "custom"
              ? { ...this.selectedOption, customIntr: Number(this.selectedOption.customIntr) }
              : null,
          customInput:
            this.selectedProduct && this.selectedProduct.id === "custom"
              ? this.customInput
              : null,
        },
        null,
        2
      );
    },
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await apiClient.get("/savings/list/");
        this.products = response.data;
      } catch (error) {
        console.error("적금 상품 데이터를 가져오는 중 오류가 발생했습니다.", error);
      }
    },
    async fetchOptions(productId) {
      try {
        const response = await apiClient.get(`/savings/list/${productId}/options`);
        this.options = response.data.options.map((option) => ({
          ...option,
          customIntr: 0, // 초기화된 사용자 정의 금리
        }));
      } catch (error) {
        console.error("옵션 데이터를 가져오는 중 오류가 발생했습니다.", error);
      }
    },
    async saveSelectedData() {
      const payload = [];

      // 직접 입력 데이터 처리
      if (this.selectedProduct && this.selectedProduct.id === "custom") {
        payload.push({
          bank: this.customInput.bank,
          product: this.customInput.product,
          mtrt: Number(this.customInput.mtrt),
          intr: Number(this.customInput.intr),
          join_deny: Number(this.customInput.join_deny),
          join_member: this.customInput.join_member,
          max_limit: Number(this.customInput.max_limit),
          intr_rate_type: this.customInput.intr_rate_type,
          rsrv_type: this.customInput.rsrv_type,
          user_id: this.userId, // 유저 ID 전달 (로그인 상태에서 가져오기)
        });
      }

      // 기존 상품과 단일 선택된 옵션 데이터 처리
      if (this.selectedProduct && this.selectedProduct.id !== "custom" && this.selectedOption) {
        payload.push({
          bank: this.selectedProduct.kor_co_nm || "알 수 없음", // 은행명 기본값 처리
          product: this.selectedProduct.fin_prdt_nm,
          mtrt: this.selectedOption.save_trm,
          intr: Number(this.selectedOption.customIntr),
          join_deny:
            this.selectedProduct.join_deny || 0, // 기본값 처리
          join_member:
            this.selectedProduct.join_member || "개인",
          max_limit:
            this.selectedProduct.max_limit || 0,
          intr_rate_type:
            this.selectedOption.intr_rate_type || "단리", // 기본값 처리
          rsrv_type:
            this.selectedOption.rsrv_type || "일반", // 기본값 처리
        });
      }

      try {
        await apiClient.post("/savings/usersaving/", payload);
        alert("저장되었습니다.");
      } catch (error) {
        console.error("데이터 저장 중 오류가 발생했습니다.", error);
      }
    },
  },
  created() {
    this.fetchProducts(); // 컴포넌트 생성 시 전체 적금 상품 목록 불러오기
  },
};
</script>

<style scoped>
.app-container {
  display: flex;
  gap: 20px;
}

.product-list,
.product-options,
.selected-data {
  flex: 1;
}

textarea {
  width: 100%;
  height: 100px;
}
</style>