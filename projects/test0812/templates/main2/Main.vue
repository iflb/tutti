<template>
    <v-container pa-10>
        <div class="text-h4">Survey Sample</div>

        <v-card width="600" class="mx-auto my-6 pa-6">
            <v-row>
                <v-col cols="12"><header><b>Pre-survey.</b> Please answer the following questions first.</header></v-col>
                <v-col cols="12"><header><b>Q1.</b> Which is the fruit you like the most?</header></v-col>
                <v-col cols="12"><v-select solo v-model="nano.ans.fruit" :items="fruits" label="Select one"></v-select></v-col>
                <v-col cols="12"><header><b>Q2.</b> Select all your hobbies that apply.</header></v-col>
                <v-checkbox v-model="nano.ans.hobbies" value="Sport" class="mx-2" label="Sport"/>
                <v-checkbox v-model="nano.ans.hobbies" value="Bookreading" class="mx-2" label="Bookreading"/>
                <v-checkbox v-model="nano.ans.hobbies" value="Traveling" class="mx-2" label="Traveling"/>
                <v-checkbox v-model="nano.ans.hobbies" value="Music" class="mx-2" label="Music"/>
                <v-col cols="12"><header><b>Q3.</b> Select one that describes your personality the best.</header></v-col>
                <v-col cols="12">
                <v-radio-group v-model="nano.ans.personality" row>
                    <v-radio label="Inspector" value="Inspector"/>
                    <v-radio label="Performer" value="Performer"/>
                    <v-radio label="Counselor" value="Counselor"/>
                    <v-radio label="Giver" value="Giver"/>
                </v-radio-group>
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="end"><v-btn class="mr-3 mb-3" @click="submit()">next</v-btn></v-row>
        </v-card>


    </v-container>
</template>

<script>
import ductMixIn from "@/mixins/duct";
export default {
    mixins: [ductMixIn],
    data: () => ({
        fruits: ["Banana", "Apple", "Grapes", "Orange", "Watermelon"],
    }),
    mounted() {
        this.$set(this.nano.ans, "hobbies", []);
    }
};
</script>
