function scheme(){
    return process.env.VUE_APP_SSL=="1" ? "https" : "http";
}

function getHost(dev) {
    return dev ? process.env.VUE_APP_DEV_HOST : process.env.VUE_APP_HOST;
}

function getUrl(prjName, dev=false) {
    const [host, port] = getHost(dev).split(":");
    let _url = `${scheme()}://${host}`;
    if(["80","443"].indexOf(port) == -1) _url += `:${port}`;
    return `${_url}/private-prod/${prjName}`;
}

module.exports = { getUrl }
