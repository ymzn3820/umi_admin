<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @AssignCustomer="AssignCustomer"

    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button
            size="small"
            v-permission="'Create'"
            type="primary"
            @click="addRow"
          >
            <i class="el-icon-plus" /> 新增
          </el-button>
          <el-button
            size="small"
            type="warning"
            @click="onExport"
            v-permission="'Export'"
            ><i class="el-icon-download" /> 导出
          </el-button>
          <importExcel
            api="api/system/user/"
            v-permission="'Import'"
            >导入
          </importExcel>
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
    </d2-crud-x>
    <el-dialog
      title="分配至销售人员"
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
      width="30%"
    >
    <el-select v-model="value" filterable placeholder="请选择">
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="doSubmit">确 认</el-button>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import { saveAs } from 'file-saver'
import * as xlxs from 'xlsx'

export default {
  name: 'dhSecretCard',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      tableRow: null,
      dialogFormVisible: false,
      assignCustomerForm: {
        id: null,
        seller_name: null
      },
      submitData: {
        seller_name: '',
        key_id: ''
      },
      options: [],
      value: ''
    }
  },
  methods: {
    getCrudOptions () {
      this.crud.searchOptions.form.user_type = 0
      this.crud.searchOptions.form.is_delete = false
      this.crud.searchOptions.form.user_name = this.$store.state.d2admin.user.info.name
      this.crud.searchOptions.form.user_id = this.$store.state.d2admin.user.info.id
      return crudOptions(this)
    },
    pageRequest (query) {
      return api.GetList(query)
    },
    addRequest (row) {
      return api.AddObj(row)
    },
    updateRequest (row) {
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row)
    },
    batchDelRequest (ids) {
      return api.BatchDel(ids)
    },
    AssignCustomer (row) {
      this.dialogFormVisible = true
      this.assignCustomerForm.id = row.id
      this.tableRow = row
      this.GetDeptEmployee()
    },
    GetDeptEmployee () {
      api.GetDeptEmployee().then(res => {
        this.options = res.data
      }
      )
    },
    doSubmit () {
      this.$confirm('是否确认分配?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log(this.assignCustomerForm)
        this.submitData.seller_name = this.value
        this.submitData.key_id = this.tableRow.row.key_id
        api.AssignCustomer(this.submitData)
        this.dialogFormVisible = false
        this.doRefresh()
        // location.reload()
      })
    },
    exportData () {
      const data = this.crud.list
      const wb = xlxs.utils.book_new()
      const ws = xlxs.utils.json_to_sheet(data)
      xlxs.utils.book_append_sheet(wb, ws, 'Sheet1')
      const wbout = xlxs.write(wb, { bookType: 'xlsx', type: 'array' })
      saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '支付管理.xlsx')
    },
    onExport () {
      this.$confirm('是否确认导出当前页数据项?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.exportData()
      })
    }
  }
}
</script>

<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>
