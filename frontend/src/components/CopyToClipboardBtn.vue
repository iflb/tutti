<template>
    <v-tooltip :value="tooltip" :open-on-hover="false" v-on:change="onchanged" bottom>
        <template v-slot:activator="{ on, attrs }">
            <v-btn v-bind="attrs" v-on="on" icon @click="click">
                <v-icon>mdi-content-copy</v-icon>
            </v-btn>
        </template>
        <span>Copied!</span>
    </v-tooltip>
</template>
<script>
export default {
    data: () => ({
        tooltip: false,
        timeout: null,
    }),
    props: ["text"],
    methods: {
        click() {
            this.copyText();
            this.tooltip = true;
            if(this.timeout) clearTimeout(this.timeout);
            this.timeout = setTimeout(()=>{
                this.tooltip = false;
                this.timeout = null;
            },2000);
        },
        copyText() {
            navigator.clipboard.writeText(this.text);
        },
        onchanged(e) {
            console.log("onchanged", e);
        }
    }
}
</script>
