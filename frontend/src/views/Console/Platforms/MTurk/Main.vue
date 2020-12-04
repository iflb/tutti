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
                    <v-btn class="ma-2" color="indigo" outlined @click="windowOpen('https://worker.mturk.com', '_blank');"><v-icon>mdi-account-group</v-icon>Workers</v-btn>
                    <v-btn class="ma-2" color="indigo" outlined @click="windowOpen('https://requester.mturk.com', '_blank');"><v-icon>mdi-account-circle</v-icon>Requesters</v-btn>
                </v-row>
            </v-col>
        </v-row>
        <v-card v-if="!isAccountSet" :loading="credentialRequested">
            <v-card-text>
                MTurk account is not set. 
                <v-btn text color="indigo" @click="$refs.dlgSetAccount.shown=true">Set account</v-btn>
            </v-card-text>
        </v-card>
        <v-card v-if="isAccountSet" :loading="credentialRequested">
            <v-alert v-if="sharedProps.mTurkAccount.isSandbox==0" dense text type="warning">You are in the <b>production mode</b>; real payments can happen</v-alert>
            <v-card-text>
                Access Key ID: {{ accessKeyId }}<br>
                Secret Access Key: {{ secretAccessKey }}<br>
                Balance: ${{ sharedProps.mTurkAccount.availableBalance }} <span v-if="'onHoldBalance' in sharedProps.mTurkAccount">(on hold: {{ sharedProps.mTurkAccount.onHoldBalance }})</span>
            </v-card-text>
            <v-card-text class="pt-0">
            <v-btn outlined color="indigo" v-text="sharedProps.mTurkAccount.isSandbox==0 ? 'Change to sandbox' : 'Change to production'" @click="setSandboxMode(!sharedProps.mTurkAccount.isSandbox)"></v-btn>
            <v-btn class="ml-3" color="grey" outlined @click="clearCredentials()">Clear credentials</v-btn>
            </v-card-text>
        </v-card>
        <dialog-set-account ref="dlgSetAccount" />
        <v-row>
            <v-col cols="4">
                <v-card>
                    <v-img src="https://media.istockphoto.com/videos/stack-of-files-documents-being-piled-onto-office-desk-video-id825340524?s=640x640" max-height="150"></v-img>
                    <v-card-title>HITs</v-card-title>
                    <v-card-text>Create, custormize, or remove task batches.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text to="hit">Manage HITs</v-btn></v-card-actions>
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
    data: () => ({
        credentialRequested: true
    }),
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
        getCredentials() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.AMT,
                data: { "Command": "GetCredentials" }
            });
        },
        setSandboxMode() {
            this.credentialRequested = true;
            this.duct.sendMsg({ tag: this.name, eid: this.duct.EVENT.AMT, data: { "Command": "SetSandboxMode", "Enabled": this.sharedProps.mTurkAccount.isSandbox==1 ? 0 : 1 } });
        },
        clearCredentials() {
            this.credentialRequested = true;
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.AMT,
                data: {
                    "Command": "ResetAuthorization"
                }
            });
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            this.$set(this.sharedProps, "mTurkAccount", {});
            this.duct.addEvtHandler({
                tag: "/console/platform/mturk/", eid: this.duct.EVENT.AMT,
                handler: (rid, eid, data) => {
    
                    if(data["Status"]=="Error") return;
    
                    const command = data["Data"]["Command"];
                    switch(command){
                        case "GetCredentials": {
                            this.$set(this.sharedProps.mTurkAccount, "accessKeyId", data["Data"]["AccessKeyId"]);
                            this.$set(this.sharedProps.mTurkAccount, "secretAccessKey", data["Data"]["SecretAccessKey"]);
                            this.$set(this.sharedProps.mTurkAccount, "isSandbox", data["Data"]["IsSandbox"]);

                            if(data["Data"]["AccountBalance"]) {
                                this.$set(this.sharedProps.mTurkAccount, "availableBalance", data["Data"]["AccountBalance"]["AvailableBalance"]);
                                if("OnHoldBalance" in data["Data"]["AccountBalance"]){
                                    this.$set(this.sharedProps.mTurkAccount, "onHoldBalance", data["Data"]["AccountBalance"]["OnHoldBalance"]);
                                }
                            }
                            this.credentialRequested = false;
                            break;
                        }
                        case "SetSandboxMode":
                        case "SetCredentials":
                        case "ResetAuthorization": {
                            this.getCredentials();
                            break;
                        }
                    }
                }
            });
            this.getCredentials();
        });
    }
}
</script>
