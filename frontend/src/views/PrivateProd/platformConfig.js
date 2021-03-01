import mturk from './platform-config-mturk'
import priv from './platform-config-private'

var config;
if(document.referrer.length>0 && (document.referrer.startsWith("https://worker.mturk.com") || document.referrer.startsWith("https://workersandbox.mturk.com"))) {
    config = mturk;
} else {
    config = priv;
}

export const platformConfig = config;
