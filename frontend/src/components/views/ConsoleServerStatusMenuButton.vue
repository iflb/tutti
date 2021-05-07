<template>
    <v-menu offset-y v-if="profile">
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                depressed
                :color="profile[status].btn.color"
                class="text-none"
                v-bind="attrs"
                v-on="on">
                {{ profile[status].btn.label }}
                <span v-if="status == 'connected'"
                    class="text-caption ml-2">
                    (last pinged: {{ lastPinged }})
                </span>
                <span v-else-if="status == 'disconnected'"
                    class="text-caption ml-2">
                    (Auto-retry remaining: {{ retry.maxCnt-retry.cnt }})
                </span>
            </v-btn>
        </template>
        <v-list>
            <v-list-item
                v-for="(menu, index) in profile[status].btn.menu"
                :key="index"
                @click="menu.handler()">
                <v-list-item-title>{{ menu.title }}</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</template>
<script>
import dateFormat from 'dateformat'

export default {
    data: () => ({
        status: "connecting",
        lastPinged: "",
        retry: {
            enabled: true,
            cnt: 0,
            maxCnt: 5,
            interval: null
        },
    }),
    props: ["duct"],
    methods: {
        reconnect() {
            console.log("trying to reconnect");
            this.initDuct();
            if(this.duct){
                try {
                    this.duct.reconnect().then(() => {
                        this.retry.enabled = true;
                        this.status = "connected";
                        this.retry.cnt = 0;
                    }).catch(() => { 
                        if(++this.retry.cnt>=this.retry.maxCnt) {
                            console.error("failed reconnection 5 times");
                            clearInterval(this.retry.interval);
                            this.retry.interval = null;
                        }
                    });
                } catch (e) {
                    console.log(e);
                }
            } else {
                if(++this.retry.cnt>=this.retry.maxCnt) {
                    console.error("failed reconnection 5 times");
                    clearInterval(this.retry.interval);
                    this.retry.interval = null;
                }
            }
        },
        disconnect() {
            this.retry.enabled = false;
            this.duct.close();
        }
    },
    created() {
        this.profile = {
            connected: {
                btn: {
                    color: "success",
                    label: "Connected to server",
                    menu: [ { title: "Disconnect", handler: this.disconnect } ]
                }
            },
            connecting: {
                btn: {
                    color: "warning",
                    label: "Connecting to server..."
                }
            },
            disconnected: {
                btn: {
                    color: "error",
                    label: "No connection to server",
                    menu: [ { title: "Connect", handler: this.reconnect } ]
                }
            }
        }

        this.retry.interval = setInterval(() => {
            if(this.status=="disconnected" && this.retry.enabled) { this.reconnect(); }
        }, 3000);


        this.duct._connection_listener.on(["onclose", "onerror"], () => { this.status = "disconnected"; } );

        this.duct.invokeOrWaitForOpen(() => {
            this.status = "connected"
            this.lastPinged = dateFormat(new Date(), "HH:MM:ss")
        });
    }
}
</script>
