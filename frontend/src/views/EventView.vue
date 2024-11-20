<template>
    <div class="savings-page">
      <Navbar />  
      <header>
        <h2>적금 관리 및 비교</h2>
        <!-- 네비게이션 바 -->
        <nav>
          <ul class="nav-tabs">
            <li :class="{ active: currentTab === 'add' }" @click="currentTab = 'add'">적금 추가</li>
            <li :class="{ active: currentTab === 'compare' }" @click="currentTab = 'compare'">적금 비교</li>
          </ul>
        </nav>
      </header>
  
      <!-- 적금 추가 섹션 -->
      <section v-if="currentTab === 'add'" class="add-savings-section">
        <h3>내 적금 추가</h3>
        <form @submit.prevent="addSavings">
          <input v-model="newSavings.name" placeholder="적금 이름" required />
          <input v-model="newSavings.amount" type="number" placeholder="가입 금액" required />
          <input v-model="newSavings.interestRate" type="number" placeholder="이율 (%)" required />
          <input v-model="newSavings.maturity" type="number" placeholder="만기 기간(개월)" required />
          <button type="submit">적금 추가</button>
        </form>
  
        <!-- API 최신화 버튼 -->
        <button @click="updateSavingsList">API 최신화</button>
  
        <!-- 적금 목록 보기 -->
        <section v-if="savingsList.length" class="savings-list">
          <h3>내 적금 목록</h3>
          <ul>
            <li v-for="savings in savingsList" :key="savings.id">
              {{ savings.name }} - {{ savings.amount }}원, 이율: {{ savings.interestRate }}%, 만기: {{ savings.maturity }}개월
            </li>
          </ul>
        </section>
      </section>
  
      <!-- 적금 비교 섹션 -->
      <section v-if="currentTab === 'compare'" class="compare-savings-section">
        <h3>적금 비교</h3>
        <form @submit.prevent="compareSavings">
          <input v-model="savings.name" placeholder="적금 이름" required />
          <input v-model="savings.amount" type="number" placeholder="가입 금액" required />
          <input v-model="savings.interestRate" type="number" placeholder="이율 (%)" required />
          <input v-model="savings.maturity" type="number" placeholder="만기 기간(개월)" required />
          <button type="submit">비교하기</button>
        </form>
  
        <!-- 적금 리스트 비교 섹션 -->
        <section v-if="comparisonResult.length" class="comparison-results">
          <h3>비교 결과</h3>
          <table>
            <thead>
              <tr>
                <th>적금 이름</th>
                <th>이율 (%)</th>
                <th>가입 금액</th>
                <th>만기 기간</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="savings in comparisonResult" :key="savings.id">
                <td>{{ savings.name }}</td>
                <td>{{ savings.interestRate }}</td>
                <td>{{ savings.amount }}</td>
                <td>{{ savings.maturity }}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </section>
    </div>
  </template>
  
  <script>
  import Navbar from '@/components/Navbar/HomeNavbar.vue'

  export default {
    name: 'EventView', // 컴포넌트 이름
    components: {
      Navbar, // Navbar 컴포넌트 등록
    },
    data() {
      return {
        currentTab: 'add',  // 현재 선택된 탭 ('add' 또는 'compare')
        newSavings: {
          name: '',
          amount: '',
          interestRate: '',
          maturity: ''
        },
        savingsList: [],  // 사용자의 적금 목록
        savings: {
          name: '',
          amount: '',
          interestRate: '',
          maturity: ''
        },
        comparisonResult: []  // 적금 비교 결과
      };
    },
    methods: {
      async addSavings() {
        // 적금 추가 API 호출
        try {
          const response = await axios.post('/api/add-savings', this.newSavings);
          this.savingsList.push(response.data);  // 추가된 적금을 리스트에 반영
          this.clearNewSavings();
        } catch (error) {
          console.error('적금 추가 중 오류 발생:', error);
        }
      },
      clearNewSavings() {
        // 입력 폼 초기화
        this.newSavings = { name: '', amount: '', interestRate: '', maturity: '' };
      },
      async updateSavingsList() {
        // API 호출하여 최신 적금 목록 불러오기
        try {
          const response = await axios.get('/api/savings-list');
          this.savingsList = response.data;
        } catch (error) {
          console.error('적금 목록 최신화 중 오류 발생:', error);
        }
      },
      async compareSavings() {
        // 적금 비교 API 호출
        try {
          const response = await axios.post('/api/compare-savings', this.savings);
          this.comparisonResult = response.data;
        } catch (error) {
          console.error('적금 비교 중 오류 발생:', error);
        }
      }
    },
    mounted() {
      // 페이지가 로드될 때 적금 목록을 불러옴
      this.updateSavingsList();
    }
  };
  </script>
  
  <style scoped>
  .nav-tabs {
    display: flex;
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .nav-tabs li {
    padding: 10px 20px;
    cursor: pointer;
    border-bottom: 2px solid transparent;
  }
  .nav-tabs li.active {
    border-bottom: 2px solid #007bff;
  }
  form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  </style>