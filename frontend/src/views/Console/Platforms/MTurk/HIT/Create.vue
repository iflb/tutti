<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1000px" class="mx-auto">
            <v-card>
                <v-card-title>
                    Assign HIT Type
                </v-card-title>
                <v-card-text>
                    <v-radio-group class="mt-0" fixed top hide-details v-model="createNew">
                        <v-radio label="Create new HIT type" :value="true"></v-radio>
                        <v-radio label="Choose from existing HIT type" :value="false"></v-radio>
                    </v-radio-group>
                </v-card-text>

                <div v-if="!createNew">
                    <v-card-subtitle><b>Existing HIT Types</b></v-card-subtitle>
                    <v-simple-table dense>
                        <template v-slot:default>
                            <thead><tr style="background-color:#eee;">
                                <th></th>
                                <th>Name</th>
                                <th>HIT Type ID</th>
                                <th>Action</th>
                            </tr></thead>
                            <tbody>
                                <tr v-for="hitType in exstHITTypes" :key="hitType.HITTypeId">
                                    <td><v-radio-group class="ma-0 pa-0" dense hide-details v-model="chosenExstHITTypeId"><v-radio :value="hitType.HITTypeId"></v-radio></v-radio-group></td>
                                    <td>{{ hitType.name }}</td>
                                    <td>{{ hitType.HITTypeId }}</td>
                                    <td><v-btn small>Copy to new</v-btn></td>
                                </tr>
                            </tbody>
                        </template>
                    </v-simple-table>
                    <v-divider></v-divider>
                </div>

                <v-card-subtitle><b>HIT Type Info</b></v-card-subtitle>
                <v-simple-table dense>
                    <template v-slot:default>
                        <thead><tr style="background-color:#eee;">
                            <th>Attribute</th>
                            <th>Value</th>
                        </tr></thead>
                        <tbody>
                            <tr v-for="attr in attributes" :key="attr.name">
                                <td>{{ attr.name }}</td>
                                <td v-if="createNew"><input style="border: 1px solid #bbb; padding: 0 5px;" type="text" v-model="attr.value" /></td>
                                <td v-if="!createNew">{{ attr.value }}</td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-card>
        </div>
    </v-main>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'

export default {
    data: () => ({
        createNew: null,
        chosenExstHITTypeId: "hoge1",
        exstHITTypes: [
            {
                name: "my type 1",
                HITTypeId: "AAAAAAA"
            },
            {
                name: "my type 2",
                HITTypeId: "BBBBBB"
            },
            {
                name: "my type 3",
                HITTypeId: "CCCCCCCCCC"
            },
        ],
        defaultAttributes: [
            { name: "Reward", value: 0.01 },
            { name: "Title", value: "" },
            { name: "Description", value: "" },
            { name: "Keywords", value: "" },
            { name: "AutoApprovalDelayInSeconds", value: 600 },
            { name: "AssignmentDurationInSeconds", value: 1800 },
            { name: "QualificationRequirements", value: [] }
        ],
        attributes: []
    }),
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
    },
    watch: {
        createNew(value) {
            if(value) this.attributes = Object.assign({}, this.defaultAttributes);
            else {
                this.duct.sendMsg({
                    tag: "/console/platform/mturk/hit/create/",
                    eid: this.duct.EVENT.MTURK_HIT,
                    data: {
                        "Command": "LoadHITType",
                        "HITTypeId": this.chosenExstHITTypeId
                    }
                });
            }
        }
    },
    created() {
        this.createNew = true;
        this.onDuctOpen(() => {
            this.duct.addEvtHandler({
                tag: "/console/platform/mturk/hit/create/",
                eid: this.duct.EVENT.MTURK_HIT,
                handler: (rid, eid, data) => {
                    if(data["Status"]=="Error") return;

                    const command = data["Data"]["Command"];
                    switch(command) {
                        case "LoadHITType": {
                            this.attributes = data["Data"]["HITTypeAttributes"];
                            break;
                        }
                    }
                }
            });
        });
    }
};
</script>
