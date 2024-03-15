<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners">
      <template v-slot:weight_slot="scope">
         <span @click="handleEdit(scope.row)">
          {{ scope.row.weight }}
        </span>
      </template>

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
        <el-dialog
          title="编辑权重"
          :visible.sync="editDialogVisible"
          width="30%">
          <el-form :model="editForm">
            <el-form-item label="权重">
              <el-input v-model="editForm.weight" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="editDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="saveEdit">保 存</el-button>
          </span>
        </el-dialog>

        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import { saveAs } from 'file-saver'
import * as xlxs from 'xlsx'
import { UpdateWeight } from '@/views/system/infoQuestionUserDetails/api'

export default {
  name: 'tab',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      dialogFormVisible: false,
      resetPwdForm: {
        id: null,
        pwd: null,
        pwd2: null
      },
      editDialogVisible: false,
      editForm: {
        weight: 0
      }
    }
  },
  methods: {
    getCrudOptions () {
      this.crud.searchOptions.form.user_type = 0
      this.crud.searchOptions.form.is_delete = false
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
      return api.DelObj(row.tab_id)
    },
    batchDelRequest (ids) {
      return api.BatchDel(ids)
    },
    enableEditing (row) {
      this.$set(row, 'editing', true)
    },
    disableEditing (row) {
      console.log('Editing enabled for row:', row)

      this.$set(row, 'editing', false)
      // 在这里调用 API 更新数据
      this.updateWeight(row)
    },
    updateWeight (row) {
      // 调用 API 更新 weight 字段
      UpdateWeight(row.id, row.weight)
        .then(response => {
          // 成功处理
          this.$message.success('Weight updated successfully')
        })
        .catch(error => {
          // 错误处理
          console.error('Error updating weight:', error)
          this.$message.error('Failed to update weight')
        })
    },
    handleEdit (row) {
      this.editForm.weight = row.weight
      this.editDialogVisible = true
    },
    saveEdit (row) {
      UpdateWeight(row.id, row.weight)
        .then(response => {
          // 成功处理
          this.$message.success('Weight updated successfully')
        })
        .catch(error => {
          // 错误处理
          console.error('Error updating weight:', error)
          this.$message.error('Failed to update weight')
        })
      this.editDialogVisible = false
    }
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
</script>

<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>
