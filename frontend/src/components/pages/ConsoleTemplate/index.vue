<template>
    <v-main>
        <template-select-toolbar
            :duct="duct"
            :prjName="prjName"
            @template-select="updateTemplateName">
        </template-select-toolbar>

        <v-row style="height:calc(100% - 53px)">
            <v-col cols="10">
                <v-fade-transition hide-on-leave>
                    <component
                        :is="tmplComponent"
                        @submit="showSubmitResults"
                        @response-update="updateResponse"/>
                </v-fade-transition>
            </v-col>
            <v-col cols="2" class="px-0 pb-0">
                <response-card :response="response"></response-card>
            </v-col>
        </v-row>


        <tutti-dialog
            ref="dialogSubmitResponse"
            maxWidth="700"
            :actions="[
                {
                    label: 'Close',
                    color: 'indigo darken-1',
                    text: true
                }
            ]">
            <template v-slot:title>
                <v-icon class="mr-2" color="green">mdi-check-circle</v-icon>Answers are submitted successfully
            </template>
            <template v-slot:body>
                <vue-json-pretty :data="sentResponse"></vue-json-pretty>
            </template>
        </tutti-dialog>
    </v-main>
</template>

<script>
import TemplateSelectToolbar from './TemplateSelectToolbar'
import ResponseCard from './ResponseCard'
import TuttiDialog from '@/views/assets/Dialog.vue'
import 'vue-json-pretty/lib/styles.css'
import VueJsonPretty from 'vue-json-pretty/lib/vue-json-pretty'

export default {
    components: {
        TemplateSelectToolbar,
        ResponseCard,
        TuttiDialog,
        VueJsonPretty
    },
    data: () => ({
        tmplName: "",

        response: {},
        sentResponse: {},
    }),
    props: ["name", "duct", "prjName"],
    computed: {
        tmplComponent() {
            if(this.prjName && this.tmplName){
                if(this.tmplName=="[Instruction]")
                    return require(`@/projects/${this.prjName}/templates/Instruction.vue`).default;
                else if(this.tmplName=="[Preview]")
                    return require(`@/projects/${this.prjName}/templates/Preview.vue`).default;
                else
                    return require(`@/projects/${this.prjName}/templates/${this.tmplName}/Main.vue`).default;

            }
            else { return null; }
        },


    },
    methods: {
        updateTemplateName(name) {
            this.tmplName = name;
        },
        updateResponse($event) {
            this.response = $event;
        },
        showSubmitResults($event) {
            this.sentResponse = $event;
            this.$refs.dialogSubmitResponse.show();
        },
    },
}
</script>
<style scoped>
#toolbar {
    border-bottom: thin;
}
</style>
