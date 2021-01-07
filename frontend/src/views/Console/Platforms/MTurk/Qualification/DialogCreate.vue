<template>
    <v-dialog v-model="shown" max-width="600">
      <v-card>
        <v-card-title class="headline">Set MTurk Account</v-card-title>
        <v-form @submit.prevent="setAccount">
            <v-card-text>
                <v-row>
                    <v-col cols="12">
                        <v-text-field prepend-icon="mdi-label" v-model="qualParams.Name" filled label="Name" dense hide-details/>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="12">
                        <v-text-field prepend-icon="mdi-message-text" v-model="qualParams.Description" filled label="Description" dense hide-details/>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="6"><v-switch v-model="qualParams.AutoGranted" color="indigo" hide-details label="AutoGranted" /></v-col>
                </v-row>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="shown=false" >Cancel</v-btn>
              <v-btn color="indigo" text :disabled="isBtnDisabled" @click="create">Create</v-btn>
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
        ...mapGetters("ductsModule", [ "duct" ]),
        isBtnDisabled() {
            return (this.qualName=="" || this.qualDescription=="")
        }
    },
    data: () => ({
        shown: false,
        qualParams: {
            Name: "",
            Description: "",
            AutoGranted: false,
            QualificationTypeStatus: "Active"
        }
    }),
    methods: {
        create() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_CREATE_QUALIFICATION,
                data: this.qualParams
            });
            this.shown = false;
        }
    }
}
</script>
