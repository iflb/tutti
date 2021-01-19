<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row justify="center">
            <v-col cols="10">
            <v-card class="pa-3">
                <v-row justify="center">
                    <v-col cols="12" lg="8">
                        <v-row class="justify-start ml-5 mr-0 pr-0" align="center">
                            <v-col cols="10">
                                <v-select width="300" hide-details :items="templateNames" v-model="templateName" label="Template name" :disabled="isTemplateSelectDisabled"></v-select>
                            </v-col>
                            <v-col cols="2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn fab small icon v-on="on" v-bind="attrs" :disabled="!project || project.name==''" @click.stop="$refs.dlgCreateTemplate.shown=true"><v-icon dark>mdi-plus-box-multiple-outline</v-icon></v-btn>
                                    </template>
                                    <span>Create New Template...</span>
                                </v-tooltip>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
            </v-card>
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col cols="10" md="7">
                <v-card height="100%">
                    <v-fade-transition hide-on-leave>
                    <component :is="nanotaskTemplateComponent" @submit="submit" @updateAnswer="updateAnswer"/>
                    </v-fade-transition>
                </v-card>
            </v-col>
            <v-col cols="10" md="3">
                <v-card height="100%" color="grey lighten-3">
                    <v-list-item three-line>
                        <v-list-item-content>
                            <div class="overline mb-4">ANSWER DATA</div>
                            <vue-json-pretty :data="currentAnswer" style="line-height:1.4em;"></vue-json-pretty>
                        </v-list-item-content>
                    </v-list-item>
                </v-card>
            </v-col>
        </v-row>

        <dialog-submit-answer ref="dlgSubmitAnswer" :answer="sentAnswer" />
        <dialog-create-template ref="dlgCreateTemplate" :duct="duct" :project="project ? project.name : null" />

    </v-main>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty/lib/vue-json-pretty'
import DialogSubmitAnswer from './DialogSubmitAnswer.vue'
import DialogCreateTemplate from './DialogCreateTemplate.vue'
import 'vue-json-pretty/lib/styles.css'

export default {
    components: {
        VueJsonPretty,
        DialogSubmitAnswer,
        DialogCreateTemplate,
    },
    data: () => ({
        templateName: null,
        currentAnswer: {},
        sentAnswer: {},
    }),
    props: ["duct", "sharedProps","name"],
    computed: {
        project() { return this.sharedProps.project },

        nanotaskTemplateComponent() {
            if(this.project && this.project.name && this.templateName){
                return require(`@/projects/${this.project.name}/templates/${this.templateName}/Main.vue`).default;
            } else { return null }
        },

        isTemplateSelectDisabled() {
            return !this.project || !this.project.templates || Object.keys(this.project.templates).length==0
        },
        templateNames() {
            if(this.project && this.project.templates) return Object.keys(this.project.templates);
            else return [];
        }
    },
    methods: {
        updateAnswer($event) {
            this.currentAnswer = $event;
        },
        submit($event) {
            this.sentAnswer = $event;
            this.$refs.dlgSubmitAnswer.shown = true;
        },
    },
    watch: {
        "project.name"() { this.templateName = null },
        templateName() { this.currentAnswer = {} }
    }
}
</script>
