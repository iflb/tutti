<template>
    <v-card elevation="0" tile color="grey lighten-5" class="pa-4" height="100%">
        <div class="overline mb-4">ANSWER DATA</div>
        <vue-json-pretty :data="response" style="line-height:1.4em;"></vue-json-pretty>
    </v-card>
</template>

<script>
import 'vue-json-pretty/lib/styles.css'
import VueJsonPretty from 'vue-json-pretty/lib/vue-json-pretty'

export default {
    components: {
        VueJsonPretty
    },
    data: () => ({
        currentAnswer: {},
    }),
    props: ["response"]
}
</script>
