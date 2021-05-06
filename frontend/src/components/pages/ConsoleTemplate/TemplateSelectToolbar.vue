<template>
    <div>
        <v-toolbar class="pa-0 ma-0 grey lighten-4">
            <v-row align="end" justify="center">
                <v-col cols="6">
                    <v-select
                        width="300"
                        :hide-details="!templateCreated"
                        messages="Page refresh may be required for rendering the new templates"
                        :items="tmplNamesWithAux"
                        v-model="tmplName"
                        label="Template name">
                        <template v-if="templateCreated" v-slot:message="{ message }">
                            <span style="color:darkorange;font-weight:bold;">{{ message }}</span>
                        </template>
                    </v-select>
                </v-col>

                <v-col cols="2">
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                fab
                                small
                                icon
                                v-on="on"
                                v-bind="attrs"
                                :disabled="!prjName"
                                @click.stop="$refs.dialogCreateTemplate.show()">
                                <v-icon dark>mdi-plus-box-multiple-outline</v-icon>
                            </v-btn>
                        </template>
                        <span>Create New Template...</span>
                    </v-tooltip>
                </v-col>
            </v-row>
        </v-toolbar>

        <tutti-dialog
            ref="dialogCreateTemplate"
            maxWidth="400"
            title="Create New Template"
            :allowEnter="true"
            :actions="[
                {
                    label: 'Create',
                    color: 'indigo darken-1',
                    text: true,
                    disableByRule: true,
                    onclick: createTemplate
                },
                {
                    label: 'Cancel',
                    color: 'grey darken-1',
                    text: true
                }
            ]">
            <template v-slot:body>

                <v-text-field
                    filled
                    autofocus
                    v-model="newTemplateName"
                    prepend-icon="mdi-pencil"
                    label="Enter Template Name"
                    :rules="[rules.required, rules.alphanumeric]">
                </v-text-field>

                <v-autocomplete
                    dense
                    filled
                    v-model="newTemplatePreset"
                    :items="presetsList"
                    prepend-icon="mdi-shape"
                    label="Choose Preset Template"
                    :rules="[rules.required]">
                </v-autocomplete>

            </template>
        </tutti-dialog>

    </div>
</template>

<script>
import TuttiDialog from '@/views/assets/Dialog.vue'
import rules from '@/lib/input-rules'

export default {
    components: {
        TuttiDialog
    },
    data: () => ({
        rules,

        templateCreated: false,
        tmplNames: [],
        tmplName: null,
        newTemplateName: "",
        newTemplatePreset: [],
        presets: [],
    }),
    props: ["duct", "prjName"],
    computed: {
        tmplNamesWithAux() {
            return [...this.tmplNames, "[Instruction]", "[Preview]"];
        },
        presetsList() { return this.presets.map((val) => ({ text: `${val[0]} - ${val[1]}`, value: val })); },
    },
    methods: {
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

    },
    watch: {
        prjName() { this.listTemplates(); },
        tmplName(val) {
            this.currentAnswer = {};
            this.$emit("template-select", val);
        }
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
