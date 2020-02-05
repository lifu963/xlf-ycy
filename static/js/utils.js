//字符串格式化
String.prototype.format = function () {
    var str = this;
    for (var i = 0; i < arguments.length; i++) {
        var str = str.replace(new RegExp('\\{' + i + '\\}', 'g'), arguments[i])
    }
    ;
    return str;
}

//数字格式化
function numFormat(num) {
    return ('00' + num).substr(-2);
}

//时间格式化
function timeFormat(timestamp) {
    var datetime = new Date(timestamp * 1000);
    var year = datetime.getFullYear();
    var month = numFormat(datetime.getMonth() + 1);
    var day = numFormat(datetime.getDate());
    var hour = numFormat(datetime.getHours());
    var minute = numFormat(datetime.getMinutes());
    var second = numFormat(datetime.getSeconds());
    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}

function setCookie(cname,cvalue,exdays){
    var d=new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires="expires="+d.toUTCString();
    document.cookie=cname+'='+cvalue+'; '+expires;
}

function getCookie(cname) {
    var name=cname+'=';
    var ca=document.cookie.split(';');
    for(var i=0;i<ca.length;i++){
        var c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return '';
}