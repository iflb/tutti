<template>
    <v-dialog v-model="shown" persistent max-width="700">
        <v-card>
            <v-card-title class="text-h6"><v-icon class="mr-2" color="green">mdi-check-circle</v-icon>Answers are submitted successfully</v-card-title>
            <v-card-text><vue-json-pretty :data="answer"></vue-json-pretty></v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="shown=false">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty/lib/vue-json-pretty'

export default {
    data: () => ({
        shown: false,
    }),
    components: { VueJsonPretty },
    props: ["answer"]
}
</script>
