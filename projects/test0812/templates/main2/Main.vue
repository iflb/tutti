<template>
    <v-container pa-10>
        <div class="text-h4">Main-2</div>
        <v-card width="600" class="mx-auto my-6 pa-6">
            <v-row>
                <v-col cols="12"><header><b>Q.</b> What did you just see in the right card?</header></v-col>
                <v-col cols="12"><v-text-field outlined flat v-model="nano.ans.description" label="I saw ..." /></v-col>
            </v-row>
            <v-row class="d-flex" justify="end"><v-btn class="mr-3 mb-3" @click="submit()">next</v-btn></v-row>
        </v-card>

    </v-container>
</template>

<script>
import ductMixIn from "@/mixins/duct";
export default {
    mixins: [ductMixIn],
};
</script>
