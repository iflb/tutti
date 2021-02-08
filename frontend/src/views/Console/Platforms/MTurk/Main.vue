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

        <keep-alive :exclude="['HIT-Create']">
            <router-view :duct="duct" :prjName="prjName" :credentials="credentials"></router-view>
        </keep-alive>
    </v-main>
</template>
<script>
export default {
    data: () => ({
        credentials: null,
        loadingCredentials: false
    }),
    props: ["duct", "prjName"],
    methods: {
        onReceiveCredentials({ data }) {
            this.loadingCredentials = false;
            this.credentials = data["Results"];
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
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            const credEvtNames = [
                "MTURK_GET_CREDENTIALS",
                "MTURK_SET_CREDENTIALS",
                "MTURK_CLEAR_CREDENTIALS",
                "MTURK_SET_SANDBOX"
            ];
            for(const e of credEvtNames) {
                this.duct.addTuttiEvtHandler({
                    eid: this.duct.EVENT[e],
                    success: this.onReceiveCredentials
                });
            }

            this.getCredentials();
        });
    }
}
</script>
<style>
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.5s;
  transition-property: opacity;
  transition-timing-function: ease-in;
}

.fade-enter-active {
  transition-duration: 0.5s;
}

.fade-enter,
.fade-leave-active {
  opacity: 0
}
</style>
