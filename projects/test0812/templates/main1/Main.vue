<template>
    <v-container pa-10>
        <div class="text-h4">Main-1</div>

        <v-card max-width="1000" class="mx-auto my-6 pa-6">
            <v-row align="center">
                <v-col cols="5">
                    <v-card class="pa-3" color="grey lighten-4">
                    <v-img height="300" :src="nano.props.img_url0" contain>

                        <template v-slot:placeholder>
                            <v-row class="fill-height ma-0" align="center" justify="center">
                                <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                            </v-row>
                        </template>

                    </v-img>
                   </v-card>
                </v-col>
                <v-col cols="2" align="center" justify="center"><v-icon x-large>mdi-arrow-left-right-bold</v-icon></v-col>
                <v-col cols="5">
                    <v-card class="pa-3" color="grey lighten-4">
                    <v-img height="300" :src="nano.props.img_url1" contain>
                        <template v-slot:placeholder>
                            <v-row class="fill-height ma-0" align="center" justify="center">
                                <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                            </v-row>
                        </template>
                    </v-img>
                    </v-card>
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="center">
                <v-btn class="ma-3" x-large dark color="green darken-4" @click="nano.ans.choice='Same';  submit()">Same</v-btn>
                <v-btn class="ma-3" x-large dark color="green darken-1" @click="nano.ans.choice='Maybe Same';  submit()">Maybe Same</v-btn>
                <v-btn class="ma-3" x-large dark color="red darken-1"   @click="nano.ans.choice='Maybe Not Same';  submit()">Maybe Not Same</v-btn>
                <v-btn class="ma-3" x-large dark color="red darken-4"   @click="nano.ans.choice='Not Same';  submit()">Not Same</v-btn>
            </v-row>
        </v-card>
    </v-container>
</template>

<script>
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({
        defaultNanoProps: {
            "img_url0": "https://images-na.ssl-images-amazon.com/images/I/61qEl7SAq9L._AC_SL1000_.jpg",
            "img_url1": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQJxhbQz2Oy8Dn8ksxkaXPbzMIvhTaGUBH98P5nQ9zIXlQVV5OnWT1ozp9joA&usqp=CAc"
        }
    })
};
</script>
