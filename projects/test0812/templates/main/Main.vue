<template>
    <v-container pa-10>
        This is the main template!

        <v-textarea v-model="ans.textarea" rows="3"></v-textarea>
        <v-radio-group v-model="ans.radio">
            <v-radio label="A" value="A">Option A</v-radio>
            <v-radio label="B" value="B">Option B</v-radio>
            <v-radio label="C" value="C">Option C</v-radio>
        </v-radio-group>

        <v-btn @click="submit()">next</v-btn>

    </v-container>
</template>

<script>
export default {
    data: () => ({
        // planned to be provided as mixin, etc.
        ans: {},

        selectItems: ["hoge", "fuga", "foo", "bar"]
    }),
    methods: {
        // planned to be provided as mixin, etc.
        submit(ans) {
            if(ans) this.$emit("submit", ans);
            else this.$emit("submit", this.ans);

            this.ans = {};
        }
    }
};
</script>
