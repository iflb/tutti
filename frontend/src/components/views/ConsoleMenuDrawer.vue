<template>
    <v-navigation-drawer v-model="drawer" app clipped left>
        <v-list nav dense>
            <v-list-item-group active-class="indigo--text text--accent-4">

                <v-list-item to="/console/dashboard/">
                    <v-list-item-icon> <v-icon>mdi-view-dashboard</v-icon> </v-list-item-icon>
                    <v-list-item-title>Dashboard</v-list-item-title>
                </v-list-item>

            </v-list-item-group>

            <v-list-item-group active-class="indigo--text text--accent-4">
                <v-subheader>DESIGN & TEST</v-subheader>

                <v-list-item to="/console/template/">
                    <v-list-item-icon> <v-icon>mdi-iframe-outline</v-icon> </v-list-item-icon>
                    <v-list-item-title>Templates</v-list-item-title>
                </v-list-item>
           
                <v-list-item to="/console/flow/">
                    <v-list-item-icon> <v-icon>mdi-wrench</v-icon> </v-list-item-icon>
                    <v-list-item-title>Scheme</v-list-item-title>
                </v-list-item>

            </v-list-item-group>

            <v-list-item-group active-class="indigo--text text--accent-4">
                <v-subheader>PUBLISH & COLLECT</v-subheader>
 
                <v-list-item to="/console/response/">
                    <v-list-item-icon> <v-icon>mdi-comment-check-outline</v-icon> </v-list-item-icon>
                    <v-list-item-title>Responses</v-list-item-title>
                </v-list-item>

                <v-list-group prepend-icon="mdi-account-group" :value="false">
                    <template v-slot:activator> <v-list-item-title>Worker Platforms</v-list-item-title> </template>

                    <v-list-item class="pl-6" to="/console/platform/tutti-market/">
                        <v-list-item-icon> <v-icon>mdi-music</v-icon> </v-list-item-icon>
                        <v-list-item-title>Tutti Market</v-list-item-title>
                    </v-list-item>

                    <v-list-item class="pl-6" to="/console/platform/mturk/">
                        <v-list-item-icon> <v-icon>mdi-amazon</v-icon> </v-list-item-icon>
                        <v-list-item-title>Amazon MTurk</v-list-item-title>
                    </v-list-item>

                </v-list-group>

            </v-list-item-group>

            <v-list-item-group active-class="indigo--text text--accent-4">
                <v-subheader>OTHERS</v-subheader>

                <v-list-item to="/console/event/">
                    <v-list-item-icon> <v-icon>mdi-lightning-bolt</v-icon> </v-list-item-icon>
                    <v-list-item-title>Duct Events</v-list-item-title>
                </v-list-item>

                <v-list-item href="https://iflb.github.io/tutti/" target="_blank">
                    <v-list-item-icon> <v-icon>mdi-file-document-outline</v-icon> </v-list-item-icon>
                    <v-list-item-title>Documentation</v-list-item-title>
                    <v-list-item-action> <v-icon small>mdi-launch</v-icon> </v-list-item-action>
                </v-list-item>

            </v-list-item-group>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
export default {
    props: ["drawer"]
}
</script>
