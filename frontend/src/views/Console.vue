<template>
    <v-app>
        <v-app-bar color="indigo" dark app clipped-left>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
            
            <v-toolbar-title>DynamicCrowd Management Console</v-toolbar-title>
        </v-app-bar>

        <v-navigation-drawer v-model="drawer" app clipped>
            <v-list nav>
                <v-list-item-group active-class="indigo--text text--accent-4">
                    <v-list-item>
                        <v-list-item-content>
                            <v-list-item-title class="title">DynamicCrowd</v-list-item-title>
                            <v-list-item-subtitle>Beta Version</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item to="/console/dashboard/">
                        <v-list-item-icon>
                            <v-icon>mdi-home</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Home</v-list-item-title>
                    </v-list-item>
                    
                    <v-list-item to="/console/tester/">
                        <v-list-item-icon>
                            <v-icon>mdi-iframe-braces-outline</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Nanotask Tester</v-list-item-title>
                    </v-list-item>

                    <v-list-item to="/console/events/">
                        <v-list-item-icon>
                            <v-icon>mdi-puzzle</v-icon>
                        </v-list-item-icon>
                        <v-list-item-title>Event Handlers</v-list-item-title>
                    </v-list-item>
                
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>

        <v-sheet><router-view></router-view></v-sheet>
        
    </v-app>
</template>

<script>
export default {
    data: () => ({
        drawer: true,
    }),
    created: function(){
        this.$store.dispatch("connectDuctsWebSocket")
    },
}
</script>
