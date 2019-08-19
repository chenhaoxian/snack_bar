<template>
  <div class="lucky-draw">
    <h2>抽奖管理</h2>
    <el-card class="box-card" style="width: 50%;margin: 10px auto;">
      <div class="auto-complete">
        查询：
        <el-autocomplete
          v-model="keyWord"
          :fetch-suggestions="querySearch"
          placeholder="请输入用户名"
          @select="handleSelect">
          <i class="el-icon-search el-input__icon" style="cursor: pointer;" slot="suffix" @click="handleIconClick(keyWord)"></i>
        </el-autocomplete>
      </div>
      <hr style="width: 99%;border: 1px solid #ccc;">
      <el-table :data="records" stripe align="left" style="width: 100%;">
        <el-table-column prop="create_date" sortable label="日期" width="180"></el-table-column>
        <el-table-column prop="prize.prizeName" sortable label="奖品名" width="180"></el-table-column>
        <el-table-column prop="user_info.nickName" sortable label="用户"></el-table-column>
        <el-table-column prop="is_redeem" label="操作" :filters="filterActions" :filter-method="filterTag">
          <template slot-scope="scope">
            <el-button type="info" v-if="scope.row.is_redeem" plain>已兑奖</el-button>
            <el-button type="primary" @click="expiry(scope.row)" v-else plain>兑奖</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
  import moment from 'moment'
  import Util from '../../utils/utils';

  export default {
    name: 'LuckyDraw',
    data () {
      return {
        user: Util.getCookie('user'),
        records: [],
        filterUsers: [],
        filterActions: [{ text: '已兑奖', value: true }, { text: '兑奖', value: false }],
        keyWord: ''
      }
    },
    methods: {
      initList() {
        var self = this;
        this.$http.get('/api/luckydraw/prize', {})
          .then(response => {
            self.records = self.formatRecords(response.data);
            this.filterUsers = this.getFilterUsers(response.data);
          })
          .catch(error => {
            console.log(error)
            this.errored = true
          });
      },
      expiry(record) {
        this.$http.post('/api/luckydraw/prize', { id: record.id })
          .then(response => {
            record.is_redeem = true;
          })
          .catch(error => {
            console.log(error)
            this.errored = true
          });
      },
      formatRecords(records){
        return records.map(record=>{
          record.create_date = moment.utc(record.create_date,'YYYY-MM-DD HH:mm:ss').local().format('YYYY-MM-DD HH:mm');
          return record;
        })
      },
      filterTag(value, row) {
        return row.is_redeem === value;
      },
      getFilterUsers: function (prizeList) {
        var users = [];
        var userNames = [];
        prizeList.forEach(prize=> {
          if (userNames.indexOf(prize.user_info.nickName) === -1) {
            var user = {};
            user.text = prize.user_info.nickName;
            user.value = prize.user_info.nickName;
            users.push(user);
            userNames.push(prize.user_info.nickName);
          }
        });
        return users;
      },
      querySearch(queryString, cb) {
        var users = this.filterUsers;
        var results = queryString ? users.filter(this.createFilter(queryString)) : users;
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },
      handleSelect(item) {
        if (item) {
          this.records = this.records.filter(record=> {
            return record.user_info.nickName === item.value;
          });
        } else {
          this.initList();
        }
      },
      handleIconClick(key){
        if (key) {
          this.records = this.records.filter(record=> {
            return record.user_info.nickName === key;
          });
        } else {
          this.initList();
        }
      }
    },
    mounted(){
      this.$nextTick(function () {
        this.initList();
        if(!this.user){
          window.location.replace('/')
        }
      })
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .auto-complete {
    float: left;
    margin: 0 auto 15px 10px;
    font-weight: bold;
    font-size: medium;
    color: #808080;
  }
</style>
