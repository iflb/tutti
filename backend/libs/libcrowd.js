window.ducts.dynamiccrowd = window.ducts.dynamiccrowd || {};
window.ducts.dynamiccrowd.event = window.ducts.dynamiccrowd.event || {};
//window.ducts.nds.asr = window.ducts.nds.asr || {};
//window.ducts.nds.asr.event = window.ducts.nds.asr.event || {};
window.ducts.dynamiccrowd._local = window.ducts.dynamiccrowd._local || {};

/*
window.ducts.nds.ResourceEventListener = class extends window.ducts.DuctEventListener {
    scenarioMetadata(event) {}
    scenariosByDate(event) {}
    scenariosByLocation(event) {}
}

window.ducts.nds.DialogueEventListener = class extends window.ducts.DuctEventListener {
    startScenario(event) {}
    startSentence(event) {}
    startSection(event) {}
    clause(event) {}
    endSection(event) {}
    endSentence(event) {}
    endScenario(event) {}
    discussion(event) {}
    skipScenario(event) {}
    suspend(event) {}
    resume(event) {}
    audio(event) {}
    request(event) {}
};

window.ducts.nds.asr.SpeechRecognizerEventListener = class extends window.ducts.DuctEventListener {
    preparing(event) {}
    available(event) {}
    unavailable(event) {}
};

window.ducts.nds.ResourceEvent = class extends window.ducts.DuctMessageEvent {

    constructor(rid, eid, data) {
	super(rid, eid, data);
    }

};

window.ducts.nds.event.ScenarioMetadata = class extends window.ducts.nds.ResourceEvent {

    constructor(rid, eid, data) {
	super(rid, eid, data);
	this.key = data['key'];
	this.title = data['title'];
	this.description = 'description' in data ? data['description'] : null;
	if (('latitude' in data) && ('longitude' in data)) {
	    this.geo = {};
	    this.geo.latitude = 'latitude' in data ? data['latitude'] : null;
	    this.geo.longitude = 'longitude' in data ? data['longitude'] : null;
	    this.geo.distance = 'distance' in data ? data['distance'] : null;
	}
    }
    
};

window.ducts.nds.event.ScenariosByDate = class extends window.ducts.nds.ResourceEvent {

    constructor(rid, eid, data) {
	super(rid, eid, data);
	this.scenarios = [];
	for (let scenario of data) {
	    this.scenarios.push(new window.ducts.nds.event.ScenarioMetadata(rid, eid, scenario));
	}
    }

};

window.ducts.nds.event.ScenariosByLocation = class extends window.ducts.nds.ResourceEvent {

    constructor(rid, eid, data) {
	super(rid, eid, data);
	this.scenarios = [];
	for (let scenario of data) {
	    this.scenarios.push(new window.ducts.nds.event.ScenarioMetadata(rid, eid, scenario));
	}
    }

};

window.ducts.nds.DialogueEvent = class extends window.ducts.DuctMessageEvent {

    constructor(rid, eid, data) {
	super(rid, eid, data);
    }

};

window.ducts.nds.event.StartScenario = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
	this.scenario_key = data['SCENARIO_KEY'];
    }
    
};

window.ducts.nds.event.StartSentence = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
	this.sentence_id = data['SENTENCE_ID'];
	this.utterance = data['UTTERANCE'];
    }
    
};

window.ducts.nds.event.StartSection = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
	this.section_id = data['SECTION_ID'];
	this.utterance = data['UTTERANCE'];
	this.questions = [];
	for (let [key, value] of Object.entries(data)) {
	    if (key.startsWith('REQUEST')) {
		this.questions.push(value);
	    }
	}
    }
    
};

window.ducts.nds.event.Clause = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
	this.utterance = data['UTTERANCE'];
    }
    
};

window.ducts.nds.event.EndSection = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.event.EndSentence = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.event.EndScenario = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.event.SkipScenario = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.event.Discussion = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.event.Suspend = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.event.Resume = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.event.Audio = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
	if (data && data.length > 0) {
	    this.play = true;
	} else {
	    this.play = false;
	}
    }
    
};

window.ducts.nds.event.Request = class extends window.ducts.nds.DialogueEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
	this.utterance = data['UTTERANCE'];
    }
    
};



window.ducts.nds.asr.SpeechRecognizerEvent = class extends window.ducts.DuctMessageEvent {

    constructor(rid, eid, data) {
	super(rid, eid, data);
    }

};

window.ducts.nds.asr.event.Preparing = class extends window.ducts.nds.asr.SpeechRecognizerEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.asr.event.Available = class extends window.ducts.nds.asr.SpeechRecognizerEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.asr.event.Unavailable = class extends window.ducts.nds.asr.SpeechRecognizerEvent {
    
    constructor(rid, eid, data) {
	super(rid, eid, data);
    }
    
};

window.ducts.nds.asr.state = Object.freeze({
    PREPARING : 0
    , AVAILABLE : 1
    , UNAVAILABLE : 2
});
*/

