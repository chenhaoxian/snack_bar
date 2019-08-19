const app = getApp()
const util = require('../../utils/util.js')

Page({
  data: {
    host: app.globalData.envHost,
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    sessionInfo: {},
    gloabalFomIds: {},
    circleList: [],//圆点数组
    awardList: [],//奖品数组
    colorCircleFirst: '#FFDF2F',//圆点颜色1
    colorCircleSecond: '#FE4D32',//圆点颜色2
    colorAwardDefault: '#F5F0FC',//奖品默认颜色
    colorAwardSelect: '#ed601a',//奖品选中颜色
    indexSelect: 0,//被选中的奖品index
    isRunning: false,//是否正在抽奖
    imageAward: [
      '../../images/0.jpg',
      '../../images/3.jpg',
      '../../images/0.jpg',
      '../../images/4.jpg',
      '../../images/0.jpg',
      '../../images/1.jpg',
      '../../images/0.jpg',
      '../../images/6.jpg',
    ],//奖品图片数组
    drawQuota: 0,
    existValidFormId: wx.getStorageSync("hasFormId")
  },

  onLoad: function () {
    this.initLuckyDraw()
    var self = this;
    var userInfo = wx.getStorageSync("userInfo")
    var sessionInfo = wx.getStorageSync("sessionInfo")
    if (userInfo && sessionInfo) {
      wx.checkSession({
        success: function () {
          self.setData({
            userInfo: userInfo,
            hasUserInfo: true,
            sessionInfo: sessionInfo
          })
          self.getDrawQuota();
          self.hasValidFormId();
        },
        fail: function () {
          // session_key 已经失效，需要重新执行登录流程
          self.init(self)
        }
      })
    } else {
      self.init(self)
    }
  },

  onShow: function () {
    this.setData({
      existValidFormId: wx.getStorageSync("hasFormId")
    })
  },

  init: function (that) {
    wx.login({
      success: function (login) {
        if (login.code) {
          wx.request({
            url: that.data.host + '/api/user/' + login.code,
            success: function (session) {
              that.setData({
                sessionInfo: session.data
              })
              wx.setStorage({ key: "sessionInfo", data: session.data })
              wx.getSetting({
                success(res) {
                  if (res.authSetting['scope.userInfo']) {
                    that.getUserInfo();
                  }
                }
              })
            }
          })
        }
        else {
          console.log('Initial login code fail!' + res.errMsg)
        }
      }
    })
  },

  getUserInfo: function () {
    var self = this;
    wx.getUserInfo({
      withCredentials: true,
      success: function (user) {
        //decode user info in server
        wx.request({
          url: self.data.host + '/api/user',
          data: {
            encryptedData: user.encryptedData,
            iv: user.iv,
            sessionKey: self.data.sessionInfo.session_key
          },
          method: 'POST',
          success: function (res) {
            self.setData({
              userInfo: res.data,
              hasUserInfo: true
            })
            wx.setStorage({ key: "userInfo", data: res.data })
            self.getDrawQuota();
            self.hasValidFormId();
          },
          fail: function (err) {
            console.log("Get user info error:" + JSON.stringify(err))
          }
        })
      }
    })
  },

  //获取formId
  saveFormId: function (e) {
    if (e.detail.formId != 'the formId is a mock one') {
      var formId = e.detail.formId;
      var self = this;
      wx.request({
        url: self.data.host + '/api/form_info',//后台存储的接口
        method: 'POST',
        data: {
          unionId: self.data.userInfo.unionId,
          formId: formId,
          expire: parseInt(new Date().getTime() / 1000) + 604800
        },
        success: function (res) {
          wx.setStorage({ key: "hasFormId", data: true })
          self.setData({
            existValidFormId: true
          })
          console.log("Save data successfully")
        },
        fail: function (err) {
          console.log("Index page saveFormId() error:" + JSON.stringify(err))
        }
      })
    }
  },

  initLuckyDraw: function () {
    var self = this;
    //圆点设置
    var leftCircle = 7.5;
    var topCircle = 7.5;
    var circleList = [];
    for (var i = 0; i < 24; i++) {
      if (i == 0) {
        topCircle = 15;
        leftCircle = 15;
      } else if (i < 6) {
        topCircle = 7.5;
        leftCircle = leftCircle + 102.5;
      } else if (i == 6) {
        topCircle = 15
        leftCircle = 620;
      } else if (i < 12) {
        topCircle = topCircle + 94;
        leftCircle = 620;
      } else if (i == 12) {
        topCircle = 565;
        leftCircle = 620;
      } else if (i < 18) {
        topCircle = 570;
        leftCircle = leftCircle - 102.5;
      } else if (i == 18) {
        topCircle = 565;
        leftCircle = 15;
      } else if (i < 24) {
        topCircle = topCircle - 94;
        leftCircle = 7.5;
      } else {
        return
      }
      circleList.push({ topCircle: topCircle, leftCircle: leftCircle });
    }
    this.setData({
      circleList: circleList
    })
    //圆点闪烁
    setInterval(function () {
      if (self.data.colorCircleFirst == '#FFDF2F') {
        self.setData({
          colorCircleFirst: '#FE4D32',
          colorCircleSecond: '#FFDF2F',
        })
      } else {
        self.setData({
          colorCircleFirst: '#FFDF2F',
          colorCircleSecond: '#FE4D32',
        })
      }
    }, 500)
    //奖品item设置
    var awardList = [];
    //间距
    var topAward = 25;
    var leftAward = 25;
    for (var j = 0; j < 8; j++) {
      if (j == 0) {
        topAward = 25;
        leftAward = 25;
      } else if (j < 3) {
        topAward = topAward;
        //166.6666是宽.15是间距下同
        leftAward = leftAward + 166.6666 + 15;
      } else if (j < 5) {
        leftAward = leftAward;
        //150是高,15是间距下同
        topAward = topAward + 150 + 15;
      } else if (j < 7) {
        leftAward = leftAward - 166.6666 - 15;
        topAward = topAward;
      } else if (j < 8) {
        leftAward = leftAward;
        topAward = topAward - 150 - 15;
      }
      var imageAward = this.data.imageAward[j];
      awardList.push({ topAward: topAward, leftAward: leftAward, imageAward: imageAward });
    }
    this.setData({
      awardList: awardList
    });
  },

  getDrawQuota: function () {
    var self = this;
    wx.request({
      url: self.data.host + '/api/luckydraw/quota/' + self.data.userInfo.unionId,
      success: function (res) {
        var quota = res.data.quota;
        self.setData({
          drawQuota: quota
        })
      },
      fail: function (err) {
        console.log("Get draw quota error:" + JSON.stringify(err))
      }
    });
  },

  startGame: function () {
    if (this.data.isRunning) return
    this.setData({
      isRunning: true
    })
    var self = this;
    var indexSelect = 0
    var i = 0;

    wx.request({
      url: self.data.host + '/api/luckydraw/prize/' + self.data.userInfo.unionId,
      success: function (res) {
        var luckyDraw = res.data;
        var loopIndex = util.getPrizeMappingIndex(luckyDraw.prize.code) + 8;

        //开始转盘
        var timer = setInterval(function () {
          indexSelect++;
          //转盘速度
          i++;
          if (i == loopIndex) {
            //去除循环
            clearInterval(timer)
            //获奖提示
            wx.showModal({
              title: '恭喜您',
              content: '获得了' + luckyDraw.prize.prizeName + " \r\n (请凭截图到Avril处领取奖品^_^)",
              showCancel: false,
              success: function (res) {
                if (res.confirm) {
                  self.setData({
                    isRunning: false
                  })
                }
              }
            })
          }
          indexSelect = indexSelect % 8;
          self.setData({
            indexSelect: indexSelect,
            drawQuota: 0
          })
        }, (200 + i))
      },
      fail: function (err) {
        console.log("Get lucky draw error:" + JSON.stringify(err))
      }
    })
  },

  hasValidFormId: function () {
    var self = this;
    wx.request({
      url: self.data.host + '/api/form_info/' + self.data.userInfo.unionId,
      success: function (res) {
        var result = res.data.result;
        wx.setStorage({ key: "hasFormId", data: result })
        self.setData({
          existValidFormId: result
        })
      }
    })

  },

  //触发表单提交&&推送消息
  // testSubmit: function(e) {
  //   if (drawQuota==1){
  //     var self = this;
  //     wx.request({
  //       url: self.data.host + '/api/form_info',
  //       method: 'POST',
  //       success: function (res) {
  //         // console.log(res);
  //         var _access_token = res.data.access_token;
  //         var url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=' + _access_token;
  //         var _jsonData = {
  //           touser: self.data.userInfo.openId,
  //           template_id: 'tduExnpJ2pkrJVQv2txDnqe_6OW4BtPtRSnxxeFjh2E',
  //           form_id: e.detail.formId,
  //           page: "pages/order/order",
  //           data: {
  //             "keyword1": { "value": "20180612", "color": "#173177" },
  //             "keyword2": { "value": "辣条", "color": "#173177" },
  //             "keyword3": { "value": "非常好吃", "color": "#173177" },
  //             "keyword4": { "value": "10000", "color": "#173177" },
  //             "keyword5": { "value": "未支�", "color": "#173177" },
  //             "keyword6": { "value": "测试数据�", "color": "#173177" },
  //             "keyword7": { "value": "测试数据�", "color": "#173177" },
  //           },
  //           "emphasis_keyword": "keyword1.DATA"
  //         }
  //         wx.request({
  //           url: url,
  //           data: _jsonData,
  //           method: 'POST',
  //           success: function (res) {
  //             console.log("11111111111")
  //             console.log(res)
  //           },
  //           fail: function (err) {
  //             console.log('request fail ', err);
  //           },
  //           complete: function (res) {
  //             console.log("request completed!");
  //           }
  //         })
  //       }
  //     })
  //   }   
  // },

})
