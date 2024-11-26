<template>
  <div>
    <!-- 데이터가 로드되었는지 확인 -->
    <div v-if="question">
      <h1>제목 : {{ question.title }}</h1>
      <p>내용 : <br>{{ question.context }}</p>
      <p>작성자: {{ question.user }}</p>
      <p>조회수: {{ question.views }}</p>

      <!-- 댓글 목록 -->
      <h2>댓글</h2>
      <ul v-if="question.answer_set.length > 0">
        <li v-for="answer in question.answer_set" :key="answer.id">
          {{ answer.content }} - {{ answer.author }}
        </li>
      </ul>
      <p v-else>댓글이 없습니다.</p>

      <!-- 댓글 작성 폼 -->
      <AnswerForm :questionId="question.id" @answerCreated="fetchQuestion" />
    </div>

    <!-- 데이터 로드 중 표시 -->
    <div v-else>
      <p>게시글을 불러오는 중입니다...</p>
    </div>
  </div>
</template>

<script>
import apiClient from "@/plugins/axios";
import AnswerForm from "@/components/articles/AnswerForm.vue";

export default {
  components: { AnswerForm },
  data() {
    return {
      question: null, // 초기 상태를 null로 설정
    };
  },
  methods: {
    async fetchQuestion() {
      try {
        const response = await apiClient.get(`/articles/answer/${this.$route.params.id}/`);
        this.question = response.data; // API 응답 데이터를 저장
      } catch (error) {
        console.error("게시글 불러오기 실패:", error);
        alert("게시글을 불러오는 중 오류가 발생했습니다.");
      }
    },
  },
  created() {
    this.fetchQuestion(); // 컴포넌트 생성 시 API 호출
  },
};
</script>