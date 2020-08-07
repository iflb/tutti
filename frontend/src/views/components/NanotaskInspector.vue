<template>
    <v-main>
        <v-container mt-0 pa-0>
        <v-toolbar prominent flat height="150px" fill-height>
            <v-toolbar-title>
            <v-row>
                <v-col>
                    <v-select :items="childProps[name].projects" v-model="projectName" label="Project name"></v-select>
                </v-col>
                <v-col>
                    <v-select :items="childProps[name].templates" v-model="templateName" label="Template name" :disabled="isTemplateSelectDisabled"></v-select>
                </v-col>
                <v-col align="right">
                    <v-btn class="text-none" :disabled="projectName === null" @click="launchProductionMode()">Launch in production mode (private)</v-btn>
                </v-col>
            </v-row>
            </v-toolbar-title>
        </v-toolbar>
        <v-row>
            <v-col cols="9">
                <v-card height="100%"><component :is="nanotaskTemplateComponent"/></v-card>
            </v-col>
            <v-col cols="3">
                <v-card height="100%" color="blue-grey lighten-4">
                    <v-list-item three-line>
                        <v-list-item-content>
                            <div class="overline mb-4">ANSWER DATA</div>
                            <v-textarea :disabled="true" v-model="currentAnswer" height="100%"></v-textarea>
                        </v-list-item-content>
                    </v-list-item>
                </v-card>
            </v-col>
        </v-row>
        </v-container>
    </v-main>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    data: () => ({
        projectName: null,
        templateName: null,
    }),
    props: ["childProps","name"],
    computed: {
        ...mapGetters("ductsModule", ["duct"]),
        nanotaskTemplateComponent: {
            cache: true,
            get: function() {
                if(this.projectName && this.templateName){
                    return require(`@/projects/${this.projectName}/templates/${this.templateName}/Main.vue`).default;
                } else { return null }
            }
        },
        currentAnswer() { return JSON.stringify(this.$store.getters.currentAnswer, undefined, 4) },

        isTemplateSelectDisabled() {
            return !(this.name in this.childProps) || this.childProps[this.name].templates.length==0
        }
    },
    methods: {
        launchProductionMode(){ window.open(`/vue/prod/private/${this.projectName}`); }
    },
    watch: {
        projectName() {
            this.templateName = null
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.LIST_TEMPLATES, data: this.projectName })
        }
    }
}
</script>
