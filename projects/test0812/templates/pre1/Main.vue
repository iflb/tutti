<template>
    <v-container pa-10>
        This is the first template!<br>
        ... and this is hogedata: {{ nano.data.field1 }}<br>
        ... nad this is fugadata: {{ nano.data.field2 }}<br>

        <v-select v-model="nano.ans.select" :items="selectItems"></v-select>
        <v-btn @click="submit()">next</v-btn>

    </v-container>
</template>

<script>
var ductMixIn = {
    data: () => ({
        nano: {
            data: {},
            ans: {}
        },
    }),
    props: ["nanoData"],
    methods: {
        submit(ans) {
            if(ans) this.$emit("submit", ans);
            else this.$emit("submit", this.nano.ans);

            this.nano.ans = {};
        }
    },
    created() {
        this.nano.data = this.nanoData;
    }
};

export default {
    mixins: [ductMixIn],
    data: () => ({
        selectItems: ["hoge", "fuga", "foo", "bar"],
        hoge: ""
    })
};
</script>
