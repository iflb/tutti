<template>
    <!--<v-main class="mt-10 grey lighten-4">-->
    <v-main>
        <v-toolbar class="pa-0 ma-0 grey lighten-4">
            <v-row align="end" justify="center">
                <v-col cols="6">
                    <v-select width="300" :hide-details="!templateCreated" messages="Page refresh may be required for rendering the new templates" :items="tmplNamesWithAux" v-model="tmplName" label="Template name">
                        <template v-if="templateCreated" v-slot:message="{ message }">
                            <span style="color:darkorange;font-weight:bold;">{{ message }}</span>
                        </template>
                    </v-select>
                </v-col>
                <v-col cols="2">
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn fab small icon v-on="on" v-bind="attrs" :disabled="!prjName" @click.stop="$refs.dialogCreateTemplate.show()"><v-icon dark>mdi-plus-box-multiple-outline</v-icon></v-btn>
                        </template>
                        <span>Create New Template...</span>
                    </v-tooltip>
                </v-col>
            </v-row>
        </v-toolbar>

        <v-divider></v-divider>

        <v-row style="height:calc(100% - 53px)">
            <v-col cols="10">
                <v-fade-transition hide-on-leave>
                    <component :is="tmplComponent" @submit="submit" @updateAnswer="updateAnswer"/>
                </v-fade-transition>
            </v-col>
            <v-col cols="2" class="px-0 pb-0">
                <v-card elevation="0" tile color="grey lighten-5" class="pa-4" height="100%">
                    <div class="overline mb-4">ANSWER DATA</div>
                    <vue-json-pretty :data="currentAnswer" style="line-height:1.4em;"></vue-json-pretty>
                </v-card>
            </v-col>
        </v-row>

        <tutti-dialog ref="dialogCreateTemplate" maxWidth="400" title="Create New Template" :allowEnter="true"
            :actions="[
                { label: 'Create', color: 'indigo darken-1', text: true, disableByRule: true, onclick: createTemplate },
                { label: 'Cancel', color: 'grey darken-1', text: true }
            ]">
            <template v-slot:body>
                <v-text-field autofocus v-model="newTemplateName" filled prepend-icon="mdi-pencil" label="Enter Template Name" :rules="rules.tmplName"></v-text-field>
                <v-autocomplete v-model="newTemplatePreset" :items="presetsList" dense filled prepend-icon="mdi-shape" label="Choose Preset Template" :rules="rules.preset"></v-autocomplete>
            </template>
        </tutti-dialog>

        <tutti-dialog ref="dialogSubmitResponse" maxWidth="700"
            :actions="[
                { label: 'Close', color: 'indigo darken-1', text: true }
            ]">
            <template v-slot:title>
                <v-icon class="mr-2" color="green">mdi-check-circle</v-icon>Answers are submitted successfully
            </template>
            <template v-slot:body>
                <vue-json-pretty :data="sentAnswer"></vue-json-pretty>
            </template>
        </tutti-dialog>
    </v-main>
</template>

<script>
import rules from '@/lib/input-rules'
import 'vue-json-pretty/lib/styles.css'

export default {
    components: {
        VueJsonPretty: () => import('vue-json-pretty/lib/vue-json-pretty'),
        TuttiDialog: () => import('@/views/assets/Dialog.vue')
    },
    data: () => ({
        rules: {
            tmplName: [rules.required, rules.alphanumeric],
            preset: [rules.required]
        },

        tmplNames: [],
        tmplName: null,
        presets: [],
        templateCreated: false,

        // for answer input test
        currentAnswer: {},
        sentAnswer: {},

        // for template creation
        newTemplateName: "",
        newTemplatePreset: [],
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

        presetsList() { return this.presets.map((val) => ({ text: `${val[0]} - ${val[1]}`, value: val })); },

        tmplNamesWithAux() {
            return [...this.tmplNames, "[Instruction]", "[Preview]"];
        }
    },
    methods: {
        updateAnswer($event) {
            this.currentAnswer = $event;
        },
        createTemplate() {
            this.duct.controllers.resource.createTemplates(this.prjName, [this.newTemplateName], this.newTemplatePreset[0], this.newTemplatePreset[1]);
            this.newTemplateName = "";
            this.newTemplatePreset = [];
            this.templateCreated = true;
        },
        listTemplates() {
            this.tmplName = null;
            if(this.prjName) this.duct.controllers.resource.listTemplates(this.prjName);
        },

        submit($event) {
            this.sentAnswer = $event;
            this.$refs.dialogSubmitResponse.show();
        },
    },
    watch: {
        prjName() { this.listTemplates(); },
        tmplName() { this.currentAnswer = {} }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("createTemplates", {
                success: this.listTemplates
            });
            this.duct.eventListeners.resource.on("listTemplatePresets", {
                success: (data) => {
                    this.presets = data["Presets"];
                }
            });
            this.duct.eventListeners.resource.on("listTemplates", {
                success: (data) => {
                    this.tmplNames = data["Templates"];
                }
            });

            this.duct.controllers.resource.listTemplatePresets();
            this.listTemplates();
        });
    }
}
</script>
<style scoped>
#toolbar {
    border-bottom: thin;
}
</style>
