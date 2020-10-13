<template>
    <v-dialog v-model="shown" max-width="400">
      <v-card>
        <v-card-title class="headline">Set MTurk Account</v-card-title>
        <v-form @submit.prevent="setAccount">
            <v-card-text>
                <v-text-field autofocus v-model="accessKeyId" filled label="Access Key Id"></v-text-field>
                <v-text-field v-model="secretAccessKey" filled label="Access Key Id"></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="shown=false" >Cancel</v-btn>
              <v-btn color="primary" text :disabled="isBtnDisabled" @click="setAccount">Set Account</v-btn>
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
            return (this.accessKeyId=="" || this.secretAccessKey=="")
        }
    },
    data: () => ({
        shown: false,
        accessKeyId: "",
        secretAccessKey: ""
    }),
    methods: {
        setAccount() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_ACCOUNT,
                data: `set ${this.accessKeyId} ${this.secretAccessKey}`
            });
            this.shown = false;
        }
    }
}
</script>
