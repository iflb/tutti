<template>
    <v-app>
        <router-view></router-view>
    </v-app>
</template>

<script>
export default {
    data: () => ({
        duct: null,
        childEventHandlers: {}
    }),
    methods: {
        init() {
        },
        main(wsd){
            this.duct = new window.ducts.dynamiccrowd.Duct(wsd);

            this.duct.catchall_event_handler = (rid, eid) => {console.log('on_message eid='+eid)};
            this.duct.uncaught_event_handler = (rid, eid) => {console.log('uncaught_message eid='+eid)};
            this.duct.event_error_handler = (rid, eid, data, error) => {console.error(error);};

            this.openDuct().then(() => {
            })
        },
        initDucts(ducts) {
            ducts.user = 'guest';
            ducts.context_url = '/ducts';
            ducts.libs_plugin = [ducts.context_url + '/libs/libcrowd.js'];
            ducts.main = this.main;
                                                
            let lib_script = document.createElement('script');
            lib_script.src = ducts.context_url+'/libs/main.js';
            document.body.appendChild(lib_script);
        },
        openDuct(){
            return new Promise((resolve, reject) => {
                this.duct.open().then(() => {
                    if(this.$refs.child.onDuctOpen) this.$refs.child.onDuctOpen();
                    resolve();
                }).catch(reject);
            })
        },
        closeDuct(){
            this.duct.close()
            if(this.$refs.child.onDuctClose) this.$refs.child.onDuctClose();
        }
    },
    created: function(){
        this.init()
        this.initDucts( window.ducts = window.ducts || {})
    }
}
</script>
