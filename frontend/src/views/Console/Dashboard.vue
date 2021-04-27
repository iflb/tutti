<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row justify="center">
            <v-col cols="9">
                <v-card>
                    <v-card-text>
                        <b>Production URL</b>: <a :href="url">{{ url }}</a><copy-to-clipboard-btn x-small class="ml-1" :text="url"></copy-to-clipboard-btn><br>
                        <b>Development URL</b>: <a :href="devUrl">{{ devUrl }}</a><copy-to-clipboard-btn x-small class="ml-1" :text="devUrl"></copy-to-clipboard-btn><br>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-main>
</template>
<script>
import { getUrl } from "@/lib/tutti-env.js"

export default {
    components: {
        CopyToClipboardBtn: () => import("@/components/CopyToClipboardBtn")
    },
    data: () => ({
    }),
    props: [ "prjName" ],
    computed: {
        url() { return getUrl(this.prjName); },
        devUrl() { return getUrl(this.prjName, true); },
    }
}
</script>
