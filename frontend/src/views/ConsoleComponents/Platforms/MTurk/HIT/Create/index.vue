<template>
    <v-row class="my-10" justify="center">
        <v-col cols="10">
            <hit-type-form-card :duct="duct" @update="updateHITTypeParams" />
        </v-col>
        <v-col cols="10">
            <hit-form-card
                @update="updateHITParams"
                :prjName="prjName"
                />
        </v-col>
        <v-col v-if="projectHasDiff" cols="10">
            <v-alert
                border="left"
                type="error">
                Seems like your project has been updated since last build.
                &nbsp;&nbsp;&nbsp;
                <v-btn
                    color="white"
                    outlined
                    :loading="rebuildingProject"
                    @click="rebuildProject">
                    Rebuild
                </v-btn>
            </v-alert>
        </v-col>
        <v-col v-else cols="10" class="text-right">
            <post-hits-button
                :duct="duct"
                :prjName="prjName"
                :HITTypeParams="HITTypeParams"
                :HITParams="HITParams"
                :numCreateHITs="numCreateHITs"
                :credentials="credentials"
                :createNew="createNew"
                :chosenExstHITTypeId="chosenExstHITTypeId"
                />
        </v-col>
        {{ HITTypeParams }}
    </v-row>
</template>
<script>
import HITTypeFormCard from './HITTypeFormCard'
import HITFormCard from './HITFormCard'
import PostHITsButton from './PostHITsButton'

export default {
    name: "HIT-Create",
    props: ["duct", "credentials", "prjName"],
    components: {
        "hit-type-form-card": HITTypeFormCard,
        "hit-form-card": HITFormCard,
        "post-hits-button": PostHITsButton,
    },
    data: () => ({
        projectHasDiff: false,
        rebuildingProject: false,

        HITTypeParams: null,
        HITParams: null,
        numCreateHITs: 1,
        createNew: true,
        chosenExstHITTypeId: "",
    }),
    methods: {
        checkProjectDiff() {
            console.log(this.prjName);
            this.duct.send(
                this.duct.next_rid(),
                this.duct.EVENT.CHECK_PROJECT_DIFF,
                { "ProjectName": this.prjName }
            );
        },
        rebuildProject() {
            this.rebuildingProject = true;
            this.duct.send(
                this.duct.next_rid(),
                this.duct.EVENT.REBUILD_PRODUCTION_ENVIRONMENT,
                { "ProjectName": this.prjName }
            );
        },

        updateHITTypeParams(params, createNew, chosenExstHITTypeId) {
            this.HITTypeParams = params;
            this.createNew = createNew;
            this.chosenExstHITTypeId = chosenExstHITTypeId;
        },
        updateHITParams(target, val) {
            if(target=="HITParams" || target=="numCreateHITs") this[target] = val;
        }
    },
    watch: {
        prjName(val) {
            if(val) this.checkProjectDiff();
        }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.setEventHandler( this.duct.EVENT.CHECK_PROJECT_DIFF, (rid,eid,data) => {
                console.log(data["Contents"]);
                if(data["Contents"]["HasDiff"]) this.projectHasDiff = true;
            });

            this.duct.setEventHandler( this.duct.EVENT.REBUILD_PRODUCTION_ENVIRONMENT, () => {
                this.rebuildingProject = false;
                setTimeout(() => { this.projectHasDiff = false; }, 1000);
            });
        });
    }
};
</script>
<style scoped>
.input-native {
    border: 1px solid #bbb;
    padding: 0 5px;
    appearance: auto;
}
</style>
