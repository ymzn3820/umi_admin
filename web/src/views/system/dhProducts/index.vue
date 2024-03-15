<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @PubSecretKey="PubSecretKey"

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
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import { saveAs } from 'file-saver'
import * as xlxs from 'xlsx'

export default {
  name: 'dhProducts',
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
      return api.DelObj(row)
    },
    batchDelRequest (ids) {
      return api.BatchDel(ids)
    },
    copyToClipboard (text) {
      const textarea = document.createElement('textarea')
      textarea.value = text
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

    PubSecretKey (row) {
      const sharedUserId = this.$store.state.d2admin.user.info.id
      const shareURL = 'https://www.umi6.com/card.html?share_id=' + sharedUserId

      this.$confirm('是否确认分享?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const shareUrlObject = { shareUrl: shareURL }
        api.GetShortUrl(shareUrlObject).then(res => {
          const shortURL = res.data.short_url
          const clipboardContent = `分享链接: ${shortURL}\n 如果打不开请点击原始链接: ${shareURL}`

          // 检查浏览器是否支持Clipboard API
          if (navigator.clipboard) {
            navigator.clipboard.writeText(clipboardContent).then(() => {
              this.$message.success('分享成功, 地址已复制到剪贴板, 使用ctrl + v 粘贴至本地')
            }).catch(err => {
              console.error('复制失败: ', err)
              this.$message.error('分享成功, 但地址复制失败')
            })
          } else {
            this.copyToClipboard(clipboardContent)
          }
        })
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
