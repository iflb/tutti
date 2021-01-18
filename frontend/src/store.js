import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const ductsModule = {
    namespaced: true,
    state: {
        duct: null
    },
    getters: {
        duct: (state) => { return state.duct }
    },
    actions: {
        initDuct({ state }) {
            var ducts = window.ducts = window.ducts || {};
            return new Promise(function(resolve){
                ducts.user = 'guest';
                ducts.context_url = '/ducts';
                ducts.libs_plugin = [ducts.context_url + '/libs/libcrowd.js'];
                ducts.main = function(wsd){
                    var duct = new window.ducts.dynamiccrowd.Duct(wsd);
                    state.duct = duct
                    resolve(duct)
                }
                                                    
                let lib_script = document.createElement('script');
                lib_script.src = ducts.context_url+'/libs/main.js';
                document.body.appendChild(lib_script);
            })
        },
        openDuct({ state }){
            return new Promise((resolve, reject) => {
                state.duct.open().then(resolve).catch(reject);
            })
        },
        closeDuct({ state }){
            state.duct.close()
        },
        onDuctOpen({ state }, f) {
            if(state.duct.state==window.ducts.State.OPEN_CONNECTED) f();
            else state.duct.addOnOpenHandler(f);
        }
    }
}

const store = new Vuex.Store({
    modules: {
        ductsModule
    }
})

export default store
