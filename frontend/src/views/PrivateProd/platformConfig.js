import mturk from './platform-config-mturk'
import priv from './platform-config-private'

export const setPlatformConfig = function(self){
    var config;
    //mturk 
    if(window.location.ancestorOrigins.length>0 && window.location.ancestorOrigins[0].startsWith("https://workersandbox.mturk.com")) {
        config = mturk;
    }
    // private
    else {
        config = priv;
    }
    self._getClientToken = config.getClientToken;
    self._onClientTokenFailure = config.onClientTokenFailure;
    self._onSubmitWorkSession = config.onSubmitWorkSession;
};
