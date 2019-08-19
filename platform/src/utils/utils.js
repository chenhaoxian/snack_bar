/**
 * Created by LIAV2 on 6/24/2018.
 */
let getCookie = function (name) {
  var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
  if (arr = document.cookie.match(reg))
    return (arr[2]);
  else
    return null;
}

let setCookie = function (c_name, value, expiredays) {
  var exdate = new Date();
  exdate.setDate(exdate.getDate() + expiredays);
  document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString());
};

let delCookie = function (name) {
  var exp = new Date();
  exp.setTime(exp.getTime() - 1);
  var cval = getCookie(name);
  if (cval != null)
    document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
};

const user = {
  name: 'admin',
  pwd: '123'
};

let getAdmins = function () {
  return user;
};

const locationMapping = {
  'A': 'Phase 3',
  'B': 'Phase 2',
  'C': 'Phase 1'
};

let getLocation = function(code){
  return locationMapping[code];
};

let getLocationCode = function(code){
  return locationMapping[code];
};

export default {
  getCookie: getCookie,
  setCookie: setCookie,
  delCookie: delCookie,
  getAdmins: getAdmins,
  getLocation: getLocation
}
