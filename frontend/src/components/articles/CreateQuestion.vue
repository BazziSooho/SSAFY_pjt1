<template>
    <div>
      <h1>게시글 작성하기</h1>
  
      <form @submit.prevent="submitQuestion">
        <div>
          <label for="title">제목</label><br>
          <input type="text" id="title" v-model="title" required />
        </div>
  
        <div>
          <label for="content">내용</label><br>
          <textarea id="content" v-model="content" required></textarea>
        </div>
  
        <button type="submit">작성하기</button>
      </form>
    </div>
  </template>
  
  <script>
  import apiClient from "@/plugins/axios";
  
  export default {
    data() {
      return {
        title: "",
        content: "",
      };
    },
    methods: {
      async submitQuestion() {
        try {
          const response = await apiClient.post("/articles/ask/", {
            title: this.title,
            context: this.content,
          });
          alert("게시글이 작성되었습니다!");
          this.$router.push(`/articles/question/${response.data.id}`); // 작성된 게시글로 이동
        } catch (error) {
          console.error("게시글 작성 실패:", error.response.data);
          alert("게시글 작성 중 오류가 발생했습니다.");
        }
      },
    },
  };
  </script>