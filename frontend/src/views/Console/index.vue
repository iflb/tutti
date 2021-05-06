<template>
    <v-app>
        <app-bar
            :duct="duct"
            :eventDrawer="eventDrawer"
            @drawer-icon-click="toggleMenuDrawer"
            @event-nav-icon-click="toggleEventDrawer"
            @project-name-update="updateProjectName">
        </app-bar>

        <menu-drawer :drawer="menuDrawer"></menu-drawer>

        <event-drawer :duct="duct" :drawer="eventDrawer"></event-drawer>

        <keep-alive>
            <router-view app
                v-if="duct"
                :duct="duct"
                :prjName="prjName"
                ref="child"
            ></router-view>
        </keep-alive>


        <tutti-snackbar color="success" :timeout="5000" ref="snackbarSuccess" />
        
    </v-app>
</template>

<script>
import tutti from '@iflb/tutti'
import AppBar from './AppBar'
import MenuDrawer from './MenuDrawer'
import EventDrawer from './EventDrawer'

export default {
    components: { 
        AppBar,
        MenuDrawer,
        EventDrawer,
        TuttiSnackbar: () => import('@/views/assets/Snackbar'),
    },
    data: () => ({
        duct: null,
        wsdPath: "/ducts/wsd",
        menuDrawer: true,
        eventDrawer: true,
        prjName: "",
    }),
    methods: {
        updateProjectName(name) {
            this.prjName = name;
            if(name){
                localStorage.setItem("tuttiProject", name);
            }
        },
        toggleMenuDrawer() { this.menuDrawer = !this.menuDrawer; },
        toggleEventDrawer() { this.eventDrawer = !this.eventDrawer; },
    },

    created: function(){
        this.duct = new tutti.Duct();
        this.duct.logger = new tutti.DuctEventLogger(this.duct);
        this.duct.open(this.wsdPath);
    }
}
</script>
<style>
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.5s;
  transition-property: opacity;
  transition-timing-function: ease-in;
}

.fade-enter-active {
  transition-duration: 0.5s;
}

.fade-enter,
.fade-leave-active {
  opacity: 0
}

.vjs-tree {
    font-size: 10px;
}
</style>
