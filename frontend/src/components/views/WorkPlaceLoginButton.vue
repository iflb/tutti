<template>
    <div class="text-right ma-6">
        <v-menu
            offset-y
            v-if="showWorkerMenu && platformWorkerId">
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    text
                    color="indigo"
                    class="text-none"
                    v-bind="attrs"
                    v-on="on">
                    Worker ID: {{ platformWorkerId }}
                </v-btn>
            </template>
            <v-list>
                <v-list-item
                    key="logout"
                    @click="$refs.dialog.show()">
                    <v-list-item-title>Log out</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
        <v-btn
            v-if="showWorkerMenu && !platformWorkerId"
            dark
            color="indigo"
            :href="`../workplace-login?project=${prjName}`">
            Log in
        </v-btn>

        <tutti-dialog ref="dialog" title="Are you sure to log out?" maxWidth="500"
            :actions="[
                { label: 'Logout', color: 'indigo darken-1', text: true, onclick: logout },
                { label: 'Cancel', color: 'grey darken-1', text: true }
            ]">
            <template v-slot:body>
                Some of your working history may not be saved.
            </template>
        </tutti-dialog>
    </div>
</template>

<script>
import TuttiDialog from '@/components/ui/TuttiDialog'
export default {
    components: {
        TuttiDialog
    },
    props: ["prjName", "showWorkerMenu", "platformWorkerId"],
    methods: {
        logout() {
            localStorage.removeItem("tuttiPlatformWorkerId");
            //this.platformWorkerId = "";
            window.location.reload();
        },
    }
}
</script>
