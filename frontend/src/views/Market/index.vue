<template>
    <v-app>
        <v-main>
            <v-toolbar
                dense
                dark
                color="light-green"
                >
                <v-row>
                    <v-col cols="4" class="text-subtitle-1">
                        Tutti Market
                    </v-col>
                    <v-col cols="4" class="text-h6" align="center" style="align-items:center">
                        Some image comparison tasks ($0.10)
                    </v-col>
                    <v-col cols="4" class="text-caption" align="right">
                        Your Worker ID: <b>{{ workerId }}</b>
                        <copy-to-clipboard-btn x-small class="ml-1" :text="workerId" />
                    </v-col>
                </v-row>
            </v-toolbar>
            <v-container fluid>
                <v-row>
                    <v-col
                        md="2"
                        offset-md="5"
                        align="center"
                        justify="center"
                        style="background-color:#ffffc4;"
                        class="text-button pt-0 pb-0"
                        >
                            00:10:05 / 00:30:00
                    </v-col>
                </v-row>
            </v-container>
            <iframe
                src="/workplace/handson-image?workerId=hoge2"
                frameborder="0"
                :style="style"
                ref="iframe"
                />
        </v-main>
    </v-app>
</template>
<script>
import CopyToClipboardBtn from "@/components/ui/CopyToClipboardBtn"

export default {
    components: {
        CopyToClipboardBtn
    },
    data: () => ({
        workerId: 'HOGEWORKERID',
        style: {
            width: '100%',
            height: 'calc(100vh - 100px)',
            backgroundColor: 'white',
            border: '1px solid #ccc'
        },
    }),
    computed: {
        tableRowsTwoColumns() {
            return this.tableRows.map(
                (r,i) => (i+1==this.tableRows.length ? [r, null] : [r, this.tableRows[i+1]])
                ).filter((r,i) => (i%2==0));
        }
    },
    mounted() {
        setTimeout(() => {
            let iframe = document.querySelector('iframe').contentWindow;
            console.log(iframe);
            iframe.postMessage({
                action: 'SyncMessage',
                message: 'Hello'
            }, '*');
        }, 2000);
    }
}
</script>
