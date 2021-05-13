<template>
    <v-sheet max-width="1000" color="transparent" class="mx-auto">
        <v-row>
            <v-col cols="4" v-for="card in cards" :key="card.to">
                <v-card>
                    <v-img :src="card.imgSrc" height="120"></v-img>
                    <v-card-title>{{ card.title }}</v-card-title>
                    <v-card-text>{{ card.text }}</v-card-text>
                    <v-card-actions>
                        <v-btn color="indigo lighten-1" text :to="card.to">{{ card.actionLabel }}</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-sheet>
</template>

<script>
export default {
    data: () => ({
        cards: [
            {
                imgSrc: "https://media.istockphoto.com/videos/stack-of-files-documents-being-piled-onto-office-desk-video-id825340524?s=640x640",
                title: "HITs",
                text: "Create, customize, or remove task batches.",
                actionLabel: "Manage HITs",
                to: "hit"
            },
            {
                imgSrc: "https://us.123rf.com/450wm/aniwhite/aniwhite1603/aniwhite160300174/53982937-stock-vector-the-crowd-of-abstract-people-flat-design-vector-illustration-.jpg?ver=6",
                title: "Workers",
                text: "Check workers' status, block or contact workers, or grant qualifications.",
                actionLabel: "Manage workers",
                to: "worker"
            },
            {
                imgSrc: "https://assets.st-note.com/production/uploads/images/30971758/rectangle_large_type_2_d321a7db4258595199bc6a264e7b320b.jpg?fit=bounds&format=jpeg&quality=45&width=960",
                title: "Qualifications",
                text: "Create or remove qualifications.",
                actionLabel: "Manage qualifications",
                to: "qual"
            },
            {
                imgSrc: "https://jopus.net/wp-content/uploads/2018/10/shutterstock_1065989561.jpg",
                title: "Assignments",
                text: "See and approve/deny assignments.",
                actionLabel: "Manage assignments",
                to: "assignment"
            },
        ]
    })
}
</script>
