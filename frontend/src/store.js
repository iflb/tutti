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



        currentAnswer: {},
        answers: [],
    },
    mutations: {
        connectDuctsWebSocket(state) {
            state.isWSOpened = false
            axios.get("/ducts/wsd").then(function(response){
                state.ducts.wsd = response.data
                state.ducts.ws = new WSClient(state.ducts.wsd)
                state.ducts.ws.set_onopen_event_handler(function(){
                    state.isWSOpened = true
                })
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
        removeAllOnMessageHandlers(state) {
            state.ducts.ws._onmessage_handlers = {};
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
        setOnMessageDefaultHandler(context, message){ context.commit("setOnMessageDefaultHandler", message) },
        setOnMessageHandler(context, message){ context.commit("setOnMessageHandler", message) },
        removeAllOnMessageHandlers(context){ context.commit("removeAllOnMessageHandlers") },
        sendWSMessage(context, message){ context.commit("sendWSMessage", message) },
        connectDuctsWebSocket(context){ context.commit("connectDuctsWebSocket"); },
        updateAnswer(context, message){ context.commit("updateAnswer", message); },
        updateAnswerForTag(context, message){ context.commit("updateAnswerForTag", message); },
        submitAnswer(context){ context.commit("submitAnswer"); }
    }
})

export default store
