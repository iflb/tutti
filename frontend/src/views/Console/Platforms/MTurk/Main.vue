<template>
    <v-main class="mt-10 grey lighten-4">
        <div style="max-width:1000px" class="mx-auto">
        <v-row align="center" justify="center" class="my-6">
            <v-col cols="3">
                <v-img src="https://pbs.twimg.com/profile_images/1067838660035280897/XJfH-OpK_400x400.jpg"></v-img>
            </v-col>
            <v-col cols="7">
                <div class="text-h3">Amazon Mechanical Turk</div>
                <v-row class="mt-4">
                    <v-btn class="ma-2" color="green" dark @click="windowOpen('https://worker.mturk.com', '_blank');">Workers</v-btn>
                    <v-btn class="ma-2" color="orange" dark @click="windowOpen('https://requester.mturk.com', '_blank');">Requesters</v-btn>
                </v-row>
                <v-row>
                    <v-btn class="ma-2" color="green" outlined @click="windowOpen('https://workersandbox.mturk.com', '_blank');">Workers sandbox</v-btn>
                    <v-btn class="ma-2" color="orange" outlined @click="windowOpen('https://requestersandbox.mturk.com', '_blank');">Requesters sandbox</v-btn>
                </v-row>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="4">
                <v-card>
                    <v-img src="https://media.istockphoto.com/videos/stack-of-files-documents-being-piled-onto-office-desk-video-id825340524?s=640x640" max-height="150"></v-img>
                    <v-card-title>HITs</v-card-title>
                    <v-card-text>Create, custormize, or remove task batches.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text>Manage HITs</v-btn></v-card-actions>
                </v-card>
            </v-col>
            <v-col cols="4">
                <v-card>
                    <v-img src="https://us.123rf.com/450wm/aniwhite/aniwhite1603/aniwhite160300174/53982937-stock-vector-the-crowd-of-abstract-people-flat-design-vector-illustration-.jpg?ver=6" max-height="150"></v-img>
                    <v-card-title>Workers</v-card-title>
                    <v-card-text>Check workers' status, block or contact workers, or grant qualifications.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text>Manage workers</v-btn></v-card-actions>
                </v-card>
            </v-col>
            <v-col cols="4">
                <v-card>
                    <v-img src="https://www.dw.com/image/48024462_303.jpg" max-height="150"></v-img>
                    <v-card-title>Qualifications</v-card-title>
                    <v-card-text>Create or remove qualifications.</v-card-text>
                    <v-card-actions><v-btn color="indigo lighten-1" text>Manage qualifications</v-btn></v-card-actions>
                </v-card>
            </v-col>
        </v-row>
        </div>
    </v-main>
</template>
<script>
export default {
    methods: {
        windowOpen(url, target){
            window.open(url, target);
        }
    }
}
</script>
