<template>
    <v-dialog v-model="shown" max-width="400">
      <v-card>
        <v-card-title class="headline">Create New Project</v-card-title>
        <v-form v-model="valid" @submit.prevent="create">
            <v-card-text>
                <v-text-field autofocus v-model="newProjectName" filled prepend-icon="mdi-pencil" label="Enter Project Name" :rules="[rules.required, rules.alphanumeric]"></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="shown=false" >Cancel</v-btn>
              <v-btn color="primary" text :disabled="!valid" @click="create">Create</v-btn>
            </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
</template>

<script>
import store from '@/store.js'
import { mapGetters } from 'vuex'

export default {
    store,
    computed: {
        ...mapGetters("ductsModule", [ "duct" ])
    },
    data: () => ({
        shown: false,
        valid: false,
        newProjectName: "",
        rules: {
            required: value => !!value || "This field is required",
            alphanumeric: value => {
                const pattern = /^[a-zA-Z0-9_-]*$/;
                return pattern.test(value) || 'Alphabets, numbers, "_", or "-" is only allowed';
            }
        }
    }),
    methods: {
        create() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.PROJECT,
                data: {
                    "Command": "Create",
                    "ProjectName": this.newProjectName
                }
            });
            this.shown = false;
        }
    }
}
</script>
