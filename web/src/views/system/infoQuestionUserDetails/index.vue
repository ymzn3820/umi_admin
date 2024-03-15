<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners">
      <template v-slot:character_avatarSlot="scope">
          <a :href="getAvatarUrl(scope.row.character_avatar)" target="_blank" v-if="scope.row.character_avatar && scope.row.character_avatar.startsWith('/static')">
            <img :src="getAvatarUrl(scope.row.character_avatar)" alt="角色头像" style="width: 100px; height: auto;" />
          </a>
      </template>

      <template v-slot:related_documentSlot="scope">
        <el-button type="text" @click="GetDocumentsQuery(scope.row.question_id)" class="details-button">查看详情</el-button>
        <el-dialog :append-to-body="true" title="文件列表" :visible.sync="dialogFormVisible">
          <el-table :data="files" style="width: 100%;">
            <el-table-column property="file_name" label="文件名称" width="250"></el-table-column>
            <el-table-column property="file_type" label="文件类型" width="250"></el-table-column>
            <el-table-column label="文件地址" width="400">
              <template v-slot="{ row }">
                <a :href="row.file_url" target="_blank" class="file-url-link">{{ row.file_url }}</a>
              </template>
            </el-table-column>
            <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
          </el-table>
          <div slot="footer" class="dialog-footer">
            <el-button type="default" @click="dialogFormVisible = false" class="cancel-button">取 消</el-button>
            <el-button type="primary" @click="dialogFormVisible = false" class="confirm-button">确 定</el-button>
          </div>
        </el-dialog>
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
import { GetDocuments } from './api'

export default {
  name: 'infoQuestionUserDetails',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      files: [],
      dialogTableVisible: false,
      dialogFormVisible: false
    }
  },
  methods: {
    getCrudOptions () {
      this.crud.searchOptions.form.user_type = 0
      this.crud.searchOptions.form.is_delete = 0
      this.crud.searchOptions.form.is_backend = 1
      return crudOptions(this)
    },
    getAvatarUrl (url) {
      if (url.startsWith('/static')) {
        return `https://umi-intelligence.oss-cn-shenzhen.aliyuncs.com${url}`
      }
      return url
    },
    GetDocumentsQuery (questionId) {
      this.dialogFormVisible = true
      console.log(questionId)
      GetDocuments(questionId).then(response => {
        this.files = response.data
        return this.files
      }
      )
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
.details-button {
  color: #007BFF;
}
.file-url-link {
  color: #007BFF;
  text-decoration: underline;
  font-weight: bold;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;

  .cancel-button {
    color: #6c757d;
  }

  .confirm-button {
    color: #fff;
    background-color: #007BFF;
    border-color: #007BFF;
  }
}

</style>
