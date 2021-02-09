window.ducts.tutti = window.ducts.tutti || {};
window.ducts.tutti.event = window.ducts.tutti.event || {};
window.ducts.tutti._local = window.ducts.tutti._local || {};

window.ducts.tutti.Duct = class extends window.ducts.Duct {

    constructor(wsd) {
	    super(wsd);

        this.controllers = {
            resource: new window.ducts.tutti.ResourceController(this),
            mturk: new window.ducts.tutti.MTurkController(this)
        };
        this.eventListeners = {
            mturk: new window.ducts.tutti.MTurkEventListener()
        };

        this.sendMsg = ({ tag, eid, data }) => {
            const rid = this.next_rid( );
            if(typeof data === "string") { data = data.split(" ") }
            this.send( rid, eid, data)
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
                this.evtHandlersNew[eid].push({ success, error } );
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
                    for(var i in this.evtHandlersNew[eid])  this.evtHandlersNew[eid][i].success({ rid, eid, timestamp: data["Timestamp"], data: data["Data"] } );
                else if (data["Status"]=="Error") {
                    console.error("Tutti event error:", data["Reason"] );
                    for(var i in this.evtHandlersNew[eid]) {
                        if(this.evtHandlersNew[eid][i].error) {
                            this.evtHandlersNew[eid][i].error({ rid, eid, timestamp: data["Timestamp"], data: data } );
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
            this.setupHandlers(this);
            for(var i in this.onOpenHandlers){
                this.onOpenHandlers[i]( );
            }
        } );


    }

    setTuttiEventHandler(eid, success, error) {
        this.setEventHandler(eid, (rid, eid, data) => {
            if (data["Status"]=="Success") success({ rid, eid, timestamp: data["Timestamp"], data: data["Data"] } );
            else if (data["Status"]=="Error" && error) error({ rid, eid, timestamp: data["Timestamp"], reason: data["Reason"] } );
        } );
    }

    invokeOrWaitForOpen(f) {
        if(this.state==window.ducts.State.OPEN_CONNECTED) f( );
        else this.addOnOpenHandler(f );
    }
 
    _onopen(self, event) {
	    super._onopen( self, event );
        self.addEvtHandler({
            tag: "",
	        eid: self.EVENT.APP_WSD,
	        handler: (rid, eid, data) => {
                self.APP_WSD = data
	        }
        } );
	    self.send( self.next_rid(), self.EVENT.APP_WSD, null );
    }

    // FIXME:: needs a protocol
    _handleMTurk(self, name, data) {
        if(data["Status"]=="Success") {
            for(const func of self.eventListeners.mturk[name].success)  func(data["Data"]);
        }
        else
            for(const func of self.eventListeners.mturk[name].error)  func(data);
    }
    _handleResource(self, name, data) {
        if(data["Status"]=="Success")
            for(const func of self.eventListeners.resource[name].success)  func(data["Data"]);
        else
            for(const func of self.eventListeners.resource[name].error)  func(data);
    }

    setupHandlers(self) {
        self.setEventHandler( self.EVENT.MTURK_GET_CREDENTIALS,
                              (rid, eid, data) => { self._handleMTurk(self, "getCredentials", data); } );

        self.setEventHandler( self.EVENT.MTURK_SET_CREDENTIALS,
                              (rid, eid, data) => { self._handleMTurk(self, "setCredentials", data); } );

        self.setEventHandler( self.EVENT.MTURK_CLEAR_CREDENTIALS,
                              (rid, eid, data) => { self._handleMTurk(self, "clearCredentials", data); } );

        self.setEventHandler( self.EVENT.MTURK_SET_SANDBOX,
                              (rid, eid, data) => { self._handleMTurk(self, "setSandbox", data); } );

        self.setEventHandler( self.EVENT.MTURK_GET_HIT_TYPES,
                              (rid, eid, data) => { self._handleMTurk(self, "getHITTypes", data); } );

        self.setEventHandler( self.EVENT.MTURK_CREATE_HIT_TYPE,
                              (rid, eid, data) => { self._handleMTurk(self, "createHITType", data); } );

        self.setEventHandler( self.EVENT.MTURK_CREATE_HITS_WITH_HIT_TYPE,
                              (rid, eid, data) => { self._handleMTurk(self, "createHITsWithHITType", data); } );

        self.setEventHandler( self.EVENT.MTURK_LIST_QUALIFICATIONS,
                              (rid, eid, data) => { self._handleMTurk(self, "listQualifications", data); } );

        self.setEventHandler( self.EVENT.MTURK_LIST_HITS,
                              (rid, eid, data) => { self._handleMTurk(self, "listHITs", data); } );

        self.setEventHandler( self.EVENT.MTURK_EXPIRE_HITS,
                              (rid, eid, data) => { self._handleMTurk(self, "expireHITs", data); } );

        self.setEventHandler( self.EVENT.MTURK_DELETE_HITS,
                              (rid, eid, data) => { self._handleMTurk(self, "deleteHITs", data); } );

        self.setEventHandler( self.EVENT.MTURK_CREATE_QUALIFICATION,
                              (rid, eid, data) => { self._handleMTurk(self, "createQualification", data); } );

        self.setEventHandler( self.EVENT.MTURK_LIST_WORKERS_WITH_QUALIFICATION_TYPE,
                              (rid, eid, data) => { self._handleMTurk(self, "listWorkersWithQualificationType", data); } );

        self.setEventHandler( self.EVENT.MTURK_DELETE_QUALIFICATIONS,
                              (rid, eid, data) => { self._handleMTurk(self, "deleteQualifications", data); } );

        //self.setEventHandler( self.EVENT.MTURK_, (rid, eid, data) => { self._handleMTurk(self, "", data); } );
    }
};

window.ducts.tutti.DuctEventListener = class extends window.ducts.DuctEventListener {  // overrides the "extended" class
    
    constructor() {
        super();
	    this.on =
	        (names) => (new Promise((resolve, reject) => {
	    	        for(let name of (names instanceof Array) ? names : [names]) {
	    	            if (!(name in this)) {
	    	        	    throw new ReferenceError('['+name+'] is not defined in '+this.constructor.name);
	    	            } 

                        // if the listener is an empty object (= no handler is registered yet), then initialize it
                        if(this[name] && Object.keys(this[name]).length === 0 && this[name].constructor === Object)  this[name] = { success: [], error: [] };
                        
	    	            this[name].success.push(resolve);
	    	            this[name].error.push(reject);
	    	        }
	            })
            );
    }
};

//window.ducts.tutti.MTurkEvent = class extends window.ducts.DuctMessageEvent {
//
//    constructor(rid, eid, data) {
//	    super(rid, eid, data);
//    }
//
//};

window.ducts.tutti.MTurkEventListener = class extends window.ducts.tutti.DuctEventListener {
    constructor() {
        super();

        this.getCredentials = {};
        this.setCredentials = {};
        this.clearCredentials = {};
        this.setSandbox = {};
        this.getHITTypes = {};
        this.createHITType = {};
        this.createHITsWithHITType = {};
        this.listQualifications = {};
        this.listHITs = {};
        this.expireHITs = {};
        this.deleteHITs = {};
        this.createQualification = {};
        this.listWorkersWithQualificationType = {};
        this.deleteQualifications = {};
        //this. = {};
    }
}

window.ducts.tutti.MTurkController = class {
    constructor( duct ){
        this._duct = duct;

        this.getCredentials =
            (  ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_GET_CREDENTIALS );
            };
        this.setCredentials =
            ( AccessKeyId, SecretAccessKey ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_SET_CREDENTIALS, { AccessKeyId, SecretAccessKey } );
            };
        this.setSandbox =
            ( Enabled ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_SET_SANDBOX, { Enabled } );
            };
        this.clearCredentials =
            (  ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_CLEAR_CREDENTIALS );
            };

        this.deleteQualifications =
            ( QualificationTypeIds ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_DELETE_QUALIFICATIONS, { QualificationTypeIds } );
            };
        this.listQualifications =
            () => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_LIST_QUALIFICATIONS );
            };
        this.listWorkersWithQualificationType =
            ( QualificationTypeId ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_LIST_WORKERS_WITH_QUALIFICATION_TYPE, { QualificationTypeId } );
            };
        this.createQualification =
            ( QualificationTypeParams ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_CREATE_QUALIFICATION, QualificationTypeParams );
            };
        this.associateQualificationsWithWorkers =
            ( AssociateQualificationParams ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_ASSOCIATE_QUALIFICATIONS_WITH_WORKERS, AssociateQualificationParams );
            };
        this.listWorkers =
            (  ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.LIST_WORKERS, { Platform: "MTurk" } );
            };
        this.notifyWorkers =
            ( Subject, MessageText, sendEmailWorkerIds ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_NOTIFY_WORKERS, { Subject, MessageText, sendEmailWorkerIds } );
            };
        this.createHITType =
            ( CreateHITTypeParams ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_CREATE_HIT_TYPE, { CreateHITTypeParams } );
            };
        this.createHITsWithHITType =
            ( ProjectName, NumHITs, CreateHITsWithHITTypeParams ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_CREATE_HITS_WITH_HIT_TYPE, { ProjectName, NumHITs, CreateHITsWithHITTypeParams } );
            };
        this.getHITTypes =
            ( HITTypeIds ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_GET_HIT_TYPES, { HITTypeIds } );
            };
        this.expireHITs =
            ( HITIds ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_EXPIRE_HITS, { HITIds } );
            };
        this.deleteHITs =
            ( HITIds ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_DELETE_HITS, { HITIds } );
            };
        this.listHITs =
            ( Cached ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.MTURK_LIST_HITS, { Cached } );
            };
        //this. =
        //    (  ) => {
        //        return this._duct.send( this._duct.next_rid(), this._duct.EVENT., {  } );
        //    };
        //this. =
        //    (  ) => {
        //        return this._duct.send( this._duct.next_rid(), this._duct.EVENT., {  } );
        //    };
    }
}

