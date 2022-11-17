<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiArrowUpBoldOutline, mdiArrowDownBoldOutline } from "@mdi/js";

const props = defineProps({
  is_clicked: { type: Boolean, default: false },
});
</script>

<template>
  <div class="container">
    <div class="comment-container">
      <img class="avatar" />
      <div class="detail-container">
        <div class="comment-info">
          <p id="name">Name</p>
          <p id="timestamp">2 hours ago</p>
        </div>
        <p id="comment-detail">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam,
          purus sit amet luctus venenatis
        </p>
        <div class="interaction-container">
          <div class="vote" id="upvote">
            <p class="vote-count" id="upvote-count">10</p>
            <svg-icon type="mdi" :path="mdiArrowUpBoldOutline"></svg-icon>
          </div>
          <div class="vote" id="downvote">
            <p class="vote-count" id="downvote-count">5</p>
            <svg-icon type="mdi" :path="mdiArrowDownBoldOutline"></svg-icon>
          </div>
          <div
            id="reply"
            role="button"
            tabindex="0"
            v-on:click.native="is_clicked = !is_clicked"
          >
            Reply
          </div>
        </div>
        <Transition>
          <div class="form-container" v-if="is_clicked">
            <input
              class="input-comment"
              v-model="comment"
              placeholder="Add an answer..."
            />
            <ButtonItem
              style="height: 48px"
              type="primary"
              state="normal"
              text="Comment"
            ></ButtonItem>
          </div>
        </Transition>
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

.detail-container {
  flex-direction: column;
  width: calc(100% - 48px);
  margin-left: 12px;
}

.form-container {
  display: flex;
  align-items: flex-end;
  width: 100%;
}

.input-comment {
  height: 48px;
  width: 100%;
  padding: 0px 24px;
  margin-right: 12px;
  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 8px;

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}

.comment-info,
.interaction-container,
.vote {
  display: flex;
  flex-direction: row;
}

#name {
  @extend .base-600;
}

#timestamp {
  margin-left: 24px;
  color: var(--gray-400);
}

#comment-detail {
  padding: 8px 0px;
}

.interaction-container {
  padding-bottom: 12px;
}

.vote {
  padding-right: 20px;
}

.vote-count {
  padding-right: 5px;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

#reply {
  cursor: pointer;
}
</style>
