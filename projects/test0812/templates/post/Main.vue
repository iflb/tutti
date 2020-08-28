<template>
    <v-container pa-10>
        <div class="text-h4">Post</div>

        <v-card width="600" class="mx-auto my-6 pa-6">
            <v-row>
                <v-col cols="12"><header><b>Post-survey.</b> Thank you for your contribution in our task! Please let us know a few things to help us improve this task.</header></v-col>
                <v-col cols="12"><header><b>Q1.</b> How did you enjoy the task?</header></v-col>
                <v-col cols="12">
                    <v-slider v-model="nano.ans.enjoyment" :tick-labels="enjoyment" :max="3" step="1" ticks="always" tick-size="4" ></v-slider>
                </v-col>
                <v-col cols="12"><header><b>Q2.</b> Describe anything you think is needed for improvement.</header></v-col>
                <v-col cols="12">
                <v-textarea v-model="nano.ans.comment" outlined></v-textarea>
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="end"><v-btn class="mr-3 mb-3" @click="submit()">Finish</v-btn></v-row>
        </v-card>


    </v-container>
</template>

<script>
import ductMixIn from "@/mixins/duct";
export default {
    mixins: [ductMixIn],
    data: () => ({
        enjoyment: ["Never", "Slightly", "Moderately", "Definitely"]
    })
};
</script>
