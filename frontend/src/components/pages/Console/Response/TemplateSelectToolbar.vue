<template>
    <v-toolbar class="grey lighten-4">
        <v-row justify="center" align="end">
            <v-col cols="8">
                <v-select
                    width="80%"
                    hide-details
                    :items="tmplNames"
                    v-model="tmplName"
                    label="Template name"
                    :disabled="tmplNames.length==0">
                </v-select>
            </v-col>
        </v-row>
    </v-toolbar>
</template>

<script>
export default {
    data: () => ({
        tmplNames: [],
        tmplName: null,
    }),
    props: ["duct", "prjName"],
    methods: {
        listTemplates() {
            this.tmplName = null;
            this.duct.controllers.resource.listTemplates(this.prjName);
        }
    },
    watch: {
        prjName(val) { if(val) this.listTemplates(); },
        tmplName() { this.duct.controllers.resource.getResponsesForTemplate(this.prjName, this.tmplName); }
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("listTemplates", {
                success: (data) => {
                    this.tmplNames = data["Templates"];
                }
            });
        })
    }
}
</script>
