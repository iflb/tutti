<template>
    <div>
        <v-card-title>
            Responses
            <v-spacer></v-spacer>
            <v-text-field
                v-model="searchStr"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details>
            </v-text-field>
        </v-card-title>

        <v-data-table
            :headers="table.headers"
            :items="table.rows"
            :items-per-page="50"
            :footer-props="{ itemsPerPageOptions: [10,30,50,100,300] }"
            :search="searchStr">

            <template v-slot:item.Answers="{ item }">
                <v-simple-table dense>
                    <template v-slot:default>
                        <tbody>
                            <tr v-for="(value, key) in item.Answers" :key="key">
                                <td style="width:100px"><b>{{ key }}</b></td>
                                <td style="word-break:break-all">{{ value }}</td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </template>

        </v-data-table>
    </div>
</template>

<script>
import { stringifyUnixTime } from '@/lib/utils'

export default {
    data: () => ({
        searchStr: "",
        table: {
            headers: [
                { text: "Session ID", value: "WorkSessionId" },
                { text: "Worker ID", value: "WorkerId" },
                { text: "Nanotask ID", value: "NanotaskId" },
                { text: "Submitted time", value: "Timestamp" },
                { text: "Answers", value: "Answers" },
            ],
            rows: []
        }
    }),
    props: ["duct"],
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("getResponsesForTemplate", {
                success: (data) => {
                     this.table.rows = data["Responses"].map(
                        (row) => (
                            Object.assign(row, {
                                Timestamp: stringifyUnixTime( row.Timestamp ) || ""
                            })
                        )
                    );
                }
            });
        });
    }
}
</script>
