//app.js
const config = require('./config/config.js')

App({
  globalData: {
    envHost: config.getHost('zach'),
    existValidFormId: false
  },
  onLaunch: function (options) {
    // console.log(options)

    // wx.openSetting({
    //   success: (res) => {
    //     /*
    //      * res.authSetting = {
    //      *   "scope.userInfo": true,
    //      *   "scope.userLocation": true
    //      * }
    //      */
    //   }
    // })

    // wx.getSetting({
    //   success(res) {
    //     if (!res.authSetting['scope.userInfo']) {
    //       wx.authorize({
    //         scope: 'scope.userInfo',
    //         success() {
    //           wx.getUserInfo()
    //         }
    //       })
    //     }
    //   }
    // })
  },
  
})