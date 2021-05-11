<template>
    <v-app-bar color="indigo" dark app clipped-left clipped-right dense>
        <v-app-bar-nav-icon @click="$emit('drawer-icon-click');"></v-app-bar-nav-icon>
        
        <v-toolbar-title>Tutti Management Console</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-autocomplete
            hide-details
            cache-items
            solo-inverted
            hide-no-data
            dense
            rounded
            v-model="prjName"
            :items="prjNames"
            label="Select existing project">
        </v-autocomplete>

        <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    fab
                    dark
                    small
                    icon
                    v-on="on"
                    v-bind="attrs"
                    @click="$refs.dialogCreateProject.show()">
                    <v-icon>mdi-plus</v-icon>
                </v-btn>
            </template>
            <span>Create new project...</span>
        </v-tooltip>

        <v-spacer></v-spacer>

        <server-status-menu-button :duct="duct"></server-status-menu-button>

        <v-btn
            icon
            :plain="!eventDrawer"
            @click="$emit('event-nav-icon-click')">
            <v-icon :color="eventDrawer ? 'yellow darken-2' : ''">mdi-lightning-bolt</v-icon>
        </v-btn>

        <tutti-dialog
            ref="dialogCreateProject"
            title="Create New Project"
            maxWidth="400"
            :allowEnter="true"
            :actions="[
                {
                    label: 'Create',
                    color: 'indigo darken-1',
                    disableByRule: true,
                    text: true,
                    onclick: createProject
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
                    v-model="newPrjName"
                    filled
                    prepend-icon="mdi-pencil"
                    label="Enter Project Name"
                    :rules="[rules.required, rules.alphanumeric]">
                </v-text-field>
            </template>
        </tutti-dialog>

    </v-app-bar>
</template>

<script>
import rules from '@/lib/input-rules'
import TuttiDialog from '@/views/assets/Dialog'
import ServerStatusMenuButton from './ConsoleServerStatusMenuButton'

export default {
    components: {
        TuttiDialog,
        ServerStatusMenuButton
    },
    data: () => ({
        rules,

        prjNames: [],
        prjName: "",
        newPrjName: "",
    }),
    props: ["duct", "eventDrawer"],
    methods: {
        createProject() { this.duct.controllers.resource.createProject(this.newPrjName); },
    },
    watch: {
        prjName(val) {
            this.$emit("project-name-update", val);
        }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("createProject", {
                success: (data) => {
                    this.$refs.snackbarSuccess.show(`Successfully created project '${data["ProjectName"]}'`);
                    this.duct.controllers.resource.listProjects();
                }
            });
            this.duct.eventListeners.resource.on("listProjects", {
                success: (data) => {
                    this.prjNames = data["Projects"].map((value) => (value.name));
                    this.prjName = localStorage.getItem("tuttiProject") || null;
                }
            });

            this.duct.controllers.resource.listProjects();
        });
    }
}
</script>
