import mturk from './platform-config-mturk'
import priv from './platform-config-private'

var config;
if(window.location.ancestorOrigins.length>0 && window.location.ancestorOrigins[0].startsWith("https://workersandbox.mturk.com")) {
    config = mturk;
} else {
    config = priv;
}

export const platformConfig = config;