window.ducts.tutti.ResourceController = class {
    constructor(duct){
        this._duct = duct;

        this.getEventHistory =
            () => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.EVENT_HISTORY );
            };
        this.setEventHistory =
            ( eid, query ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.EVENT_HISTORY, `${this.eid} ${this.query}` );
            };

        this.listProjects =
            () => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.LIST_PROJECTS );
            };
        this.createProject =
            ( ProjectName ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.CREATE_PROJECT, { ProjectName } );
            };
        this.listTemplates =
            ( ProjectName ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.LIST_TEMPLATES, { ProjectName } );
            };
        this.getAnswersForTemplate =
            ( ProjectName, TemplateName ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.GET_ANSWERS_FOR_TEMPLATE, { ProjectName, TemplateName } );
            };
        this.createTemplates =
            ( ProjectName, TemplateNames, PresetEnvName, PresetTemplateName ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.CREATE_TEMPLATES, { ProjectName, TemplateNames, PresetEnvName, PresetTemplateName } );
            };
        this.listTemplatePresets =
            () => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.LIST_TEMPLATE_PRESETS );
            };
        this.getProjectScheme =
            ( ProjectName, Cached ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.GET_PROJECT_SCHEME, { ProjectName, Cached } );
            };
        this.getNanotasks =
            ( ProjectName, TemplateName ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.GET_NANOTASKS, { ProjectName, TemplateName } );
            };
        this.deleteNanotasks =
            ( NanotaskIds ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.DELETE_NANOTASKS, { NanotaskIds } );
            };
        this.updateNanotaskNumAssignable =
            ( NanotaskId, NumAssignable ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.UPDATE_NANOTASK_NUM_ASSIGNABLE, { NanotaskId, NumAssignable } );
            };
        this.uploadNanotasks =
            ( ProjectName, TemplateName, Nanotasks, NumAssignable, Priority, TagName ) => {
                return this._duct.send( this._duct.next_rid(), this._duct.EVENT.UPLOAD_NANOTASKS, { ProjectName, TemplateName, Nanotasks, NumAssignable, Priority, TagName } );
            };
        //this. =
        //    (  ) => {
        //        return this._duct.send( this._duct.next_rid(), this._duct.EVENT., {  } );
        //    };
        //this. =
        //    (  ) => {
        //        return this._duct.send( this._duct.next_rid(), this._duct.EVENT., {  } );
        //    };
    }
    
}
