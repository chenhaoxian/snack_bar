<template>
  <div class="products">

    <h2 style="text-align: center;">物品管理</h2>
    <el-form :rules="rules" ref="productForm" :model="productForm" label-width="80px" class="prod-form">
      <el-form-item label="购买地点" prop="location" required>
        <el-radio-group v-model="productForm.location">
          <el-radio label="Phase 3">三期</el-radio>
          <el-radio label="Phase 2">二期</el-radio>
          <el-radio label="Phase 1">一期</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="物品名称" prop="name" required>
        <el-input v-model="productForm.name"></el-input>
      </el-form-item>
      <el-form-item label="物品条码" prop="code" required>
        <el-input v-model="productForm.code"></el-input>
      </el-form-item>
      <el-form-item label="物品单价" prop="price" required>
        <el-input v-model.number="productForm.price"></el-input>
      </el-form-item>
      <el-form-item style="text-align: center;">
        <el-button type="primary" @click="addSnack('productForm')">保存</el-button>
        <el-button @click="resetForm('productForm')">重置</el-button>
      </el-form-item>
    </el-form>

    <hr style="width: 99%;border: 1px solid #ccc;">

    <el-card class="box-card" style="width: 70%;margin: 10px auto;">
      <el-table :data="productsData" stripe style="width: 100%;" align="left">
        <el-table-column prop="snack_name" label="物品名称" width="180"></el-table-column>
        <el-table-column prop="snack_code" label="物品条码" width="180"></el-table-column>
        <el-table-column prop="snack_price" sortable label="单价"></el-table-column>
        <el-table-column prop="location" label="地点" :filters="filterLocation"
                         :filter-method="filterHandler"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" @click="editProduct(scope.row)" circle></el-button>
            <el-button type="danger" icon="el-icon-delete" @click="delProduct(scope.row, scope.$index)" circle></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <br>
    <br>
  </div>
</template>

<script>
  import Util from '../../utils/utils'

  export default {
    name: 'Products',
    data () {
      return {
        user: Util.getCookie('user'),
        productForm: { location: 'Phase 3', name: '', code: '', price: '' },
        productsData: [],
        rules: {
          name: [
            { required: true, message: '请输入物品名称', trigger: 'blur' },
            { min: 2, message: '长度至少为2 ', trigger: 'blur' }
          ],
          code: [
            { required: true, message: '请输入Bar Code', trigger: 'blur' }
          ],
          price: [{ required: true, message: '单价不能为空' }, { type: 'number', message: '单价必须为数字值' }]
        },
        filterLocation: [{ text: 'Phase 3', value: 'Phase 3' }, { text: 'Phase 2', value: 'Phase 2' }, { text: 'Phase 1', value: 'Phase 1' }]
      }
    },
    methods: {
      initList: function () {
        var self = this;
        this.$http.get('/api/snack', {})
          .then(response => {
            self.productsData = response.data
          })
          .catch(error => {
            console.log(error)
            this.errored = true
          });
      },
      addSnack: function (formName) {
        var self = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            var prod = {
              location: self.productForm.location,
              snack_name: self.productForm.name,
              snack_code: self.productForm.code,
              snack_price: self.productForm.price,
            };
            if (self.productForm.id) {
              prod.id = self.productForm.id;
            }
            this.$http.post('/api/snack', prod)
              .then((response) => {
                this.$refs[formName].resetFields();
                this.initList();
              })
              .catch((error)=> {
                console.log(error);
              });
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      editProduct: function (record) {
        this.productForm = {
          id: record.id,
          location: record.location,
          name: record.snack_name,
          code: record.snack_code,
          price: record.snack_price
        }
        scrollTo(0,0);
      },
      delProduct: function (record, index) {
        console.log(index)
        var self = this;
        this.$confirm('此操作将永久删除该物品, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          self.$http.post('/api/snack/' + record.id)
            .then(response => {
              self.productsData.splice(index, 1);
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            })
            .catch(error => {
              console.log(error)
              this.errored = true
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      filterHandler(value, row, column) {
        const property = column['property'];
        return row[property] === value;
      }
    },
    mounted(){
      this.$nextTick(function () {
        this.initList();
        if (!this.user) {
          window.location.replace('/')
        }
      })
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .prod-form {
    width: 500px;
    margin: 0px auto;
    text-align: left;
  }

</style>
