<template>
    <v-container pa-10>
        This is the first template!

        <v-select v-model="ans.select" :items="selectItems"></v-select>

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
