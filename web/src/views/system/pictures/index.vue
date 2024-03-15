<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @copyToClipboard="copyToClipboard"
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
          <el-button size="small" type="danger" @click="batchDelete">
            <i class="el-icon-delete"></i> 批量删除
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
      <span slot="PaginationPrefixSlot" class="prefix">
        <el-button
          class="square"
          size="mini"
          title="批量删除"
          @click="batchDelete"
          icon="el-icon-delete"
          :disabled="!multipleSelection || multipleSelection.length == 0"
        />
      </span>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
export default {
  name: 'pictures',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      dialogFormVisible: false,
      resetPwdForm: {
        id: null,
        pwd: null,
        pwd2: null
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
      return api.DelObj(row.pic_id)
    },
    batchDelRequest (ids) {
      return api.BatchDel(ids)
    },
    copyToClipboard (row) {
      const textarea = document.createElement('textarea')

      // 检查对象名称是否为中文
      const isChinese = /[\u3400-\u9FBF]/.test(row.row.name)

      // 如果是中文，则进行转义
      textarea.value = isChinese ? escape(row.row.pic_url) : row.row.pic_url

      textarea.style.position = 'fixed' // 防止页面滚动
      document.body.appendChild(textarea)
      textarea.focus()
      textarea.select()

      try {
        document.execCommand('copy')
        this.$message.success('分享成功, 地址已复制到剪贴板, 使用ctrl + v 粘贴至本地')
      } catch (err) {
        this.$message.error('分享成功, 但地址复制失败')
      }

      document.body.removeChild(textarea)
    },

    onExport () {
      const that = this
      this.$confirm('是否确认导出所有数据项?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        const query = that.getSearch().getForm()
        return api.exportData({ ...query })
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
