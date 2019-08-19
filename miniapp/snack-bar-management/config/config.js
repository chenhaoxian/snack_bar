const getHost = function (name) {
  let host = '';
  switch (name) {
    case 'hyman':
      host = 'http://chenhy-2-w7:12301';
      break;
    case 'avril':
      host = 'http://liav2-2-w7:5000';
      break;
    case 'zach':
      host = 'http://shaza-2-w7:5901';
      break;
    default:
      host = 'https://isnackbar.opsmart.cn';
  }
  return host;
};

module.exports = {
  getHost: getHost
}