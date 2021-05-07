<template>
    <div>
        <v-card-title>Tutti-Duct Event Logs (Advanced)</v-card-title>

        <v-data-table
            :headers="logTableHeaders"
            :items="logs"
            :items-per-page="10">

            <template v-slot:item.sent="{ item }">
                {{ item.eid }}
                <vue-json-pretty
                    :data="item.sent"
                    :deep="1"
                    style="font-size:0.6em;">
                </vue-json-pretty>
            </template>

            <template v-slot:item.received="{ item }">
                <vue-json-pretty
                    :data="item.received"
                    :deep="2"
                    style="font-size:0.6em;">
                </vue-json-pretty>
            </template>

        </v-data-table>
    </div>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty/lib/vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'

export default {
    components: {
        VueJsonPretty
    },
    data: () => ({
        logTableHeaders: [
            { text: "Request ID", value: "rid" },
            { text: "Sent Message", value: "sent" },
            { text: "Received Message", value: "received" },
        ],
    }),
    props: ["logs"]
}
</script>
