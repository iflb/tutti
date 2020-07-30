<template>
    <v-app>
        <!--<router-view :to=`${projectName}` :duct="duct"></router-view>-->
        <v-btn @click="getNextState">get next state</v-btn>
    </v-app>
</template>

<script>
export default {
    data: () => ({
        duct: null,
        sessionId: null
    }),
    props: ["projectName"],
    methods: {
        initDucts(ducts) {
            ducts.user = 'guest';
            ducts.context_url = '/ducts';
            ducts.libs_plugin = [ducts.context_url + '/libs/libcrowd.js'];
            ducts.main = this.main;
                                                
            let lib_script = document.createElement('script');
            lib_script.src = ducts.context_url+'/libs/main.js';
            document.body.appendChild(lib_script);
        },
        main(wsd){
            this.duct = new window.ducts.dynamiccrowd.Duct(wsd);

            this.duct.catchall_event_handler = (rid, eid) => {console.log('on_message eid='+eid)};
            this.duct.uncaught_event_handler = (rid, eid) => {console.log('uncaught_message eid='+eid)};
            this.duct.event_error_handler = (rid, eid, data, error) => {console.error(error);};

            this.duct.setEventHandler(this.duct.EVENT.NANOTASK_SESSION_MANAGER, (rid, eid, data) => {
                console.log(data["Command"], data["Status"])
                if(data["Status"]==="error") console.log(data["Reason"])
                else {
                    switch(data["Command"]){
                        case "REGISTER_SM":
                            break
                        case "CREATE_SESSION":
                            this.sessionId = data["SessionId"]
                            console.log(this.sessionId)
                            break
                        case "GET":
                            console.log(data["NextStatus"])
                            break
                    }
                }
            })

            this.openDuct().then(() => {
                this.duct.send(this.duct.next_rid(), this.duct.EVENT.NANOTASK_SESSION_MANAGER, ["REGISTER_SM", "fugapro"])
                this.duct.send(this.duct.next_rid(), this.duct.EVENT.NANOTASK_SESSION_MANAGER, ["CREATE_SESSION", "fugapro"])
            })
        },
        openDuct(){
            return new Promise((resolve, reject) => {
                this.duct.open().then(() => {
                    //if(this.$refs.child.onDuctOpen) this.$refs.child.onDuctOpen();
                    resolve();
                }).catch(reject);
            })
        },
        closeDuct(){
            this.duct.close()
            //if(this.$refs.child.onDuctClose) this.$refs.child.onDuctClose();
        },
        getNextState(){
            if(this.sessionId) this.duct.send(this.duct.next_rid(), this.duct.EVENT.NANOTASK_SESSION_MANAGER, ["GET", this.sessionId])
        }
    },
    created: function(){
        this.initDucts( window.ducts = window.ducts || {})
    }
}
</script>
