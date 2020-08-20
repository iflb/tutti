<template>
    <div id="app">
        <vuep :template="code"></vuep>
    </div>
</template>

<script>
import Vue from 'vue'
import Vuep from 'vuep'
import 'vuep/dist/vuep.css'

Vue.use(Vuep /*, { codemirror options } */)
// or Vue.component('Vuep', Vuep)

export default {
  el: '#app',

  created: function () {
    this.code = ""
  }
}
</script>
