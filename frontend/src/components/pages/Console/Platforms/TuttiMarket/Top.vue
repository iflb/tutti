<template>
    <div>
        <v-row justify="center" class="mt-6">
            <v-col cols="10">
                <v-card>
                    <v-card-title>
                        Tutti Market
                    </v-card-title>
                    <div v-for="item in menuItems" :key="item.title">
                        <v-divider />
                        <v-card-text class="d-flex">
                            <div class="text-body-1">
                                {{ item.title }}
                            </div>
                            <v-spacer />
                            <v-btn>
                                Go
                            </v-btn>
                        </v-card-text>
                    </div>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>
<script>
export default {
    data: () => ({
        menuItems: [
            { title: 'Jobs' },
            { title: 'Spots' },
        ]
    })
}
</script>
