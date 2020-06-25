import Vue from 'vue'

export const registerComponent = (name, def) => {
    if(name && def){
        Vue.component(name, def)
    }
}

export const registerComponents = (components) => {
    for(const c in components)
        registerComponent(c, components[c])
}
