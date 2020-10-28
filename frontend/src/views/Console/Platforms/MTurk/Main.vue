<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1000px" class="mx-auto">
        <v-row align="center" justify="center" class="my-6">
            <v-col cols="3">
                <v-img src="https://pbs.twimg.com/profile_images/1067838660035280897/XJfH-OpK_400x400.jpg"></v-img>
            </v-col>
            <v-col cols="7">
                <div class="text-h3">Amazon Mechanical Turk</div>
                <v-row class="mt-4">
                    <v-btn class="ma-2" color="green" dark @click="windowOpen('https://worker.mturk.com', '_blank');">Workers</v-btn>
                    <v-btn class="ma-2" color="orange" dark @click="windowOpen('https://requester.mturk.com', '_blank');">Requesters</v-btn>
                </v-row>
                <v-row>
                    <v-btn class="ma-2" color="green" outlined @click="windowOpen('https://workersandbox.mturk.com', '_blank');">Workers sandbox</v-btn>
                    <v-btn class="ma-2" color="orange" outlined @click="windowOpen('https://requestersandbox.mturk.com', '_blank');">Requesters sandbox</v-btn>
                </v-row>
            </v-col>
        </v-row>
        <v-card v-if="!isAccountSet">
            <v-card-text>
                MTurk account is not set. 
                <v-btn text color="indigo" @click="$refs.dlgSetAccount.shown=true">Set account</v-btn>
            </v-card-text>
        </v-card>
        <v-card v-if="isAccountSet">
            <v-card-text>
                Access Key ID: {{ accessKeyId }}<br>
                Secret Access Key: {{ secretAccessKey }}<br>
                Balance: ${{ sharedProps.mTurkAccount.availableBalance }} <span v-if="'onHoldBalance' in sharedProps.mTurkAccount">(on hold: {{ sharedProps.mTurkAccount.onHoldBalance }})</span>
            </v-card-text>
        </v-card>
        <dialog-set-account ref="dlgSetAccount" />
        <v-row>
            <v-col cols="4">
                <v-card>
                    <v-img src="https://media.istockphoto.com/videos/stack-of-files-documents-being-piled-onto-office-desk-video-id825340524?s=640x640" max-height="150"></v-img>
                    <v-card-title>HITs</v-card-title>
                    <v-card-text>Create, custormize, or remove task batches.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text>Manage HITs</v-btn></v-card-actions>
                </v-card>
            </v-col>
            <v-col cols="4">
                <v-card>
                    <v-img src="https://us.123rf.com/450wm/aniwhite/aniwhite1603/aniwhite160300174/53982937-stock-vector-the-crowd-of-abstract-people-flat-design-vector-illustration-.jpg?ver=6" max-height="150"></v-img>
                    <v-card-title>Workers</v-card-title>
                    <v-card-text>Check workers' status, block or contact workers, or grant qualifications.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text>Manage workers</v-btn></v-card-actions>
                </v-card>
            </v-col>
            <v-col cols="4">
                <v-card>
                    <v-img src="https://assets.st-note.com/production/uploads/images/30971758/rectangle_large_type_2_d321a7db4258595199bc6a264e7b320b.jpg?fit=bounds&format=jpeg&quality=45&width=960" max-height="150"></v-img>
                    <v-card-title>Qualifications</v-card-title>
                    <v-card-text>Create or remove qualifications.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text to="qual/">Manage qualifications</v-btn></v-card-actions>
                </v-card>
            </v-col>
        </v-row>
        </div>
    </v-main>
</template>
<script>
import DialogSetAccount from './DialogSetAccount.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
    props: ["sharedProps","name"],
    components: { DialogSetAccount },
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        accessKeyId() {
            try { return this.sharedProps.mTurkAccount.accessKeyId;
            } catch { return null; }
        },
        secretAccessKey() {
            try { return this.sharedProps.mTurkAccount.secretAccessKey;
            } catch { return null; }
        },
        isAccountSet() {
            return this.accessKeyId && this.secretAccessKey;
        }
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
        windowOpen(url, target){
            window.open(url, target);
        },
        init() {

        }
    },
    mounted() {
        this.onDuctOpen(() => {
            if(Object.keys(this.sharedProps.mTurkAccount).length==0) {
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.MTURK_ACCOUNT, data: "get" });
                this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.MTURK_REQUESTER_INFO, data: null });
            }
        });
    }
}
</script>
