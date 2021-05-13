<template>
    <v-card class="mt-10">
        <v-card-title>
            Task Flow
        </v-card-title>
        <v-container>
            <v-row>
                <v-col align="right">
                </v-col>
            </v-row>

            <v-card
                align="center"
                class="mx-auto py-2 text-h6"
                color="grey lighten-2"
                width="200">
                Start
            </v-card>

            <arrow :color="templateColor" depth="1" />

            <div v-if="flow">
                <recursive-batch
                    :duct="duct"
                    :parent-params="{
                        prjName, templateColor,
                        node: flow,
                        depth: 1,
                        isLast: true,
                    }" />
            </div>

            <arrow :color="templateColor" depth="1" />

            <v-card
                align="center"
                class="mx-auto py-2 text-h6"
                color="grey lighten-2"
                width="200">
                End
            </v-card>
        </v-container>
    </v-card>
</template>

<script>
import RecursiveBatch from './RecursiveBatch'
import Arrow from './Arrow'

export default {
    components: {
        RecursiveBatch,
        Arrow,
    },
    props: ["duct", "prjName", "flow", "templateColor"],
}
</script>
