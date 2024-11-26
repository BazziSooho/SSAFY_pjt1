<template>
    <div class="Navbar"><Navbar /></div>
    <div>
      <h1>게시글 목록</h1>
  
      <!-- 게시글 작성하기 버튼 -->
      <button @click="goToCreate">게시글 작성하기</button>
  
      <!-- 게시글 목록 -->
      <ul v-if="questions.length > 0">
        <li v-for="question in questions" :key="question.id">
          <a @click="goToDetail(question.id)">{{ question.title }}</a>
          <p>조회수: {{ question.views }}</p>
        </li>
      </ul>
  
      <!-- 게시글이 없을 때 -->
      <p v-else>게시글이 없습니다.</p>
    </div>
  </template>
  
  <script>
  import apiClient from "@/plugins/axios";
  import Navbar from "@/components/Navbar/HomeNavbar.vue"

  export default {
    components : {
        Navbar,
    },
    data() {
      return {
        questions: [],
      };
    },
    methods: {
      async fetchQuestions() {
        try {
          const response = await apiClient.get("/articles/ask/");
          this.questions = response.data;
        } catch (error) {
          console.error("게시글 목록 불러오기 실패:", error);
        }
      },
      goToDetail(id) {
        this.$router.push(`/articles/question/${id}`);
      },
      goToCreate() {
        this.$router.push("/articles/create-question");
      },
    },
    created() {
      this.fetchQuestions();
    },
  };
  </script>