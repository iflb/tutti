<template>
    <v-card class="mt-5">
        <v-card-title>Create HITs for<span style="color:red;" class="pl-2">{{ prjName }}</span></v-card-title>
        <v-card-text>
            <v-row>
                <v-col cols="2"> <b># of HITs to post:</b> </v-col>
                <v-col cols="2"> <v-text-field outlined dense hide-details type="number" min=0 step=1 v-model.number="numCreateHITs"></v-text-field> </v-col>
            </v-row>
        </v-card-text>
        <v-card-subtitle>
            <b>HIT Params</b>
            <help-button name="CreateHITWithHITType" />
        </v-card-subtitle>
        <v-simple-table dense>
            <template v-slot:default>
                <thead><tr style="background-color:#eee;">
                    <th>Key</th>
                    <th>Value</th>
                </tr></thead>
                <tbody>
                    <tr>
                        <td>MaxAssignments</td>
                        <td>
                            <v-text-field
                                dense
                                hide-details
                                disabled
                                type="number"
                                min=1
                                step=1
                                v-model.number="HITParams.MaxAssignments" />
                        </td>
                    </tr>
                    <tr>
                        <td>LifetimeInSeconds</td>
                        <td>
                            <v-text-field
                                dense
                                hide-details
                                type="number"
                                min=0
                                step=10
                                v-model.number="HITParams.LifetimeInSeconds" />
                        </td>
                    </tr>
                    <tr>
                        <td>RequesterAnnotation</td>
                        <td>
                            <v-text-field
                                dense
                                hide-details
                                v-model="HITParams.RequesterAnnotation" />
                        </td>
                    </tr>
                </tbody>
            </template>
        </v-simple-table>
    </v-card>
</template>

<script>
import HelpButton from './HelpButton'
import { defaultHITParams, defaultNumCreateHITs } from './create-hit-manifest'

export default {
    components: {
        HelpButton
    },
    data: () => ({
        HITParams: defaultHITParams,
        numCreateHITs: defaultNumCreateHITs,
    }),
    props: ["prjName"],
    watch: {
        HITParams: {
            deep: true,
            handler(val) { this.$emit("update", "HITParams", val); }
        },
        numCreateHITs(val) {
            this.$emit("update", "numCreateHITs", val);
        }
    }
}
</script>
