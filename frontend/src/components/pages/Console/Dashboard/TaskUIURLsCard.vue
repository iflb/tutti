<template>
    <v-card>
        <v-card-title>
            Visit Tutti Task UI:
        </v-card-title>
        <v-card-text>
            <div v-if="projectHasDiff">
                Production URL is not available since "{{ prjName }}" seems to be changed since the last build.
                <v-btn outlined small color="grey" :loading="rebuildingProject" @click="rebuildProject">Rebuild now</v-btn>
            </div>
            <div v-else>
                <b>Production URL</b>: <a :href="url" target="_blank">{{ url }}</a><copy-to-clipboard-btn x-small class="ml-1" :text="url"></copy-to-clipboard-btn><br>
            </div>
            <b>Development URL</b>: <a :href="devUrl" target="_blank">{{ devUrl }}</a><copy-to-clipboard-btn x-small class="ml-1" :text="devUrl"></copy-to-clipboard-btn><br>
        </v-card-text>
    </v-card>
</template>
<script>
import { getUrl } from "@/lib/tutti-env.js"
import CopyToClipboardBtn from "@/components/ui/CopyToClipboardBtn"

export default {
    components: {
        CopyToClipboardBtn,
    },
    data: () => ({
        projectHasDiff: false,
        rebuildingProject: false,
    }),
    props: [ "prjName", "duct" ],
    computed: {
        url() { return getUrl(this.prjName); },
        devUrl() { return getUrl(this.prjName, true); },
    },
    methods: {
        checkProjectDiff(){
            this.duct.send(this.duct.next_rid(), this.duct.EVENT.CHECK_PROJECT_DIFF, {"ProjectName": this.prjName});
        },
        rebuildProject(){
            this.rebuildingProject = true;
            this.duct.send(this.duct.next_rid(), this.duct.EVENT.REBUILD_PRODUCTION_ENVIRONMENT, {"ProjectName": this.prjName});
        }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.checkProjectDiff();

            this.duct.setEventHandler( this.duct.EVENT.CHECK_PROJECT_DIFF, (rid,eid,data) => {
                this.projectHasDiff = data["Contents"]["HasDiff"];
            });

            this.duct.setEventHandler( this.duct.EVENT.REBUILD_PRODUCTION_ENVIRONMENT, () => {
                this.rebuildingProject = false;
                setTimeout(() => { this.projectHasDiff = false; }, 1000);
            });
        });
    },
    watch: {
        prjName() {
            this.checkProjectDiff();
        }
    }
}
</script>
