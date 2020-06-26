import 'babel-polyfill'
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import { WSClient } from './lib/main'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        ducts: {
            ws: null,
            wsd: {}
        },
        isWSOpened: false,
        onOpenHandler: null,

        currentAnswer: {},
        answers: [],
    },
    mutations: {
        connectDuctsWebSocket(state, wsd) {
            state.isWSOpened = false
            state.ducts.wsd = wsd.data
            state.ducts.ws = new WSClient(state.ducts.wsd)
        },
        setOnOpenHandler(state, handler) {
            state.onOpenHandler = handler;
        },
        _setOnOpenHandler(state) {
            state.ducts.ws.set_onopen_event_handler(function(){
                state.isWSOpened = true
                if(state.onOpenHandler) state.onOpenHandler();
            })
        },
        setOnMessageDefaultHandler(state, handler) {
            state.ducts.ws.set_onmessage_default_handler(handler);
        },
        setOnMessageHandler(state, message) {
            const eid = message[0]
            const handler = message[1]
            state.ducts.ws.set_onmessage_handler(eid, handler);
        },
        setOnCloseHandler(state, handler) {
            state.ducts.ws._ws_onclose = handler
        },
        removeAllOnMessageHandlers(state) {
            const handlers = state.ducts.ws._onmessage_handlers
            var remainingHandlers = {}
            for(const evt in handlers){
                if(evt<1000) remainingHandlers[evt] = handlers[evt]
            }
            state.ducts.ws._onmessage_handlers = remainingHandlers;
        },
        sendWSMessage(state, message) {
            const rid = new Date().getTime();
            const eid = message[0]
            const data = message[1]
            state.ducts.ws.send(rid, eid, data)
        },


        updateAnswer(state, data){
            state.currentAnswer = data
        },
        submitAnswer: function(state){
            alert("submitting answer");
            state.answers.push(state.currentAnswer)
            console.table(state.currentAnswer);
        }
    },
    getters: {
        ws: (state) => { return state.ducts.ws },
        wsd: (state) => { return state.ducts.wsd },
        isWSOpened: (state) => { return state.isWSOpened },
        currentAnswer: (state) => { return state.currentAnswer },
        getValueForName: (state) => (name) => { return state.currentAnswer[name] }
    },
    actions: {
        connectDuctsWebSocket(context){
            return new Promise((resolve) => {
                axios.get("/ducts/wsd").then(function(wsd){
                    context.commit("connectDuctsWebSocket", wsd);
                    context.commit("_setOnOpenHandler");
                    resolve()
                })
            })
        },
        setOnOpenHandler(context, message){ context.commit("setOnOpenHandler", message) },
        setOnMessageDefaultHandler(context, message){ context.commit("setOnMessageDefaultHandler", message) },
        setOnMessageHandler(context, message){ context.commit("setOnMessageHandler", message) },
        setOnCloseHandler(context, message){ context.commit("setOnCloseHandler", message) },
        removeAllOnMessageHandlers(context){ context.commit("removeAllOnMessageHandlers") },
        sendWSMessage(context, message){ context.commit("sendWSMessage", message) },
        updateAnswer(context, message){ context.commit("updateAnswer", message); },
        updateAnswerForTag(context, message){ context.commit("updateAnswerForTag", message); },
        submitAnswer(context){ context.commit("submitAnswer"); }
    }
})

export default store
