<template>
    <v-dialog v-model="shown" max-width="400">
      <v-card>
        <v-card-title class="headline">Create New Template</v-card-title>
        <v-form v-model="valid" @submit.prevent="create">
            <v-card-text>
                <v-text-field autofocus v-model="newTemplateName" filled prepend-icon="mdi-pencil" label="Enter Template Name" :rules="[rules.required, rules.alphanumeric]"></v-text-field>
                <v-autocomplete v-model="newTemplatePreset" :items="presetsList" dense filled prepend-icon="mdi-shape" label="Choose Preset Template"></v-autocomplete>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="shown=false" >Cancel</v-btn>
              <v-btn color="primary" text :disabled="!valid" @click="create" >Create</v-btn>
            </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
</template>

<script>
export default {
    computed: {
        presetsList() {
            var l = []
            for(var i in this.presets){
                l.push({
                    text: `${this.presets[i][0]} - ${this.presets[i][1]}`,
                    value: this.presets[i]
                });
            }
            return l;
        }
    },
    data: () => ({
        shown: false,
        valid: false,
        newTemplateName: "",
        newTemplatePreset: "",
        rules: {
            required: value => !!value || "This field is required",
            alphanumeric: value => {
                const pattern = /^[a-zA-Z0-9_-]*$/;
                return pattern.test(value) || 'Alphabets, numbers, "_", or "-" is only allowed';
            }
        },
        presets: {}
    }),
    props: ["duct", "project"],
    methods: {
        create() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.CREATE_TEMPLATES,
                data: {
                    "ProjectName": this.project,
                    "TemplateNames": [this.newTemplateName],
                    "PresetEnvName": this.newTemplatePreset[0],
                    "PresetTemplateName": this.newTemplatePreset[1]
                }
            });
            this.newTemplateName = "";
            this.newTemplatePreset = "";
            this.shown = false;
        }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.LIST_TEMPLATE_PRESETS,
                data: null
            });
            this.duct.addEvtHandler({
                tag: this.name,
                eid: this.duct.EVENT.LIST_TEMPLATE_PRESETS,
                handler: (rid, eid, data) => {
                    this.$set(this, "presets", data["Data"]["Presets"]);
                }
            });
        });
    }
}
</script>
