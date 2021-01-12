<template>
    <v-main class="grey lighten-4">
        <div v-if="credentials">
            <v-system-bar v-if="credentials.Sandbox" dark color="warning">
                <span>Current mode is set to <b>SANDBOX</b>.</span>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn icon v-bind="attrs" v-on="on" @click="setSandbox(false)" :loading="loadingCredentials"><v-icon>mdi-swap-horizontal</v-icon></v-btn>
                    </template>
                    <span>Change to production mode</span>
                </v-tooltip>
                <v-spacer></v-spacer>
                <span>AccessKeyId: <b>{{ credentials.AccessKeyId }}</b></span>
            </v-system-bar>
            <v-system-bar v-else dark color="error">
                <span>Current mode is set to <b>PRODUCTION</b>. Real payments can happen.</span>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn icon v-bind="attrs" v-on="on" @click="setSandbox(true)" :loading="loadingCredentials"><v-icon>mdi-swap-horizontal</v-icon></v-btn>
                    </template>
                    <span>Change to sandbox mode</span>
                </v-tooltip>
                <v-spacer></v-spacer>
                <span>AccessKeyId: <b>{{ credentials.AccessKeyId }}</b> (Balance: <b>${{ credentials.AccountBalance.AvailableBalance }}</b>)</span>
            </v-system-bar>
        </div>
        <div v-else>
            <v-system-bar color="grey lighten-2">
                <span v-if="loadingCredentials">Loading credentials... <v-btn icon disabled loading></v-btn></span>
                <span v-else>No valid credential is currently set</span>
            </v-system-bar>
        </div>

        <v-slide-x-transition hide-on-leave>
            <router-view :credentials="credentials"></router-view>
        </v-slide-x-transition>
    </v-main>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
export default {
    data: () => ({
        credentials: null,
        loadingCredentials: false
    }),
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),

        onReceiveCredentials(rid, eid, data) {
            this.loadingCredentials = false;
            this.credentials = data["Data"]["Results"];
        },

        getCredentials() {
            this.loadingCredentials = true;
            this.duct.sendMsg({
                tag: "",
                eid: this.duct.EVENT["MTURK_GET_CREDENTIALS"],
                data: null
            });
        },
        setSandbox(Enabled) {
            this.loadingCredentials = true;
            this.duct.sendMsg({
                tag: "",
                eid: this.duct.EVENT["MTURK_SET_SANDBOX"],
                data: { Enabled }
            });
        }
    },
    mounted() {
        this.onDuctOpen(() => {
            const credEvtNames = ["MTURK_GET_CREDENTIALS", "MTURK_SET_CREDENTIALS", "MTURK_CLEAR_CREDENTIALS", "MTURK_SET_SANDBOX"];
            for(var i in credEvtNames)  this.duct.addEvtHandler({ tag: "", eid: this.duct.EVENT[credEvtNames[i]], handler: this.onReceiveCredentials });

            this.getCredentials();
        });
    }
}
</script>
