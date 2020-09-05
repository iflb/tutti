<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row justify="center">
            <v-col cols="10">
            <v-card class="pa-3">
                <v-row justify="center">
                    <v-col cols="12" lg="8">
                        <v-row class="justify-start ml-5 mr-0 pr-0" align="center">
                            <v-col cols="10">
                                <v-select width="300" hide-details :items="project.templates" v-model="templateName" label="Template name" :disabled="isTemplateSelectDisabled"></v-select>
                            </v-col>
                            <v-col cols="2">
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn fab small icon v-on="on" v-bind="attrs" :disabled="project.name==''" @click.stop="dialog.createTemplate = true"><v-icon dark>mdi-plus-box-multiple-outline</v-icon></v-btn>
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

        <v-dialog v-model="dialog.submitAnswer" persistent max-width="700">
            <v-card>
                <v-card-title class="text-h6"><v-icon class="mr-2" color="green">mdi-check-circle</v-icon>Answers are submitted successfully</v-card-title>
                <v-card-text><vue-json-pretty :data="sentAnswer"></vue-json-pretty></v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="dialog.submitAnswer = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="dialog.createTemplate" max-width="400">
          <v-card>
            <v-card-title class="headline">Create New Template</v-card-title>
            <v-form v-model="isFormValid.createTemplate" @submit.prevent="createTemplate(); dialog.createTemplate = false">
                <v-card-text>
                    <v-text-field autofocus v-model="newTemplateName" filled prepend-icon="mdi-pencil" label="Enter Template Name" :rules="[rules.required, rules.alphanumeric]"></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn text @click="dialog.createTemplate = false" >Cancel</v-btn>
                  <v-btn color="primary" text :disabled="!isFormValid.createTemplate" @click="createTemplate(); dialog.createTemplate = false" >Create</v-btn>
                </v-card-actions>
            </v-form>
          </v-card>
        </v-dialog>

    </v-main>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'
import VueJsonPretty from 'vue-json-pretty'

export default {
    store,
    components: {
        VueJsonPretty
    },
    data: () => ({
        templateName: null,
        currentAnswer: {},
        sentAnswer: {},
        newTemplateName: "",
        dialog: {
            submitAnswer: false,
            createTemplate: false
        },
        isFormValid: {
            createTemplate: false
        },
        rules: {
            required: value => !!value || "This field is required",
            alphanumeric: value => {
                const pattern = /^[a-zA-Z0-9_-]*$/;
                return pattern.test(value) || 'Alphabets, numbers, "_", or "-" is only allowed';
            }
        }
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

        isTemplateSelectDisabled() {
            return this.project.templates.length==0 || !this.project.name
        }
    },
    methods: {
        updateAnswer($event) {
            this.currentAnswer = $event;
        },
        submit($event) {
            this.dialog.submitAnswer = true;
            this.sentAnswer = $event;
        },
        createTemplate() {
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.CREATE_TEMPLATE, data: `${this.project.name} ${this.newTemplateName} Default` })
        }
    },
    watch: {
        "project.name"() { this.templateName = null },
        templateName() { this.currentAnswer = {} }
    }
}
</script>
