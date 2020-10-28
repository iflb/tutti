<template>
    <v-row style="width:100%" class="text-center">
        <v-col cols="12">This is a default template</v-col>
        <v-col><v-btn cols="12" @click="submit()">Submit</v-btn></v-col>
    </v-row>
</template>
<script>
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({
    })
};
</script>
