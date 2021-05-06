<template>
    <v-main>
        <template-select-toolbar :duct="duct" :prjName="prjName"></template-select-toolbar>

        <response-table :duct="duct"></response-table>
    </v-main>
</template>

<script>
import TemplateSelectToolbar from './TemplateSelectToolbar'
import ResponseTable from './ResponseTable'

export default {
    components: {
        TemplateSelectToolbar,
        ResponseTable
    },
    props: ["duct", "prjName"],
}
</script>