/*
window.ducts.nds.Facade = class {

    constructor(wsd) {
    	this._duct = new window.ducts.nds._local.Duct(wsd);
    
    	this.onConnection = 
    	    (names, func) => {
    		this._duct._connection_listener.on(names, func);
    	    };
    		
    	this.onResource =
    	    (names, func) => {
    		this._duct._resource_listener.on(names, func);
    	    };
    		
    	this.onDialogue =
    	    (names, func) => {
    		this._duct._dialogue_listener.on(names, func);
    	    };
    		
    	this.onASR =
    	    (names, func) => {
    		this._duct._asr_listener.on(names, func);
    	    };
    	
    	//this.catchall_event_handler =
    	//(rid, eid, data) => {console.log('on_message eid='+eid)};
    	//this.uncaught_event_handler = (rid, eid, data) => {};
    	//this.event_error_handler = (rid, eid, data, error) => {console.error(error);};
    	
    	this.open =
    	    () => {
    		self = this;
    		return new Promise(function(resolve, reject) {
    		    self._duct.open()
    			.then(function(duct) {
    			    resolve(self);
    			})
    			.catch(function(error){
    			    reject(error);
    			});
    		});
    	    };
    
    	this.close =
    	    () => {
    		this._duct.close();
    	    };
    
    }

    get resource_controller() {
	    return this._duct._resource;
    }

    get dialogue_controller() {
	    return this._duct._dialogue;
    }

    get speech_recognizer() {
	    return this._duct._asr;
    }

    get state() {
	    return this._duct.state;
    }

};
*/

/*
window.ducts.nds.ResourceController = class {
    
    constructor(duct) {
	this._duct = duct;
	this.getScenarioMetadata =
	    (scenarioKey) => {
		return this._duct.sendResourceCommand(
		    this._duct.EVENT.GET_SCENARIO_METADATA
		    , {'key':scenarioKey});
	    };
	this.getScenariosByLocation =
	    (latitude, longitude, radius, unit='km') => {
		return this._duct.sendResourceCommand(
		    this._duct.EVENT.GET_SCENARIOS_BY_LOCATION
		    , {'latitude': latitude, 'longitude': longitude, 'radius': radius, 'unit': unit});
	    };
	
	this.getScenariosByDate =
	    (from, to) => {
		return this._duct.sendResourceCommand(
		    this._duct.EVENT.GET_SCENARIOS_BY_DATE
		    , {'from': from, 'to': to});
	    };
	
    }
	
}

window.ducts.nds.DialogueController = class {
    
    constructor(duct) {
	this._duct = duct;
	
	this.play =
	    (scenarioKey) => {return this._duct.sendStartScenario(scenarioKey);};

	this.suspend =
	    () => {return this._duct.sendUserBehavior('Suspend');};

	this.resume =
	    () => {return this._duct.sendUserBehavior('Resume');};

	this.skipScenario =
	    () => {return this._duct.sendUserBehavior('SkipScenario');};

	this.skipSection =
	    () => {return this._duct.sendUserBehavior('SkipSection');};

	this.skipSentence =
	    () => {return this._duct.sendUserBehavior('SkipSentence');};

	this.repeatSection =
	    () => {return this._duct.sendUserBehavior('RepeatSection');};

	this.repeatSentence =
	    () => {return this._duct.sendUserBehavior('RepeatSentence');};

	this.sendUtteranceText =
	    (text) => {return this._duct.sendUserBehavior(text);};

    }
};

window.ducts.nds.AutomaticSpeechRecognizer = class {
    
    constructor(duct) {
	this._duct = duct;
	
	this._state = window.ducts.nds.asr.state.UNAVAILABLE;
	
	this.start =
	    () => {return this._duct.sendASRCtrl('START');};

	this.process =
	    (audio) => {return this._duct.sendASRInput(audio);};
	
	this.stop =
	    () => {return this._duct.sendASRCtrl('STOP');};
    }

    get state() {
	return this._state;
    }

};
*/

