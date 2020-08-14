<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row justify="center">
            <v-col cols="10">
            <v-card class="pa-3">
                <v-row class="justify-space-around">
                <v-col cols="12" md="7" align="center">
                <v-select width="80%" hide-details :items="project.templates" v-model="templateName" label="Template name" :disabled="isTemplateSelectDisabled"></v-select>
                </v-col>
                <v-col cols="12" md="4" align="center">
                <v-container>
                <v-btn class="text-none" :disabled="project.name === null" @click="launchProductionMode()">Launch in production mode (private)</v-btn>
                </v-container>
                </v-col>
                </v-row>
            </v-card>
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col cols="10" md="7">
                <v-card height="100%"><component :is="nanotaskTemplateComponent"/></v-card>
            </v-col>
            <v-col cols="10" md="3">
                <v-card height="100%" color="grey lighten-3">
                    <v-list-item three-line>
                        <v-list-item-content>
                            <div class="overline mb-4">ANSWER DATA</div>
                            <v-textarea auto-grow no-resize :disabled="true" v-model="currentAnswer"></v-textarea>
                        </v-list-item-content>
                    </v-list-item>
                </v-card>
            </v-col>
        </v-row>
    </v-main>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        templateName: null,
    }),
    props: ["sharedProps","name"],
    computed: {
        ...mapGetters("ductsModule", ["duct"]),
        project() { return this.sharedProps.project },

        nanotaskTemplateComponent: {
            cache: true,
            get: function() {
                if(this.project.name && this.templateName){
                    return require(`@/projects/${this.project.name}/templates/${this.templateName}/Main.vue`).default;
                } else { return null }
            }
        },
        currentAnswer() { return JSON.stringify(this.$store.getters.currentAnswer, undefined, 4) },

        isTemplateSelectDisabled() {
            return this.project.templates.length==0 || !this.project.name
        }
    },
    methods: {
        launchProductionMode(){ window.open(`/vue/private-prod/${this.project.name}`); }
    },
    watch: {
        "project.name"() { this.templateName = null }
    }
}
</script>
