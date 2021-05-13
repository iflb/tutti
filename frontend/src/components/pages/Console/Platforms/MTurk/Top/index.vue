<template>
    <div>
        <v-row align="center" justify="center" class="my-6">
            <v-col cols="2" class="text-center">
                <v-img
                    contain
                    :max-height="200"
                    src="https://pbs.twimg.com/profile_images/1067838660035280897/XJfH-OpK_400x400.jpg">
                </v-img>
            </v-col>

            <v-col cols="5">
                <div class="text-h3">Amazon Mechanical Turk</div>
                <v-row class="mt-4">
                    <v-btn
                        outlined
                        class="ma-2"
                        color="indigo"
                        :href="workerSiteUrl"
                        target="_blank">
                        <v-icon>mdi-account-group</v-icon>Workers
                    </v-btn>
                    <v-btn
                        outlined
                        class="ma-2"
                        color="indigo"
                        :href="requesterSiteUrl"
                        target="_blank">
                        <v-icon>mdi-account-circle</v-icon>Requesters
                    </v-btn>
                </v-row>
            </v-col>

        </v-row>

        <credentials-card :duct="duct" :crd="credentials"></credentials-card>

        <page-cards></page-cards>

    </div>
</template>
<script>
import PageCards from './TopPageCards'
import CredentialsCard from './TopCredentialsCard'

export default {
    components: {
        PageCards,
        CredentialsCard,
    },
    props: ["duct", "credentials"],
    computed: {
        workerSiteUrl() {
            if(this.credentials && this.credentials.Sandbox)
                return 'https://workersandbox.mturk.com';
            else
                return 'https://worker.mturk.com';
        },
        requesterSiteUrl() {
            if(this.credentials && this.credentials.Sandbox)
                return 'https://requestersandbox.mturk.com';
            else
                return 'https://requester.mturk.com';
        }
    }
}
</script>