window.ducts.dynamiccrowd.Duct = class extends window.ducts.Duct {

    constructor(wsd) {
	    super(wsd);

	    //this._resource = new window.ducts.nds.ResourceController(this);
	    //this._dialogue = new window.ducts.nds.DialogueController(this);
	    //this._asr = new window.ducts.nds.AutomaticSpeechRecognizer(this);
	    //
	    //this._resource_listener = new window.ducts.nds.ResourceEventListener(this);
	    //this._dialogue_listener = new window.ducts.nds.DialogueEventListener(this);
	    //this._asr_listener = new window.ducts.nds.asr.SpeechRecognizerEventListener(this);

	    //this.sendResourceCommand =
	    //    (event_id, kwargs) => {
	    //	return this._sendResourceCommand(this, event_id, kwargs);
	    //    };

	    //this.sendStartScenario =
	    //    (scenarioKey) => {return this._sendStartScenario(this, scenarioKey);};
	    //
	    //this.sendUserBehavior =
	    //    (behavior) => {return this._sendUserBehavior(this, behavior);};
	    //	
	    //this.sendASRCtrl =
	    //    (ctrl) => {return this._sendASRCtrl(this, ctrl);};
	    //
	    //this.sendASRInput =
	    //    (audio) => {return this._sendASRInput(this, audio);};
	    
	    this._setup_handlers(this);
	    
    }
    
    _setup_handlers(self) {
        /*
	    self.setEventHandler(
	        self.EVENT.GET_SCENARIO_METADATA,
	        (rid, eid, data) => {
	    	self._resource_listener.scenarioMetadata(
	    	    new window.ducts.nds.event.ScenarioMetadata(rid, eid, data));
	        });
	    self.setEventHandler(
	        self.EVENT.GET_SCENARIOS_BY_DATE,
	        (rid, eid, data) => {
	    	self._resource_listener.scenariosByDate(
	    	    new window.ducts.nds.event.ScenariosByDate(rid, eid, data));
	        });
	    self.setEventHandler(
	        self.EVENT.GET_SCENARIOS_BY_LOCATION,
	        (rid, eid, data) => {
	    	self._resource_listener.scenariosByLocation(
	    	    new window.ducts.nds.event.ScenariosByLocation(rid, eid, data));
	        });
	    self.setEventHandler(
	        self.EVENT.SYSTEM_AUDIO_MODEL,
	        (rid, eid, data) => {
	    	self._dialogue_listener.audio(
	    	    new window.ducts.nds.event.Audio(rid, eid, data));
	        });
	    self.setEventHandler(
	        self.EVENT.SYSTEM_BEHAVIOR_MODEL,
	        (rid, eid, data) => {self._handleDialogueEvent(self, rid, eid, data)});
	    self.setEventHandler(
	        self.EVENT.ASRCTRL_MODEL,
	        (rid, eid, data) => {self._handleASREvent(self, rid, eid, data);});

	    self._dialogue_handler = {};
	    self._dialogue_handler['START_SCENARIO'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.startScenario(new window.ducts.nds.event.StartScenario(rid, eid, data));
	        };
	    self._dialogue_handler['START_SENTENCE'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.startSentence(
	    	    new window.ducts.nds.event.StartSentence(rid, eid, data));
	        };
	    self._dialogue_handler['START_SECTION'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.startSection(
	    	    new window.ducts.nds.event.StartSection(rid, eid, data));
	        };
	    self._dialogue_handler['NEXT_CLAUSE'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.clause(
	    	    new window.ducts.nds.event.Clause(rid, eid, data));
	        };
	    self._dialogue_handler['END_SECTION'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.endSection(
	    	    new window.ducts.nds.event.EndSection(rid, eid, data));
	        };
	    self._dialogue_handler['END_SENTENCE'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.endSentence(
	    	    new window.ducts.nds.event.EndSentence(rid, eid, data));
	        };
	    self._dialogue_handler['DISCUSSION'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.discussion(
	    	    new window.ducts.nds.event.Discussion(rid, eid, data));
	        };
	    self._dialogue_handler['END_SCENARIO'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.endScenario(
	    	    new window.ducts.nds.event.EndScenario(rid, eid, data));
	        };
	    self._dialogue_handler['SKIP_SCENARIO'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.skipScenario(
	    	    new window.ducts.nds.event.SkipScenario(rid, eid, data));
	        };
	    self._dialogue_handler['SUSPEND'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.suspend(
	    	    new window.ducts.nds.event.Suspend(rid, eid, data));
	        };
	    self._dialogue_handler['RESUME'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.resume(
	    	    new window.ducts.nds.event.Resume(rid, eid, data));
	        };
	    self._dialogue_handler['REQUEST'] =
	        (rid, eid, data) => {
	    	self._dialogue_listener.request(
	    	    new window.ducts.nds.event.Request(rid, eid, data));
	        };
	    
	    
	    self._asr_handler = {};
	    self._asr_handler['QUEUE'] = 
	        (rid, eid, data) => {
	    	self._asr._state = window.ducts.nds.asr.state.PREPARING;
	    	self._asr_listener.preparing(
	    	    new window.ducts.nds.asr.event.Preparing(rid, eid, data));
	        };
	    self._asr_handler['RUNNING'] =
	        (rid, eid, data) => {
	    	self._asr._state = window.ducts.nds.asr.state.AVAILABLE;
	    	self._asr_listener.available(
	    	    new window.ducts.nds.asr.event.Available(rid, eid, data));
	        };
	    self._asr_handler['END'] = self._asr_handler['ERROR'] = self._asr_handler['INIT'] =
	        (rid, eid, data) => {
	    	self._asr._state = window.ducts.nds.asr.state.UNAVAILABLE;
	    	self._asr_listener.unavailable(
	    	    new window.ducts.nds.asr.event.Unavailable(rid, eid, data));
	        };
        */
    }

    _onopen(self, event) {
	    super._onopen(self, event);
	    self.send(self.next_rid(), self.EVENT.SYSTEM_BEHAVIOR_MODEL, null);
	    self.send(self.next_rid(), self.EVENT.SYSTEM_AUDIO_MODEL, null);
	    self.send(self.next_rid(), self.EVENT.ASRCTRL_MODEL, null);
    }

    /*
    _handleDialogueEvent(self, rid, eid, data) {
	    let state = ('STATE' in data) ? data.STATE : '';
	    console.log('STATE='+state);
	    let handle = (state in self._dialogue_handler) ? self._dialogue_handler[state] :
	        (rid, eid, data) => {
	    	self.uncaught_event_handler(rid, eid, data);
	        };
	    handle(rid, eid, data);
    }
    
    _handleASREvent(self, rid, eid, data) {
	    let state = ('STATE' in data) ? data.STATE : '';
	    let handle = (state in self._asr_handler) ? self._asr_handler[state] :
	        (rid, eid, data) => {
	    	self.duct.uncaught_event_handler(rid, eid, data);
	        };
	    handle(rid, eid, data);
    }
    
    _sendResourceCommand(self, event_id, kwargs) {
	    let rid = self.next_rid();
	    let eid = event_id;
	    let data = kwargs;
	    return self._send(self, rid, eid, data);
    }

    _sendStartScenario(self, scenarioKey) {
	    let rid = self.next_rid();
	    let eid = self.EVENT.MAIN_CONTROLLER;
	    let data = {'key':scenarioKey};
	    return self._send(self, rid, eid, data);
    }

    _sendUserBehavior(self, behavior) {
	    let rid = self.next_rid();
	    let eid = self.EVENT.USER_BEHAVIOR_LISTENER;
	    let data = behavior;
	    return self._send(self, rid, eid, data);
    }

    _sendASRCtrl(self, ctrl) {
	    let rid = self.next_rid();
	    let eid = self.EVENT.ASRCTRL_LISTENER;
	    let data = ctrl;
	    return self.send(rid, eid, data);
    }

    _sendASRInput(self, audio) {
	    let rid = self.next_rid();
	    let eid = self.EVENT.USER_WAV_AUDIO_LISTENER;
	    let data = audio
	    return self.send(rid, eid, data);
    }
    */

};


