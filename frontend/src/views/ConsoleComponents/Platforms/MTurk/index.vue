<template>
    <v-main class="grey lighten-4">
        <div v-if="crd">
            <v-system-bar
                v-if="crd.Sandbox"
                dark
                color="warning">
                <span>Current mode is set to <b>SANDBOX</b>.</span>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            icon
                            v-bind="attrs"
                            v-on="on"
                            @click="setSandbox(false)"
                            :loading="loading">
                            <v-icon>mdi-swap-horizontal</v-icon>
                        </v-btn>
                    </template>
                    <span>Change to production mode</span>
                </v-tooltip>

                <v-spacer></v-spacer>

                <span>
                    AccessKeyId:
                    <b>{{ crd.AccessKeyId }}</b>
                </span>
            </v-system-bar>

            <v-system-bar
                v-else
                dark
                color="error">
                <span>Current mode is set to <b>PRODUCTION</b>. Real payments can happen.</span>

                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            icon
                            v-bind="attrs"
                            v-on="on"
                            @click="setSandbox(true)"
                            :loading="loading">
                            <v-icon>mdi-swap-horizontal</v-icon>
                        </v-btn>
                    </template>
                    <span>Change to sandbox mode</span>
                </v-tooltip>

                <v-spacer></v-spacer>

                <span>
                    AccessKeyId:
                    <b>{{ crd.AccessKeyId }}</b>
                    (Balance: <b>${{ crd.AccountBalance.AvailableBalance }}</b>)
                </span>
            </v-system-bar>
        </div>
        <div v-else>
            <v-system-bar color="grey lighten-2">
                <span v-if="loading">
                    Loading credentials...
                    <v-btn icon disabled loading></v-btn>
                </span>

                <span v-else>
                    No valid credential is currently set
                </span>
            </v-system-bar>
        </div>

        <keep-alive :exclude="['HIT-Create']">
            <router-view :duct="duct" :prjName="prjName" :credentials="crd"></router-view>
        </keep-alive>
    </v-main>
</template>
<script>
export default {
    data: () => ({
        crd: null,
        loading: false
    }),
    props: ["duct", "prjName"],
    methods: {
        onReceiveCredentials(crd) {
            this.loading = false;
            this.crd = crd;
        },
        getCredentials() {
            this.loading = true;
            this.duct.controllers.mturk.getCredentials();
        },
        setSandbox(Enabled) {
            this.loading = true;
            this.duct.controllers.mturk.setSandbox(Enabled);
        }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.mturk.on([
                    "getCredentials",
                    "setCredentials",
                    "clearCredentials",
                    "setSandbox"
                ],
                {
                    success: (data) => {
                        this.onReceiveCredentials(data["Results"]);
                    }
                }
            );

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
