<!-- Your HTML code here -->
<template>   
    <v-container pa-10>
        <v-card width="600" class="mx-auto my-6 pa-6">
            <v-row>
                <v-col cols="12">
                    <header><b>Q.</b> Copy-and-paste your Worker ID.</header>
                </v-col>
                <v-col cols="12">
                    <v-text-field outlined flat v-nano.required v-model="workerId" label="Worker ID" />
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="end">
                <v-btn class="mr-3 mb-3" :disabled="!canSubmit" @click="canSubmit ? submit() : false">next</v-btn>
            </v-row>
        </v-card>
    </v-container>
</template>

<!-- Your JavaScript code here -->
<script>   
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({
        workerId: ""
    })
};
</script>

<!-- Your CSS here -->
<style scoped>   
</style>
