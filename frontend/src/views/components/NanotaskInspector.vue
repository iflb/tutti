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
export default {
    data: () => ({
        projects: [],
        templates: [],
        projectName: null,
        templateName: null,
        componentName: "NanotaskInspector"
    }),
    props: ["duct"],
    mounted: function(){
        if(this.duct) {
            this.duct.setState(this.componentName)
            this.duct.send(this.duct.next_rid(), this.duct.EVENT.LIST_PROJECTS, null)
        }
    },
    computed: {
        nanotaskTemplateComponent: {
            cache: true,
            get: function() {
                if(this.projectName && this.templateName){
                    return require(`@/projects/${this.projectName}/templates/${this.templateName}/Main.vue`).default;
                } else { return null }
            }
        },
        currentAnswer() { return JSON.stringify(this.$store.getters.currentAnswer, undefined, 4) },

        isTemplateSelectDisabled() { return this.templates.length==0 }
    },
    methods: {
        onDuctOpen(){
            this.duct.setChildEventHandler("NanotaskInspector", this.duct.EVENT.LIST_PROJECTS, this.receivedProjectsList)
            this.duct.setChildEventHandler("NanotaskInspector", this.duct.EVENT.LIST_TEMPLATES, this.receivedTemplatesList)
            this.duct.setState(this.componentName)

            this.duct.send(this.duct.next_rid(), this.duct.EVENT.LIST_PROJECTS, null)
        },
        receivedProjectsList(rid, eid, data){ this.projects = data },
        receivedTemplatesList(rid, eid, data){ this.templates = data },
        launchProductionMode(){ window.open(`/vue/prod/private/${this.projectName}`); }
    },
    watch: {
        projectName() {
            this.duct.send(this.duct.next_rid(), this.duct.EVENT.LIST_TEMPLATES, this.projectName)
        }
    }
}
</script>