//window.ducts.nds.asr.AudioRecorder = class {
//
//    constructor() {
//	this._isEdge = navigator.userAgent.indexOf('Edge') !== -1 && (!!navigator.msSaveOrOpenBlob || !!navigator.msSaveBlob);
//	this._isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
//	this._recorder; // globally accessible
//	this._microphone;
//
//	this.get_user_media =
//	    (callback) => {this._get_user_media(this, callback)};
//	    
//	this.start_recording =
//	    () => {this._start_recording(this, null)};
//	    
//	this.stop_recording =
//	    () => {this._stop_recording(this)};
//
//	this._ondata_event_handler = null;
//	this.set_ondata_event_handler = 
//	    (handler) => {this._ondata_event_handler = handler;};
//
//	this._recorder_event_handler = null;
//	this.set_recorder_event_handler = 
//	    (handler) => {this._recorder_event_handler = handler;};
//
//	this._recorder_error_handler = null;
//	this.set_recorder_error_handler = 
//	    (handler) => {this._recorder_error_handler = handler;};
//
//    }
//
//    _get_user_media(self, callback) {
//	console.log('get_user_media');
//	if(self._microphone) {
//	    callback(self._microphone);
//	    return;
//	}
//	if(typeof navigator.mediaDevices === 'undefined' || !navigator.mediaDevices.getUserMedia) {
//	    alert('This browser does not supports WebRTC getUserMedia API.');
//	    if(!!navigator.getUserMedia) {
//		alert('This browser seems supporting deprecated getUserMedia API.');
//	    }
//	}
//	navigator.mediaDevices.getUserMedia({
//	    audio: isEdge ? true : {
//		echoCancellation: false
//	    }
//	}).then(function(mic) {
//	    callback(mic);
//	}).catch(function(error) {
//	    alert('Unable to capture your microphone. Please check console logs.');
//	    console.error(error);
//	});
//    }
//
//    _start_recording(self, microphone) {
//
//	console.log('start_recording:mic='+microphone)
//	
//	if (!self._microphone) {
//	    if (!microphone) {
//		self.get_user_media(function(stream) {
//		    self._start_recording(self, stream);
//		});
//	    } else {
//		self._microphone = microphone;
//		if(self._isSafari) {
//		    alert('Please click startRecording button again. First time we tried to access your microphone. Now we will record it.');
//		    return;
//		}
//		self._start_recording(self, microphone);
//	    }
//	    return;
//	}
//	var options = {
//	    type: 'audio',
//	    recorderType: RecordRTC.StereoAudioRecorder,
//	    mimeType: 'audio/wav',
//	    //disableLogs: false,
//	    //numberOfAudioChannels: isEdge ? 1 : 2,
//	    desiredSampRate: 16000,
//	    numberOfAudioChannels: 1,
//	    checkForInactiveTracks: true,
//	    bufferSize: 16384,
//	    timeSlice: 1000
//	};
//	/**
//	if(navigator.platform && navigator.platform.toString().toLowerCase().indexOf('win') === -1) {
//	    options.sampleRate = 48000; // or 44100 or remove this line for default
//	}
//	if(self._isSafari) {
//	    options.sampleRate = 44100;
//	    options.bufferSize = 4096;
//	    options.numberOfAudioChannels = 2;
//	}
//	*/
//	if(self._recorder) {
//	    self._recorder.destroy();
//	    self._recorder = null;
//	}
//	
//	options.ondataavailable = (blob) => {
//	    if (this._ondata_event_handler) {
//		let fileReader = new FileReader();
//		fileReader.onload = (event) => {self._ondata_event_handler(self, event.target.result);};
//		fileReader.readAsArrayBuffer(blob);
//	    } else {
//		console.log('dataavailable:e='+blob);
//	    }
//	}
//	
//	self._recorder = RecordRTC(self._microphone, options);
//	
//	self._recorder.startRecording();
//
//    }
//
//    _stop_recording(self) {
//	if (self._recorder) {
//	    self._recorder.stopRecording(self._stopRecordingCallback);
//	}
//    }
//
//    _stopRecordingCallback() {
//
//    }
//
//    _release_microphone(self) {
//	if(self._microphone) {
//	    self._microphone.stop();
//	    self._microphone = null;
//	}
//	if(self._recorder) {
//	    // click(btnStopRecording);
//	}
//    }
//
//}
//
//
//
//
//
//
