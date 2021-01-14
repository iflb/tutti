export const stringifyUnixTime = function(unixTime){
    if(unixTime.toString().length==10) unixTime = unixTime*1000;

    var dt = new Date(unixTime);
    return dt.getFullYear() + '-' +
        ('0' + (dt.getMonth() + 1)).slice(-2) + '-'+
        ('0' + dt.getDate()).slice(-2) + ' ' +
        ('0' + dt.getHours()).slice(-2) + ':' +
        ('0' + dt.getMinutes()).slice(-2) + ':' +
        ('0' + dt.getSeconds()).slice(-2);
}
