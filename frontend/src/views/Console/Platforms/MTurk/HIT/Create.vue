<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1000px" class="mx-auto">
            <v-card>
                <v-card-title>
                    Assign HIT Type <v-btn icon @click="openNewWindow('https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkRequester/Concepts_HITTypesArticle.html');"><v-icon>mdi-help-circle-outline</v-icon></v-btn>
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
                                <tr v-for="(params,htid) in exstHITTypes" :key="htid">
                                    <td><v-radio-group class="ma-0 pa-0" dense hide-details v-model="chosenExstHITTypeId"><v-radio :value="htid"></v-radio></v-radio-group></td>
                                    <td>{{ params.Title }}</td>
                                    <td>{{ htid }}</td>
                                    <td><v-btn small text color="indigo">Copy to new</v-btn></td>
                                </tr>
                            </tbody>
                        </template>
                    </v-simple-table>
                    <v-divider></v-divider>
                </div>

                <v-card-subtitle><b>HIT Type Params</b> <v-btn icon @click="openNewWindow('https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_CreateHITTypeOperation.html');"><v-icon>mdi-help-circle-outline</v-icon></v-btn></v-card-subtitle>
                <v-simple-table dense>
                    <template v-slot:default>
                        <thead><tr style="background-color:#eee;">
                            <th>Attribute</th>
                            <th>Value</th>
                        </tr></thead>
                        <tbody>
                            <tr v-for="attr in attributeOptions" :key="attr.name">
                                <td>{{ attr.name }}</td>
                                <td v-if="createNew">
                                    <v-text-field v-bind="attr.attrs" dense hide-details v-model="attributes[attr.name]"></v-text-field>
                                </td>
                                <td v-if="!createNew">{{ attributes[attr.name] }}</td>
                            </tr>
                            <tr v-for="(qualItem, qualIndex) in attributes.QualificationRequirements" :key="'QualificationRequirements-'+qualIndex">
                                <td> QualificationRequirements - {{ qualIndex+1 }} </td>
                                <td>
                                    <v-simple-table dense>
                                        <tbody>
                                            <tr>
                                                <td>QualificationTypeId</td>
                                                <td v-if="createNew"><v-autocomplete v-model="qualItem['QualificationTypeId']" dense hide-details :items="allQualIds"></v-autocomplete></td>
                                                <td v-if="!createNew">{{ qualItem['QualificationTypeId'] }}</td>
                                            </tr>
                                            <tr>
                                                <td>Comparator</td>
                                                <td v-if="createNew"><v-select v-model="qualItem['Comparator']" dense hide-details :items="qualRequirementOptions['Comparator']"></v-select></td>
                                                <td v-if="!createNew">{{ qualItem['Comparator'] }}</td>
                                            </tr>
                                            <tr>
                                                <td>IntegerValues</td>
                                                <td v-if="createNew"><v-combobox v-model="qualItem['IntegerValues']" multiple dense small-chips hide-details append-icon :rules="[rules.numbers]"></v-combobox></td>
                                                <td v-if="!createNew">{{ qualItem['IntegerValues'] }}</td>
                                            </tr>
                                            <tr v-for="(localeItem, localeIndex) in qualItem.LocaleValues" :key="'LocaleValues-'+localeIndex">
                                                <td>LocaleValues - {{ localeIndex+1 }}</td>
                                                <td>
                                                    <v-simple-table dense>
                                                        <template v-slot:default>
                                                            <tbody>
                                                                <tr>
                                                                    <td>Country</td>
                                                                    <td v-if="createNew"><v-text-field v-model="localeItem.Country" dense hide-details></v-text-field></td>
                                                                    <td v-if="!createNew">{{ localeItem.Country }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Subdivision</td>
                                                                    <td v-if="createNew"><v-text-field v-model="localeItem.Subdivision" dense hide-details></v-text-field></td>
                                                                    <td v-if="!createNew">{{ localeItem.Subdivision }}</td>
                                                                </tr>
                                                            </tbody>
                                                        </template>
                                                    </v-simple-table>
                                                </td>
                                            </tr>
                                            <tr v-if="createNew">
                                                <td>
                                                    <b>{{ numLocaleValues(qualItem) }} LocaleValues</b>
                                                    <v-btn x-small icon @click="pushLocaleValues(qualItem)"><v-icon>mdi-plus</v-icon></v-btn>
                                                    <v-btn x-small icon @click="popLocaleValues(qualItem)"><v-icon>mdi-minus</v-icon></v-btn>
                                                </td>
                                                <td></td>
                                            </tr>
                                            <tr>
                                                <td>ActionsGuarded</td>
                                                <td v-if="createNew"><v-select v-model="qualItem['ActionsGuarded']" dense hide-details :items="qualRequirementOptions['ActionsGuarded']"></v-select></td>
                                                <td v-if="!createNew">{{ qualItem["ActionsGuarded"] }}</td>
                                            </tr>
                                        </tbody>
                                    </v-simple-table>
                                </td>
                            </tr>
                            <tr v-if="createNew">
                                <td>
                                    <b>{{ numQualRequirements }} QualificationRequirements</b>
                                    <v-btn x-small icon @click="openNewWindow('https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html#ApiReference_QualificationType-IDs');"><v-icon>mdi-help-circle-outline</v-icon></v-btn>
                                    <v-btn x-small icon @click="pushQualRequirements()"><v-icon>mdi-plus</v-icon></v-btn>
                                    <v-btn x-small icon @click="popQualRequirements()" v-if="numQualRequirements"><v-icon>mdi-minus</v-icon></v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-card>
            <v-card class="mt-5">
                <v-card-title>Create HITs</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col cols="2"> <b>Project:</b> </v-col>
                        <v-col cols="4"> <v-text-field outlined dense hide-details disabled v-model="sharedProps.project.name"></v-text-field> </v-col>
                    </v-row>
                </v-card-text>
                <v-card-text>
                    <v-alert dense outlined border="left" class="text-caption" type="warning" >Make sure the project name is correct. If not, change it in the top navigation bar.</v-alert>
                </v-card-text>
                <v-card-text>
                    <v-row>
                        <v-col cols="2"> <b># of HITs to post:</b> </v-col>
                        <v-col cols="2"> <v-text-field outlined dense hide-details type="number" min=0 step=1 v-model.number="numCreateHITs"></v-text-field> </v-col>
                    </v-row>
                </v-card-text>
                <v-card-subtitle><b>HIT Params</b> <v-btn icon @click="openNewWindow('https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_CreateHITWithHITTypeOperation.html');"><v-icon>mdi-help-circle-outline</v-icon></v-btn></v-card-subtitle>
                <v-simple-table dense>
                    <template v-slot:default>
                        <thead><tr style="background-color:#eee;">
                            <th>Attribute</th>
                            <th>Value</th>
                        </tr></thead>
                        <tbody>
                            <tr>
                                <td>MaxAssignments</td>
                                <td><v-text-field dense hide-details disabled type="number" min=1 step=1 v-model="createHITParams.MaxAssignments"></v-text-field></td>
                            </tr>
                            <tr>
                                <td>LifetimeInSeconds</td>
                                <td><v-text-field dense hide-details type="number" min=0 step=10 v-model="createHITParams.LifetimeInSeconds"></v-text-field></td>
                            </tr>
                            <tr>
                                <td>RequesterAnnotation</td>
                                <td><v-text-field dense hide-details v-model="createHITParams.RequesterAnnotation"></v-text-field></td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-card>
            <v-row class="mb-8">
                <v-col class="text-right">
                    <v-btn dark :loading="postingHITs" color="indigo" @click="postHITs()">Post HITs</v-btn>
                </v-col>
            </v-row>

            <v-snackbar :color="snackbar.success.color" v-model="snackbar.success.shown" :timeout="snackbar.success.timeout">
              {{ snackbar.success.text }}
              <template v-slot:action="{ attrs }">
                  <v-btn dark color="white" text v-bind="attrs" @click="snackbar.success.shown=false">Close</v-btn>
              </template>
            </v-snackbar>
        </div>
    </v-main>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'

export default {
    data: () => ({
        hitTypes: [],

        attributeOptions: [
            { name: "Reward", attrs: { type: "number", min: 0, step: 0.01 } },
            { name: "Title" },
            { name: "Description" },
            { name: "Keywords" },
            { name: "AutoApprovalDelayInSeconds", attrs: { type: "number", min: 0, step: 10 } },
            { name: "AssignmentDurationInSeconds", attrs: { type: "number", min: 0, step: 10 } },
        ],
        qualRequirementOptions: {
            "Comparator": [
                    "LessThan",
                    "LessThanOrEqualTo",
                    "GreaterThan",
                    "GreaterThanOrEqualTo",
                    "EqualTo",
                    "NotEqualTo",
                    "Exists",
                    "DoesNotExist",
                    "In",
                    "NotIn"
                ],
            "ActionsGuarded": [
                    "Accept",
                    "PreviewAndAccept",
                    "DiscoverPreviewAndAccept"
                ]
        },
        qualIds: [
            { id: "2ARFPLSP75KLA8M8DH1HTEQVJT3SY6", name: "Masters (Sandbox)" },
            { id: "2F1QJWKUDD8XADTFD2Q0G6UTO95ALH", name: "Masters (Production)" },
            { id: "00000000000000000040", name: "Worker_NumberHITsApproved" },
            { id: "00000000000000000071", name: "Worker_Locale" },
            { id: "00000000000000000060", name: "Worker_Adult" },
            { id: "000000000000000000L0", name: "Worker_PercentAssignmentsApproved" }
        ],
        customQualIds: [],

        createNew: null,
        chosenExstHITTypeId: "",
        exstHITTypes: [],


        defaultAttributes: {
            "Reward": 0.01,
            "Title": "",
            "Description": "",
            "Keywords": "",
            "AutoApprovalDelayInSeconds": 600,
            "AssignmentDurationInSeconds": 1800,
            "QualificationRequirements": []
        },
        defaultQualRequirements: {
            "QualificationTypeId": "",
            "Comparator": "",
            "IntegerValues": [],
            "LocaleValues": [],
            "ActionsGuarded": ""
        },
        attributes: [],
        
        createHITParams: {
            "MaxAssignments": 1,
            "LifetimeInSeconds": 3600,
            "RequesterAnnotation": ""
        },
        numCreateHITs: 1,


        rules: {
            numbers: value => {
                const pattern = /^[0-9]*$/;
                var ret = true;
                for(const i in value) if(!pattern.test(value[i])) { ret = false; value.splice(i,1); break; }
                return ret || '';
            }
        },

        postingHITs: false,
        snackbar: {
            success: {
                shown: false,
                text: "",
                timeout: 5000,
                color: "success"
            },
        }
    }),
    props: ["sharedProps"],
    computed: {
        ...mapGetters("ductsModule", [ "duct" ]),
        numQualRequirements() {
            if(this.attributes && this.attributes.QualificationRequirements)
                return this.attributes.QualificationRequirements.length;
            else return 0;
        },
        allQualIds() {
            var ret = [];
            for(const i in this.qualIds){
                const id = this.qualIds[i].id;
                const name = this.qualIds[i].name;
                ret.push({ text: `${name} - ${id}`, value: id });
            }
            for(const i in this.customQualIds){
                const id = this.customQualIds[i].id;
                const name = this.customQualIds[i].name;
                ret.push({ text: `${name} - ${id}`, value: id });
            }
            return ret;
        }
    },
    methods: {
        ...mapActions("ductsModule", [ "onDuctOpen" ]),
        openNewWindow(url) {
            window.open(url, "_blank");
        },

        pushQualRequirements() { this.attributes.QualificationRequirements.push(Object.assign({}, this.defaultQualRequirements)); },
        popQualRequirements()  { this.attributes.QualificationRequirements.pop(); },

        numLocaleValues(item)  { return (item && item.LocaleValues) ? item.LocaleValues.length : 0; },
        pushLocaleValues(item) { item.LocaleValues.push({ "Country": "", "Subdivision": "" }); },
        popLocaleValues(item)  { item.LocaleValues.pop(); },

        _evtMTurkHIT(data) {
            this.duct.sendMsg({
                tag: "/console/platform/mturk/hit/create/",
                eid: this.duct.EVENT.MTURK_HIT,
                data: data
            });
        },

        createHITType() {
            var qrs = this.attributes.QualificationRequirements;
            for(const i in qrs) for(const j in qrs[i]["IntegerValues"]) qrs[i]["IntegerValues"][j] = parseInt(qrs[i]["IntegerValues"][j]);
            this.attributes.Reward = this.attributes.Reward.toString();
            this.attributes.AutoApprovalDelayInSeconds = parseInt(this.attributes.AutoApprovalDelayInSeconds);
            this.attributes.AssignmentDurationInSeconds = parseInt(this.attributes.AssignmentDurationInSeconds);

            this._evtMTurkHIT({ "Command": "CreateHITType", "Params": this.attributes });
        },

        createHITsForHITTypeId(htid) {
            //console.log({
            //    "Command": "CreateHIT",
            //    "Params": { "HITTypeId": htid, ...this.createHITParams },
            //    "NumHITs": this.numCreateHITs
            //});
            this._evtMTurkHIT({
                "Command": "CreateHITWithHITType",
                "ProjectName": this.sharedProps.project.name,
                "Params": { "HITTypeId": htid, ...this.createHITParams },
                "NumHITs": this.numCreateHITs
            });
        },

        postHITs() {
            this.postingHITs = true;
            if(this.createNew){ this.createHITType(); }
            else { this.createHITsForHITTypeId(this.chosenExstHITTypeId); }
        },
        _evtGetQualificationTypeIds() {
            this.duct.sendMsg({
                tag: this.name,
                eid: this.duct.EVENT.MTURK_QUALIFICATION,
                data: { "Command": "List" }
            });
        }
    },
    watch: {
        chosenExstHITTypeId(value) {
            if(value!="") this.attributes = this.exstHITTypes[value];
        },
        createNew(value) {
            this.chosenExstHITTypeId = "";
            if(value) this.attributes = Object.assign({}, this.defaultAttributes);
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
                        case "ListHITTypes": {
                            this.exstHITTypes = data["Data"]["HITTypes"];
                            break;
                        }
                        case "CreateHITType": {
                            const htid = data["Data"]["HITTypeId"];
                            this.createHITsForHITTypeId(htid);
                            break;
                        }
                        case "CreateHITWithHITType": {
                            this.postingHITs = false;
                            this.snackbar.success.text = "Successfully posted HITs";
                            this.snackbar.success.shown = true;
                            break;
                        }
                    }
                }
            });

            this.duct.addEvtHandler({
                tag: this.name, eid: this.duct.EVENT.MTURK_QUALIFICATION,
                handler: (rid, eid, data) => {
                    const command = data["Data"]["Command"];
                    if(data["Status"]=="error") return;

                    if(command=="List"){
                        var ret = [];
                        for(var i in data["Data"]["QualificationTypes"]) {
                            const id = data["Data"]["QualificationTypes"][i]["QualificationTypeId"];
                            const name = data["Data"]["QualificationTypes"][i]["Name"];
                            ret.push({ id, name });
                        }
                        this.customQualIds = ret;
                    }
                }
            });
            this._evtMTurkHIT({ "Command": "ListHITTypes" });
        });

        this._evtGetQualificationTypeIds();
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
