export const stringifyUnixTime = function(time){
    return new Date(time).toISOString().split(".")[0].replace("T"," ");
}
