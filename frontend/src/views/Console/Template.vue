<template>
    <!--<v-main class="mt-10 grey lighten-4">-->
    <v-main>
        <v-toolbar class="grey lighten-4">
            <v-row class="ml-5 mr-0 pr-0" align="end" justify="center">
                <v-col cols="6">
                    <v-select width="300" :hide-details="!templateCreated" messages="Page refresh may be required for rendering the new templates" :items="tmplNames" v-model="tmplName" label="Template name" :disabled="tmplNames.length==0">
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

        <v-navigation-drawer app clipped right class="grey lighten-4">
            <div class="pa-4">
                <div class="overline mb-4">ANSWER DATA</div>
                <vue-json-pretty :data="currentAnswer" style="line-height:1.4em;"></vue-json-pretty>
            </div>
        </v-navigation-drawer>

        <v-fade-transition hide-on-leave>
            <component :is="tmplComponent" @submit="submit" @updateAnswer="updateAnswer"/>
        </v-fade-transition>

        <tutti-dialog ref="dialogCreateTemplate" maxWidth="400" title="Create New Template"
            :actions="[
                { label: 'Create', color: 'indigo darken-1', text: true, disableByRule: true, onclick: createTemplate },
                { label: 'Cancel', color: 'grey darken-1', text: true }
            ]">
            <template v-slot:body>
                <v-text-field autofocus v-model="newTemplateName" filled prepend-icon="mdi-pencil" label="Enter Template Name" :rules="rules.tmplName"></v-text-field>
                <v-autocomplete v-model="newTemplatePreset" :items="presetsList" dense filled prepend-icon="mdi-shape" label="Choose Preset Template" :rules="rules.preset"></v-autocomplete>
            </template>
        </tutti-dialog>

        <tutti-dialog ref="dialogSubmitAnswer" maxWidth="700"
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
import VueJsonPretty from 'vue-json-pretty/lib/vue-json-pretty'
import Dialog from '@/views/assets/Dialog.vue'
import rules from '@/lib/input-rules'
import 'vue-json-pretty/lib/styles.css'

export default {
    components: {
        VueJsonPretty,
        TuttiDialog: Dialog
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
            if(this.prjName && this.tmplName){ return require(`@/projects/${this.prjName}/templates/${this.tmplName}/Main.vue`).default; }
            else { return null; }
        },

        presetsList() { return this.presets.map((val) => ({ text: `${val[0]} - ${val[1]}`, value: val })); }
    },
    methods: {
        updateAnswer($event) {
            this.currentAnswer = $event;
        },
        createTemplate() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.CREATE_TEMPLATES,
                data: {
                    "ProjectName": this.prjName,
                    "TemplateNames": [this.newTemplateName],
                    "PresetEnvName": this.newTemplatePreset[0],
                    "PresetTemplateName": this.newTemplatePreset[1]
                }
            });
            this.newTemplateName = "";
            this.newTemplatePreset = [];
            this.templateCreated = true;
        },
        listTemplatePresets() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.LIST_TEMPLATE_PRESETS,
                data: null
            });
        },
        listTemplates() {
            this.tmplName = null;
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.LIST_TEMPLATES,
                data: { "ProjectName": this.prjName }
            });
        },

        submit($event) {
            this.sentAnswer = $event;
            this.$refs.dialogSubmitAnswer.show();
        },
    },
    watch: {
        prjName() { this.listTemplates(); },
        tmplName() { this.currentAnswer = {} }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.setTuttiEventHandler(this.duct.EVENT.CREATE_TEMPLATES, () => {
                this.listTemplates();
            });
            this.duct.addTuttiEvtHandler({
                eid: this.duct.EVENT.LIST_TEMPLATE_PRESETS,
                success: ({ data }) => {
                    this.presets = data["Presets"];
                }
            });
            this.duct.addTuttiEvtHandler({
                eid: this.duct.EVENT.LIST_TEMPLATES, 
                success: ({ data }) => {
                    this.tmplNames = data["Templates"];
                }
            });

            this.listTemplatePresets();
            if(this.prjName) this.listTemplates();
        });
    }
}
</script>
