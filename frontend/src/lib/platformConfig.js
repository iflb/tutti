import cfMturk from './platform-configs/mturk.js'
import cfPrivate from './platform-configs/private.js'

var config = null;

if(document.referrer.length>0 && (document.referrer.startsWith("https://worker.mturk.com") || document.referrer.startsWith("https://workersandbox.mturk.com"))) {
    config = cfMturk
} else {
    config = cfPrivate
}

export const platformConfig = config;
