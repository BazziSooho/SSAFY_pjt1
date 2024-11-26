<template>
  <form @submit.prevent="submitAnswer">
    <textarea v-model="content" placeholder="댓글을 입력하세요"></textarea>
    <button type="submit">댓글 작성</button>
  </form>
</template>

<script>
import apiClient from "@/plugins/axios";

export default {
  props: ["questionId"], // 부모 컴포넌트에서 questionId 전달받음
  data() {
    return {
      content: "",
    };
  },
  methods: {
    async submitAnswer() {
      try {
        const response = await apiClient.post(`/articles/answer/${this.questionId}/create/`, {
          content: this.content,
        });
        this.$emit("answerCreated"); // 부모 컴포넌트에 이벤트 전달 (댓글 새로고침)
        this.content = ""; // 입력 필드 초기화
      } catch (error) {
        console.error("댓글 작성 실패:", error.response ? error.response.data : error.message);
      }
    },
  },
};
</script>