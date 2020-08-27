<template>
    <v-hover v-slot:default="{ hover }" open-delay="300" style="cursor:pointer;">
        <v-sheet :width="width" class="text-center mx-auto py-2" color="rgba(0,0,0,0)">
            <v-icon x-large>mdi-arrow-down-bold</v-icon>
            <div v-if="hover">
            <v-card class="mx-auto py-5" outlined><v-icon>mdi-plus-box</v-icon></v-card>
            <v-icon x-large>mdi-arrow-down-bold</v-icon>
            </div>
        </v-sheet>
    </v-hover>
</template>

<script>
export default {
    data: () => ({
        width: 300
    })
}
</script>
