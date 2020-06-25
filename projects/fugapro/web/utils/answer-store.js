import store from '../../../../store.js'

export const updateAnswer = function(anskey, val){
    store.dispatch("updateAnswer", [anskey, val])
}

export const updateAnswerForTag = function(anskey, tag, val){
    store.dispatch("updateAnswerForTag", [anskey, tag, val])
}

export default { updateAnswer, updateAnswerForTag }
