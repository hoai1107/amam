<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
</script>

<template>
  <div class="container">
    <div class="comment-container">
      <img class="avatar" />
      <div class="form-container">
        <input
          class="input-comment"
          v-model="comment"
          placeholder="Add an answer..."
        />
        <ButtonItem
          style="margin-top: 12px"
          type="primary"
          state="normal"
          text="Comment"
        ></ButtonItem>
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
  box-sizing: border-box;
  @extend .base-400;
}

.comment-container {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  position: relative;
  padding-bottom: 8px;
}

.avatar {
  height: 48px;
  width: 48px;

  border: 2px solid #000000;
  border-radius: 8px;
  background-color: var(--white);
}

.form-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: flex-end;
}

.input-comment {
  height: 48px;
  width: calc(100% - 12px);
  padding: 0px 24px;
  margin-left: 12px;
  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 8px;

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}
</style>
