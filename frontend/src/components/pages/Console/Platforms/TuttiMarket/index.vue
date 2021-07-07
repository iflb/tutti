<template>
    <v-main class="grey lighten-4">
        <div>
            <v-toolbar>
                <v-row justify="center">
                    <v-col cols="8">
                        <v-select
                            :items="registeredPlatforms"
                            hide-details
                            />
                    </v-col>
                </v-row>
            </v-toolbar>
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
        loading: false,
        registeredPlatforms: [
            { text: 'TEAI annotators', value: 'teai' },
            { text: 'YAHATA Techno Center workers', value: 'yht-techno' }
        ],
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
