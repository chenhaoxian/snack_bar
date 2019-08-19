const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

const randomIndex = function () {
  var indexMapping = [0, 2, 6, 8];
  var randomIndex = Math.round(Math.random() * 3);
  return indexMapping[randomIndex];
}

const prizeMapping = {
  'a0':100,
  'a1': 5,
  'a2': 3,
  'a3': 1,
  'a4': 7
};

const getPrizeMappingIndex = function (code) {
  var result;
  var prizeMapIndex = prizeMapping[code];
  if (prizeMapIndex === 100) {
    result = randomIndex();
  } else {
    result = prizeMapIndex;
  }
  return result;
}

module.exports = {
  formatTime: formatTime,
  getPrizeMappingIndex: getPrizeMappingIndex
}
