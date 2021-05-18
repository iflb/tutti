<template>
    <v-card>
        <v-card-title>
            Assign HIT Type
            <help-button name="QualificationRequirements" />
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
                            <td>
                                <v-btn
                                    small
                                    text
                                    color="indigo"
                                    @click="copyToNew(htid)">
                                    Copy to new
                                </v-btn>
                            </td>
                        </tr>
                    </tbody>
                </template>
            </v-simple-table>
            <v-divider></v-divider>
        </div>

        <v-card-subtitle><b>HIT Type Params</b> <help-button name="CreateHITType" /></v-card-subtitle>
        <v-simple-table dense>
            <template v-slot:default>
                <thead><tr style="background-color:#eee;">
                    <th>Key</th>
                    <th>Value</th>
                </tr></thead>
                <tbody>
                    <tr v-for="option in HITTypeParamOptions" :key="option.name">
                        <td>{{ option.name }}</td>
                        <td v-if="createNew">
                            <v-text-field
                                dense
                                hide-details
                                v-bind="option.attrs"
                                v-model="HITTypeParams[option.name]" />
                        </td>
                        <td v-else>
                            {{ HITTypeParams[option.name] }}
                        </td>
                    </tr>
                    <tr v-for="(qualItem, qualIndex) in visibleQualificationRequirements" :key="'QualificationRequirements-'+qualIndex">
                        <td> QualificationRequirements -     {{ qualIndex+1 }} </td>
                        <td>
                            <v-simple-table dense>
                                <tbody>
                                    <tr>
                                        <td>QualificationTypeId</td>
                                        <td v-if="createNew">
                                            <v-autocomplete
                                                dense
                                                hide-details
                                                v-model="qualItem['QualificationTypeId']"
                                                :items="allQualIds" />
                                        </td>
                                        <td v-else>
                                            {{ qualItem['QualificationTypeId'] }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>Comparator</td>
                                        <td v-if="createNew">
                                            <v-select
                                                dense
                                                hide-details
                                                v-model="qualItem['Comparator']"
                                                :items="qualRequirementOptions['Comparator']" />
                                        </td>
                                        <td v-else>
                                            {{ qualItem['Comparator'] }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>IntegerValues</td>
                                        <td v-if="createNew">
                                            <v-combobox
                                                multiple
                                                dense
                                                small-chips
                                                hide-details
                                                append-icon
                                                v-model="qualItem['IntegerValues']"
                                                :rules="[rules.numbers]" />
                                        </td>
                                        <td v-else>
                                            {{ qualItem['IntegerValues'] }}
                                        </td>
                                    </tr>
                                    <tr v-for="(localeItem, localeIndex) in qualItem.LocaleValues" :key="'LocaleValues-'+localeIndex">
                                        <td>LocaleValues - {{ localeIndex+1 }}</td>
                                        <td>
                                            <v-simple-table dense>
                                                <template v-slot:default>
                                                    <tbody>
                                                        <tr>
                                                            <td>Country</td>
                                                            <td v-if="createNew">
                                                                <v-text-field
                                                                    dense
                                                                    hide-details
                                                                    v-model="localeItem.Country" />
                                                            </td>
                                                            <td v-else>
                                                                {{ localeItem.Country }}
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td>Subdivision</td>
                                                            <td v-if="createNew">
                                                                <v-text-field
                                                                    dense
                                                                    hide-details
                                                                    v-model="localeItem.Subdivision" />
                                                            </td>
                                                            <td v-else>
                                                                {{ localeItem.Subdivision }}
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </template>
                                            </v-simple-table>
                                        </td>
                                    </tr>
                                    <tr v-if="createNew">
                                        <td>
                                            <b>{{ getNumLocaleValues(qualItem) }} LocaleValues</b>
                                            <v-btn
                                                x-small
                                                icon
                                                @click="pushLocaleValues(qualItem)">
                                                <v-icon>mdi-plus</v-icon>
                                            </v-btn>
                                            <v-btn
                                                x-small
                                                icon
                                                @click="popLocaleValues(qualItem)">
                                                <v-icon>mdi-minus</v-icon>
                                            </v-btn>
                                        </td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>ActionsGuarded</td>
                                        <td v-if="createNew">
                                            <v-select
                                                dense
                                                hide-details
                                                v-model="qualItem['ActionsGuarded']"
                                                :items="qualRequirementOptions['ActionsGuarded']" />
                                        </td>
                                        <td v-else>
                                            {{ qualItem["ActionsGuarded"] }}
                                        </td>
                                    </tr>
                                </tbody>
                            </v-simple-table>
                        </td>
                    </tr>
                    <tr v-if="createNew">
                        <td>
                            <b>{{ visibleQualificationRequirements.length }} QualificationRequirement{{ visibleQualificationRequirements.length>1 ? "s" : "" }}</b>
                            <help-button x-small name="QualificationRequirements" />
                            <v-btn
                                x-small
                                icon
                                @click="pushQualRequirements()">
                                <v-icon>mdi-plus</v-icon>
                            </v-btn>
                            <v-btn
                                v-if="visibleQualificationRequirements.length"
                                x-small
                                icon
                                @click="popQualRequirements()">
                                <v-icon>mdi-minus</v-icon>
                            </v-btn>
                        </td>
                    </tr>
                </tbody>
            </template>
        </v-simple-table>
        <tutti-snackbar ref="snackbar" />
    </v-card>
</template>

<script>
import HelpButton from './HelpButton'
import TuttiSnackbar from '@/components/ui/TuttiSnackbar'
import rules from '@/lib/input-rules'
import {
    HITTypeParamOptions,
    defaultHITTypeParams,
    qualRequirementOptions,
    defaultQualRequirements,
    knownQualIds
} from './create-hit-manifest'

export default {
    components: {
        HelpButton,
        TuttiSnackbar
    },
    data: () => ({
        rules,
        qualRequirementOptions,
        HITTypeParamOptions,

        createNew: true,
        exstHITTypes: [],
        chosenExstHITTypeId: "",
        HITTypeParams: defaultHITTypeParams,
        customQualTypes: []
    }),
    props: ["duct"],
    computed: {
        allQualIds() {
            var ret = [];
            for(const i in knownQualIds){
                const id = knownQualIds[i].id;
                const name = knownQualIds[i].name;
                ret.push({ text: `${name} - ${id}`, value: id });
            }
            for(const id in this.customQualTypes){
                const name = this.customQualTypes[id].name;
                ret.push({ text: `${name} - ${id}`, value: id });
            }
            return ret;
        },
        visibleQualificationRequirements() {
            if(this.HITTypeParams && this.HITTypeParams.QualificationRequirements){
                let qrs = [];
                for(const qr of this.HITTypeParams.QualificationRequirements){
                    if( this.isTuttiQual(qr.QualificationTypeId) ) {
                        continue;
                    }

                    qrs.push(qr);
                }
                return qrs;
            } else {
                return [];
            }
        }
    },
    methods: {
        pushQualRequirements() {
            this.HITTypeParams.QualificationRequirements.push( Object.assign({}, defaultQualRequirements) );
        },
        popQualRequirements() {
            this.HITTypeParams.QualificationRequirements.pop();
        },
        getNumLocaleValues(item)  {
            return (item && item.LocaleValues) ? item.LocaleValues.length : 0;
        },
        pushLocaleValues(item) {
            if( !("LocaleValues" in item) ) this.$set(item, "LocaleValues", []);
            item.LocaleValues.push({ "Country": "", "Subdivision": "" });
        },
        popLocaleValues(item)  {
            item.LocaleValues.pop();
            if(item.LocaleValues.length==0) delete item.LocaleValues;
        },
        isTuttiQual(qtid){
            return (qtid
                   && (qtid in this.customQualTypes)
                   && this.customQualTypes[qtid].name.startsWith("TUTTI_HITTYPE_QUALIFICATION"))==true;
        },
        copyToNew(htid){
            this.createNew = true;
            this.$nextTick(() => {
                this.chosenExstHITTypeId = htid;
                this.$nextTick(() => {
                    this.HITTypeParams.QualificationRequirements.forEach((qr,i) => {
                        if(this.isTuttiQual(qr.QualificationTypeId)) {
                            delete this.HITTypeParams.QualificationRequirements[i];
                        }
                    });
                    this.$emit("update", this.HITTypeParams, this.createNew, this.chosenExstHITTypeId);
                });
            });
        }
    },
    watch: {
        chosenExstHITTypeId(value) {
            if(value!="") this.HITTypeParams = this.exstHITTypes[value];
        },
        createNew(v) {
            this.chosenExstHITTypeId = "";
            if(v) { this.HITTypeParams = Object.assign({}, defaultHITTypeParams); }

            this.$emit("update", this.HITTypeParams, this.createNew, this.chosenExstHITTypeId);
        },

        HITTypeParams: {
            deep: true,
            handler(params) {
                if(params){
                    params.AutoApprovalDelayInSeconds = parseInt(params.AutoApprovalDelayInSeconds);
                    params.AssignmentDurationInSeconds = parseInt(params.AssignmentDurationInSeconds);
                }
                this.$emit("update", params, this.createNew, this.chosenExstHITTypeId);
            }
        }
    },
    created() {
        this.duct.eventListeners.mturk.on("getHITTypes", {
            success: (data) => {
                this.exstHITTypes = data["HITTypes"];
            },
            error: (data) => {
                this.$refs.snackbar.show("error", `Error in getting HIT types: ${data["Reason"]}`);
            }
        });
        this.duct.eventListeners.mturk.on("listQualifications", {
            success: (data) => {
                let ret = {};
                for(var i in data["QualificationTypes"]) {
                    const id = data["QualificationTypes"][i]["QualificationTypeId"];
                    const name = data["QualificationTypes"][i]["Name"];
                    ret[id] = { name };
                }
                this.customQualTypes = ret;
            }
        });

        this.duct.invokeOrWaitForOpen(() => {
            this.duct.controllers.mturk.getHITTypes();
            this.duct.controllers.mturk.listQualifications(false);
        });
    }
}
</script>
