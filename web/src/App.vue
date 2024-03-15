<template>
  <div id="app">
    <router-view/>
    <!--  用来兼容乾坤前端微服务  -->
    <div id="qiankun"></div>
<!--    <div id="reload">-->
<!--          <router-view v-if="isShow"></router-view>-->
<!--    </div>-->

  </div>
</template>

<script>
import util from '@/libs/util'
export default {
  name: 'app',
  provide () {
    return {
      reload: this.reload
    }
  },
  data () {
    return {
      isShow: true
    }
  },
  watch: {
    '$i18n.locale': 'i18nHandle'
  },
  created () {
    this.i18nHandle(this.$i18n.locale)
  },
  methods: {
    i18nHandle (val, oldVal) {
      util.cookies.set('lang', val)
      document.querySelector('html').setAttribute('lang', val)
    },
    reload () {
      this.isShow = false
      this.$nextTick(function () {
        this.isShow = true
      }
      )
    }
  }
}
</script>

<style lang="scss">
// 授权样式
.dvadmin-auth {
  font-size: 0.8em;
  position: fixed;
  top: 50vh;
  right: -163px;;
  text-align: center;
  color: #888888;
  background-image: linear-gradient(to left, #d3d3d3, #989898, #888888, #363636, #888888, #989898, #d3d3d3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  -webkit-background-size: 200% 100%;
  animation: bgp 6s infinite linear;
  transform: rotate(90deg);
}

@import "~@/assets/style/public-class.scss";
@import "~@/assets/style/yxt-public.scss";
</style>
