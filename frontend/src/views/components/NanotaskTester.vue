<template>
    <v-main>
        <v-container mt-0 pa-0>
        <v-toolbar prominent flat height="150px" fill-height>
            <v-toolbar-title>
            <v-row>
                <v-col>
                    <v-select :items="projects" v-model="projectName" label="Project name"></v-select>
                </v-col>
                <v-col>
                    <v-select :items="templates" v-model="templateName" label="Template name" :disabled="isTemplateSelectDisabled"></v-select>
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
export default {
    data: () => ({
        projects: [],
        templates: [],
        projectName: null,
        templateName: null
    }),
    mounted() {
        this.initOnMount()
    },
    computed: {
        nanotaskTemplateComponent: {
            cache: true,
            get: function() {
                if(this.projectName && this.templateName){
                    return require(`@/projects/${this.projectName}/templates/${this.templateName}/Main.vue`).default;
                } else {
                    return null
                }
            }
        },
        currentAnswer() { return JSON.stringify(this.$store.getters.currentAnswer, undefined, 4) },

        ws() { return this.$store.getters.ws },
        wsd() { return this.$store.getters.wsd },
        isWSOpened() { return this.$store.getters.isWSOpened },
        isTemplateSelectDisabled() { return this.templates.length==0 }
    },
    methods: {
        initOnMount(){
            if(!this.ws || !this.wsd){ return }

            this.$store.dispatch("setOnMessageHandler", [this.wsd.EVENT["LIST_PROJECTS"], this.receivedProjectsList])
            this.$store.dispatch("setOnMessageHandler", [this.wsd.EVENT["LIST_TEMPLATES"], this.receivedTemplatesList])

            if(this.isWSOpened){
                this.$store.dispatch("sendWSMessage", [this.wsd.EVENT["LIST_PROJECTS"], []]);
            }
        },
        receivedProjectsList(rid, eid, data){
            this.projects = data
        },
        receivedTemplatesList(rid, eid, data){
            this.templates = data
        },
    },
    watch: {
        isWSOpened() {
            this.initOnMount();
        },
        projectName() {
            this.$store.dispatch("sendWSMessage", [this.wsd.EVENT["LIST_TEMPLATES"], [this.projectName]]);
        }
    }
}
</script>

<style>
/*
#nanotask-test {
    width: 100%;
    height: 800px;
    margin-top: 50px;
}
#selectboxes {
    display: flex;
    justify-content: center;
}
#selectboxes>* {
    max-width: 300px;
    margin: 0 10px;
}
#nanotask-test-inner {
    width: 90%;
    margin: 0 auto;
    display: flex;
    height: 100%;
    justify-content: center;
}
#nanotask-test-inner>* {
    height: 80%;
    margin: 0 10px;
}
#left { width: 70%; }
#right { width: 15%; }
textarea {
    width: 100%;
    height: 100%;
    background: #ddd;
    font-weight: bold;
    box-sizing: border-box;
}
*/
</style>
