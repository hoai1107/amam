<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiCheckBold } from '@mdi/js';
const props = defineProps(
  {
    wrong: {type: Boolean, default: true},
  }
)
</script>

<template>
    <div class="container flex flex-col">
        <div class="input-container flex flex-col content-stretch">
            <p>Email</p>
            <input type="email" class="input-form" v-model="email" />
        </div>
        <div class="input-container flex flex-col content-stretch">
            <p>Password</p>
            <input type="password" class="input-form" v-model="password" />
        </div>
        <div class="checkbox-container flex flex-row items-center">
            <div class="tick-box flex flex-row items-center justify-center">
                <input type="checkbox" id="remembered" class="input-checkbox items-center" v-model="remembered">
                <span class="flex tick-icon">
                    <svg-icon type="mdi" :path="mdiCheckBold" size=10></svg-icon>
                </span>
            </div>
            <label for="remembered">Remember me</label>
        </div>
        <p class="warning" v-if="false">Wrong account or password</p>
        <p class="warning" v-if="false">Your email hasn't verified yet!</p>
        <p class="warning" style="color: var(--blue)" v-if="true">Please verify email before logging in</p>
        <ButtonItem
              style="margin-top: 10px"
              type="primary"
              state="normal"
              text="Login"
            ></ButtonItem>
    </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
    @extend .base-400;
}

.input-container {
    margin-bottom: 12px;
}

.input-form {
    padding: 12px 24px;
    gap: 8px;
    background: #FFFFFF;
    border: 2px solid #000000;
    border-radius: 8px;

    -moz-appearance:none; /* Firefox */
    -webkit-appearance:none; /* Safari and Chrome */
    appearance:none;
}

.checkbox-container {
    margin-bottom: 12px;
}

.input-checkbox {
    cursor: pointer;
    opacity: 0;
    z-index: 1;
}
.tick-icon {
    position: absolute;
    opacity: 0;
}

.tick-box input[type="checkbox"]:checked ~ .tick-icon {
    opacity: 1;
}

.tick-box {
    width: 14px;
    height: 14px;
    
    background: #FFFFFF;
    border: 2px solid #000000;
    border-radius: 2px;
    margin-right: 8px;
}

.button-container {
    padding-top: 12px;
}

.warning {
    font-size: 14px;
    color: var(--red);
}
</style>
