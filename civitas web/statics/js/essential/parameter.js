/*
获取url后附带的参数（如：?url=1）
*/

function get_parameter_value(parameter_name)
{
    /*参数说明：
    parameter_name：参数名
    */
    var reg = new RegExp('(^|&)' + parameter_name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
      return unescape(r[2]);
    }
    return null;
}