window.ducts.tutti = window.ducts.tutti || {};
window.ducts.tutti.event = window.ducts.tutti.event || {};
window.ducts.tutti._local = window.ducts.tutti._local || {};

window.ducts.tutti.Duct = class extends window.ducts.Duct {

    constructor(wsd) {
	    super(wsd);

        this.controller = new window.ducts.tutti.Controller(this);

        this.sendMsg = ({ tag, eid, data }) => {
            const rid = this.next_rid();
            if(typeof data === "string") { data = data.split(" ") }
            this.send(rid, eid, data)
            this.log.sent.push({ tag, rid, eid, data })
        }

        this.log = {
            sent: [],
            received: []
        }

        this.evtHandlers = {}
        this.evtHandlersNew = {}

        this.addEvtHandler =
            ({ tag, eid, handler }) => {
                if(!(eid in this.evtHandlers)) this.evtHandlers[eid] = {}
                this.evtHandlers[eid][tag] = handler
            }

        this.addTuttiEvtHandler =
            ({ eid, success, error }) => {
                if(!(eid in this.evtHandlersNew)) this.evtHandlersNew[eid] = [];
                this.evtHandlersNew[eid].push({ success, error });
                console.log("added evt handler");
                console.log(this.evtHandlersNew);
            }
            
        this.catchall_event_handler = (rid, eid, data) => {
            if(eid>=1000) this.log.received.push({ rid, eid, data })
            if(eid in this.evtHandlers) {
                for(var tag in this.evtHandlers[eid]){
                    this.evtHandlers[eid][tag](rid, eid, data)
                }
            }
            if(this.evtHandlersNew[eid]) {
                if(data["Status"]=="Success")
                    for(var i in this.evtHandlersNew[eid])  this.evtHandlersNew[eid][i].success({ rid, eid, timestamp: data["Timestamp"], data: data["Data"] });
                else if (data["Status"]=="Error") {
                    console.error("Tutti event error:", data["Reason"]);
                    for(var i in this.evtHandlersNew[eid]) {
                        if(this.evtHandlersNew[eid][i].error) {
                            this.evtHandlersNew[eid][i].error({ rid, eid, timestamp: data["Timestamp"], data: data });
                        }
                    }
                }
            }
        }

        this.onOpenHandlers = [];
        this.addOnOpenHandler = (handler) => {
            this.onOpenHandlers.push(handler);
        };

        this._connection_listener.on("onopen", () => {
            for(var i in this.onOpenHandlers){
                this.onOpenHandlers[i]();
            }
        });

    }

    setTuttiEventHandler(eid, success, error) {
        this.setEventHandler(eid, (rid, eid, data) => {
            if (data["Status"]=="Success") success({ rid, eid, timestamp: data["Timestamp"], data: data["Data"] });
            else if (data["Status"]=="Error" && error) error({ rid, eid, timestamp: data["Timestamp"], reason: data["Reason"] });
        });
    }

    invokeOrWaitForOpen(f) {
        if(this.state==window.ducts.State.OPEN_CONNECTED) f();
        else this.addOnOpenHandler(f);
    }
 
    _onopen(self, event) {
	    super._onopen(self, event);
        self.addEvtHandler({
            tag: "",
	        eid: self.EVENT.APP_WSD,
	        handler: (rid, eid, data) => {
                self.APP_WSD = data
	        }
        });
	    self.send(self.next_rid(), self.EVENT.APP_WSD, null);
    }
};

window.ducts.tutti.EventListener = class extends window.ducts.DuctEventListener {

}

window.ducts.tutti.Controller = class {
    constructor(duct) {
        this._duct = duct;
    }

    listTemplates(tag, ProjectName) {
        this._duct.sendMsg({
            tag,
            eid: this._duct.EVENT.LIST_TEMPLATES,
            data: { ProjectName }
        });
    }
}
