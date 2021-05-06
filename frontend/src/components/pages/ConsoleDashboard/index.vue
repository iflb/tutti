<template>
    <v-main class="mt-10 grey lighten-4">
        <v-row justify="center">
            <v-col cols="9">
                <task-ui-urls-card :prjName="prjName" :duct="duct"></task-ui-urls-card>
            </v-col>
        </v-row>
    </v-main>
</template>
<script>
import TaskUIURLsCard from "./TaskUIURLsCard" 
export default {
    components: {
        "task-ui-urls-card": TaskUIURLsCard
    },
    props: [ "prjName", "duct" ],
}
</script>
