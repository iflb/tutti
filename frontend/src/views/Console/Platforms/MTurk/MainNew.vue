<template>
    <v-main class="grey lighten-4">
        <v-system-bar dark color="red lighten-2">
            <v-spacer></v-spacer>
            <span>MTurk Production Mode is active. Real payments can happen.</span>
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn icon v-bind="attrs" v-on="on"><v-icon>mdi-swap-horizontal</v-icon></v-btn>
                </template>
                <span>Change to sandbox mode</span>
            </v-tooltip>
            <v-spacer></v-spacer>
        </v-system-bar>
    </v-main>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
//import VueJsonPretty from 'vue-json-pretty'
//import 'vue-json-pretty/lib/styles.css'
//import Snackbar from '@/views/assets/Snackbar.vue'
export default {
    components: {
        //VueJsonPretty,
        //TuttiSnackbar: Snackbar
        //codemirror
    },
    data: () => ({
    }),
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
    },
    mounted() {
        this.onDuctOpen(() => {
        });
    }
}
</script>
