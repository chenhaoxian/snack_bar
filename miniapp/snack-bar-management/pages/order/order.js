const app = getApp()
const util = require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    host: app.globalData.envHost,
    orders: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var self = this;
    var userInfo = wx.getStorageSync("userInfo")
    if (userInfo) {
      this.setData({
        userInfo: userInfo
      })
    } else {
      wx.switchTab({
        url: '../index/index',
      })
    }

    wx.request({
      url: self.data.host + '/api/order/' + userInfo.unionId,
      success: function (res) {
        var orderList = res.data;
        orderList.map(item => {
          item.created_date = util.formatTime(new Date(item.created_date));
          return item;
        })
        // console.log(res.data)
        self.setData({
          orders: res.data,
        });
      },
      fail: function (err) {
        console.log("Get order list error:" + JSON.stringify(err))
      }
    })
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    // console.log('load more....');
    // wx.showNavigationBarLoading()
    // wx.hideNavigationBarLoading()
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})