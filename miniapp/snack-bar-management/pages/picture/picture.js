const app = getApp()

Page({

  data: {
    host: app.globalData.envHost,
    userInfo: {},
    customizedNickName: ''
  },

  customizedNickName: function (e) {
    this.setData({
      customizedNickName: e.detail.value,
    })
  },

  onLoad: function (options) {

  },
  onShow: function () {
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
  },

  uploadUserImage: function (e) {
    let self = this;
    wx.chooseImage({
      count: 1, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        var tempFilePaths = res.tempFilePaths
        self.upload(self, tempFilePaths);
      }
    })
  },
  upload: function (page, path) {
    var self = this;
    self.data.userInfo.customizedNickName = self.data.customizedNickName;
    wx.showToast({
      icon: "loading",
      title: "正在上传",
      duration: 10000
    }),
      wx.uploadFile({
        url: self.data.host + '/api/faces/' + self.data.userInfo.unionId,
        filePath: path[0],
        name: 'file',
        formData: {
          'profile': JSON.stringify(self.data.userInfo)
        },
        header: { "Content-Type": "multipart/form-data" },
        success: function (res) {
          if (res.statusCode === 200) {

            wx.showModal({
              title: '提示',
              content: '上传成功！快到人脸识别区域试试吧~',
              showCancel: false
            })
            self.setData({
              customizedNickName: ''
            })

          } else if (res.statusCode === 401) {
            wx.showModal({
              title: '提示',
              content: '照片不符合要求，请重新上传清晰的单人正面照片~',
              showCancel: false
            })
          } else {
            console.log(res);
            wx.showModal({
              title: '提示',
              content: 'Oops，上传失败！请稍后再试~',
              showCancel: false
            })
          }
        },
        fail: function (e) {
          console.log(e);
          wx.showModal({
            title: '提示',
            content: 'Oops，上传失败！请稍后再试~',
            showCancel: false
          })
        },
        complete: function () {
          wx.hideToast();  //隐藏Toast
        }
      })
  },

  saveFormId1: function (e) {
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
          console.log("Save data successfully")
        },
        fail:function(err){
          console.log("saveFormId(upload) error:" + JSON.stringify(err))
        }
      })
    }
  },


})