<template>
    <v-container pa-10>
        <v-text-field v-model="nano.textinput"></v-text-field>
        <v-textarea v-model="nano.textarea" rows="3"></v-textarea>

        <v-checkbox v-model="nano.checkbox" label="Orange" value="orange"></v-checkbox>
        <v-checkbox v-model="nano.checkbox" label="Apple" value="apple"></v-checkbox>
        <v-checkbox v-model="nano.checkbox" label="Pineapple" value="pineapple"></v-checkbox>
        <v-checkbox v-model="nano.checkbox" label="Grape" value="grape"></v-checkbox>

        <v-radio-group v-model="nano.radio">
            <v-radio label="A" value="A">Option A</v-radio>
            <v-radio label="B" value="B">Option B</v-radio>
            <v-radio label="C" value="C">Option C</v-radio>
        </v-radio-group>

        <v-btn @click="setAnswerValue('button', 'primary')" color="primary">button1</v-btn>
        <v-btn @click="setAnswerValue('button', 'secondary')" color="error">button2</v-btn>
        <v-btn @click="setAnswerValue('button', 'success')">button3</v-btn>

        <v-select v-model="nano.select" :items="selectItems" label="Select"></v-select>
    </v-container>
</template>

<script>
export default {
    data: () => ({
        nano: {},
        selectItems: ["select 1", "select 2"]
    }),
    methods: {
        setAnswerValue(key,val) {
            this.$set(this.nano, key, val);
        },
        updateAnswer() {
            this.$store.dispatch("updateAnswer", this.nano);
        }
    },
    watch: {
        nano: {
            handler: function(){
                this.updateAnswer();
            },
            deep: true
        }
    }
};
</script>

<style scoped>
</style>
