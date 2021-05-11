<template>
    <div>
        <v-row justify="center">
            <v-col cols="9">
                <v-card v-if="crd">
                    <v-card-text>
                        Access Key ID: {{ crd.AccessKeyId }}<br>
                        Secret Access Key: {{ crd.SecretAccessKey }}<br>
                        Balance: ${{ crd.AccountBalance.AvailableBalance }}
                        <span v-if="'OnHoldBalance' in crd.AccountBalance">
                            (on hold: {{ crd.AccountBalance.OnHoldBalance }})
                        </span>
                    </v-card-text>

                    <v-card-text class="pt-0">
                        <v-btn
                            outlined
                            class="ml-3"
                            color="grey"
                            @click="clearCredentials()">
                            Clear credentials
                        </v-btn>
                    </v-card-text>
                </v-card>

                <v-card v-else>
                    <v-card-text>
                        MTurk account is not set. 
                        <v-btn
                            text
                            color="indigo"
                            @click="$refs.dialog.show()">
                        Set credentials
                    </v-btn>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <tutti-dialog
            ref="dialog"
            title="Set MTurk Credentials"
            maxWidth="600"
            :actions="[
                {
                    label: 'Set account',
                    color: 'indigo darken-1',
                    dark: true,
                    onclick: setCredentials
                },
                {
                    label: 'Cancel',
                    color: 'grey darken-1',
                    text: true
                }
            ]" >
            <template v-slot:body>
                <v-text-field
                    autofocus
                    filled
                    v-model="newCredentials.AccessKeyId"
                    label="Access Key Id">
                </v-text-field>
                <v-text-field
                    filled
                    v-model="newCredentials.SecretAccessKey"
                    label="Secret Access Key">
                </v-text-field>
            </template>
        </tutti-dialog>
    </div>
</template>

<script>
import TuttiDialog from '@/views/assets/Dialog'

export default {
    components: {
        TuttiDialog
    },
    data: () => ({
        newCredentials: {
            AccessKeyId: "",
            SecretAccessKey: ""
        }
    }),
    props: ["duct", "crd"],
    methods: {
        setCredentials() {
            this.duct.controllers.mturk.setCredentials(
                this.newCredentials.AccessKeyId,
                this.newCredentials.SecretAccessKey
            );
        },
        clearCredentials() {
            this.duct.controllers.mturk.clearCredentials();
        }
    }
}
</script>
