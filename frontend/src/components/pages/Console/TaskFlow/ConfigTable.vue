<template>
    <v-card class="mt-1">
        <v-card-title> Config Parameters </v-card-title>
        <v-data-table
            dense
            hide-default-footer
            :headers="[
                { width: '40%', text: 'Property', value: 'key' },
                { width: '60%', text: 'Value', value: 'val' }
            ]"
            :items="configItems"
            :items-per-page="100"
        >
            <template v-slot:item.val="{ item }">
                <v-icon
                    v-if="item.val===true"
                    color="success">
                    mdi-check-circle-outline
                </v-icon>

                <v-icon
                    v-else-if="item.val===false"
                    color="error">
                    mdi-cancel
                </v-icon>

                <b v-else>{{ item.val }}</b>
            </template>
        </v-data-table>
    </v-card>
</template>

<script>
export default {
    props: ["config"],
    computed: {
        configItems() {
            if(!this.config) return [];
            let arr = [];
            for(const [key,val] of Object.entries(this.config)){
                arr.push({ key, val });
            }
            return arr;
        }
    }
}
</script>
