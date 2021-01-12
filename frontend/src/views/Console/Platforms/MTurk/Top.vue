<template>
    <div>
        <v-row align="center" justify="center" class="my-6">
            <v-col cols="2" class="text-center">
                <v-img :max-height="200" contain src="https://pbs.twimg.com/profile_images/1067838660035280897/XJfH-OpK_400x400.jpg"></v-img>
            </v-col>
            <v-col cols="5">
                <div class="text-h3">Amazon Mechanical Turk</div>
                <v-row class="mt-4">
                    <v-btn class="ma-2" color="indigo" outlined
                        @click="credentials && credentials.Sandbox ?
                                windowOpen('https://workersandbox.mturk.com', '_blank') :
                                windowOpen('https://worker.mturk.com', '_blank');">
                        <v-icon>mdi-account-group</v-icon>Workers
                    </v-btn>
                    <v-btn class="ma-2" color="indigo" outlined
                        @click="credentials && credentials.Sandbox ?
                                windowOpen('https://requestersandbox.mturk.com', '_blank') :
                                windowOpen('https://requester.mturk.com', '_blank');">
                        <v-icon>mdi-account-circle</v-icon>Requesters
                    </v-btn>
                </v-row>
            </v-col>
        </v-row>



        <v-row justify="center">
        <v-col cols="9">
            <v-card v-if="credentials">
                <v-card-text>
                    Access Key ID: {{ credentials.AccessKeyId }}<br>
                    Secret Access Key: {{ credentials.SecretAccessKey }}<br>
                    Balance: ${{ credentials.AccountBalance.AvailableBalance }}
                    <span v-if="'OnHoldBalance' in credentials.AccountBalance">
                        (on hold: {{ credentials.AccountBalance.OnHoldBalance }})
                    </span>
                </v-card-text>
                <v-card-text class="pt-0">
                    <v-btn class="ml-3" color="grey" outlined @click="clearCredentials()">Clear credentials</v-btn>
                </v-card-text>
            </v-card>
            <v-card v-else>
                <v-card-text>
                    MTurk account is not set. 
                    <v-btn text color="indigo" @click="$refs.dlgSetAccount.shown=true">Set account</v-btn>
                </v-card-text>
            </v-card>
        </v-col>
        </v-row>


        <dialog-set-account ref="dlgSetAccount" />


        <v-row justify="center">
            <v-col cols="3">
                <v-card>
                    <v-img src="https://media.istockphoto.com/videos/stack-of-files-documents-being-piled-onto-office-desk-video-id825340524?s=640x640" max-height="150"></v-img>
                    <v-card-title>HITs</v-card-title>
                    <v-card-text>Create, custormize, or remove task batches.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text to="hit">Manage HITs</v-btn></v-card-actions>
                </v-card>
            </v-col>
            <v-col cols="3">
                <v-card>
                    <v-img src="https://us.123rf.com/450wm/aniwhite/aniwhite1603/aniwhite160300174/53982937-stock-vector-the-crowd-of-abstract-people-flat-design-vector-illustration-.jpg?ver=6" max-height="150"></v-img>
                    <v-card-title>Workers</v-card-title>
                    <v-card-text>Check workers' status, block or contact workers, or grant qualifications.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text>Manage workers</v-btn></v-card-actions>
                </v-card>
            </v-col>
            <v-col cols="3">
                <v-card>
                    <v-img src="https://assets.st-note.com/production/uploads/images/30971758/rectangle_large_type_2_d321a7db4258595199bc6a264e7b320b.jpg?fit=bounds&format=jpeg&quality=45&width=960" max-height="150"></v-img>
                    <v-card-title>Qualifications</v-card-title>
                    <v-card-text>Create or remove qualifications.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text to="qual/">Manage qualifications</v-btn></v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>
<script>
import DialogSetAccount from './DialogSetAccount.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
    props: ["credentials", "name"],
    components: { DialogSetAccount },
    data: () => ({
    }),
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
        windowOpen(url, target){
            window.open(url, target);
        },

        clearCredentials() {
            this.duct.sendMsg({
                tag: "",
                eid: this.duct.EVENT["MTURK_CLEAR_CREDENTIALS"],
                data: null
            });
        }
    },
    mounted() {
    }
}
</script>
