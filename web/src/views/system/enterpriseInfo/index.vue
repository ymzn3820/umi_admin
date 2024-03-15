<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners">
      <template v-slot:enterprise_projectSlot="scope">
        <el-button type="text" @click="showEnterpriseProjectDialog(scope.index)">查看企业项目详情</el-button>
        <el-dialog :append-to-body="true" title="企业项目详情列表" :visible.sync="enterpriseProjectDialogFormVisibles[scope.index]">
          <el-table :data="scope.row.enterprise_project" style="width: 100%;">
            <el-table-column property="brief_introduction" label="简介" width="250"></el-table-column>
            <el-table-column property="category_name" label="类型名称" width="250"></el-table-column>
            <el-table-column property="company_code" label="公司编号" width="250"></el-table-column>
            <el-table-column property="project_code" label="项目编号" width="250"></el-table-column>
            <el-table-column property="project_name" label="项目名称" width="250"></el-table-column>
            <el-table-column label="企业知识库包含文档内容" width="400">
                <template v-slot="{ row }">
                    <el-button type="text" @click="showEnterpriseInfoDocumentsDialog(row.index)">企业知识库包含文档内容内容</el-button>
                    <el-dialog :append-to-body="true" title="文档列表" :visible.sync="enterpriseInfoDocumentsDialogFormVisibles[row.index]">
                      <el-table :data="row.enterprise_documents" style="width: 100%;">
                        <el-table-column property="code" label="对应项目编号" width="250"></el-table-column>
                        <el-table-column property="file_category" label="文档分类" width="250"></el-table-column>
                        <el-table-column label="文件地址" width="400">
                          <template v-slot="{ row }">
                              <a :href="row.file_url" target="_blank" class="file-url-link">{{ row.file_url }}</a>
                          </template>
                        </el-table-column>
                        <el-table-column property="group_code" label="文件类型" width="250"></el-table-column>
                        <el-table-column property="create_by" label="创建人" width="250"></el-table-column>
                        <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
                        <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
                      </el-table>
                      <div slot="footer" class="dialog-footer">
                        <el-button type="default" @click="closeEnterpriseInfoDocumentsDialog(row.index)" class="cancel-button">取 消</el-button>
                        <el-button type="primary" @click="closeEnterpriseInfoDocumentsDialog(row.index)" class="confirm-button">确 定</el-button>
                      </div>
                    </el-dialog>
                </template>
            </el-table-column>
            <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
            <el-table-column property="is_delete" label="数据库状态" width="250"></el-table-column>
            <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
          </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button type="default" @click="closeEnterpriseProjectDialog(scope.index)" class="cancel-button">取 消</el-button>
          <el-button type="primary" @click="closeEnterpriseProjectDialog(scope.index)" class="confirm-button">确 定</el-button>
        </div>
        </el-dialog>
      </template>

      <template v-slot:enterprise_knowledge_baseSlot="scope">
        <el-button type="text" @click="showEnterpriseKnowledgeBaseDialog(scope.index)">查看企业知识库详情</el-button>
        <el-dialog :append-to-body="true" title="企业知识库详情列表" :visible.sync="enterpriseKnowledgeBaseDialogFormVisibles[scope.index]">
          <el-table :data="scope.row.enterprise_knowledge_base" style="width: 100%;">
            <el-table-column property="category" label="类型编号" width="250"></el-table-column>
            <el-table-column property="category_name" label="类型名称" width="250"></el-table-column>
            <el-table-column property="company_code" label="公司编号" width="250"></el-table-column>
            <el-table-column property="knowledge_code" label="知识库编号" width="250"></el-table-column>
            <el-table-column property="create_by" label="创建人" width="250"></el-table-column>
            <el-table-column label="企业知识库详情包含标签内容" width="400">
                <template v-slot="{ row }">
                    <el-button type="text" @click="showEnterpriseInfoLabelsDialog(row.index)">企业知识库详情包含标签内容</el-button>
                    <el-dialog :append-to-body="true" title="标签列表" :visible.sync="enterpriseInfoLabelsDialogFormVisibles[row.index]">
                      <el-table :data="row.enterprise_labels" style="width: 100%;">
                        <el-table-column property="label" label="标签" width="250"></el-table-column>
                        <el-table-column property="label_code" label="标签编号" width="250"></el-table-column>
                        <el-table-column property="label_type" label="标签类型" width="250"></el-table-column>
                        <el-table-column property="create_by" label="创建人" width="250"></el-table-column>
                        <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
                        <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
                      </el-table>
                      <div slot="footer" class="dialog-footer">
                        <el-button type="default" @click="closeEnterpriseInfoLabelsDialog(row.index)" class="cancel-button">取 消</el-button>
                        <el-button type="primary" @click="closeEnterpriseInfoLabelsDialog(row.index)" class="confirm-button">确 定</el-button>
                      </div>
                    </el-dialog>
                </template>
            </el-table-column>
            <el-table-column label="企业知识库包含文档内容" width="400">
                <template v-slot="{ row }">
                    <el-button type="text" @click="showEnterpriseInfoDocumentsDialog(row.index)">企业知识库包含文档内容</el-button>
                    <el-dialog :append-to-body="true" title="文档列表" :visible.sync="enterpriseInfoDocumentsDialogFormVisibles[row.index]">
                      <el-table :data="row.enterprise_documents" style="width: 100%;">
                        <el-table-column property="code" label="文档编号" width="250"></el-table-column>
                        <el-table-column property="file_category" label="文档分类" width="250"></el-table-column>
                        <el-table-column label="文件地址" width="400">
                          <template v-slot="{ row }">
                              <a :href="row.file_url" target="_blank" class="file-url-link">{{ row.file_url }}</a>
                          </template>
                        </el-table-column>
                        <el-table-column property="group_code" label="文件类型" width="250"></el-table-column>
                        <el-table-column property="create_by" label="创建人" width="250"></el-table-column>
                        <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
                        <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
                      </el-table>
                      <div slot="footer" class="dialog-footer">
                        <el-button type="default" @click="closeEnterpriseInfoDocumentsDialog(row.index)" class="cancel-button">取 消</el-button>
                        <el-button type="primary" @click="closeEnterpriseInfoDocumentsDialog(row.index)" class="confirm-button">确 定</el-button>
                      </div>
                    </el-dialog>
                </template>
            </el-table-column>
            <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
            <el-table-column property="is_delete" label="数据库状态" width="250"></el-table-column>
            <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
            <el-table-column property="purpose" label="作用" width="250"></el-table-column>
          </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button type="default" @click="closeEnterpriseKnowledgeBaseDialog(scope.index)" class="cancel-button">取 消</el-button>
          <el-button type="primary" @click="closeEnterpriseKnowledgeBaseDialog(scope.index)" class="confirm-button">确 定</el-button>
        </div>
        </el-dialog>
      </template>

      <template v-slot:enterprise_infoSlot="scope">
        <el-button type="text" @click="showEnterpriseInfoDialog(scope.index)">查看公司详情</el-button>
        <el-dialog :append-to-body="true" title="公司详情列表" :visible.sync="enterpriseInfoDialogFormVisibles[scope.index]">
          <el-table :data="scope.row.enterprise_info" style="width: 100%;">
            <el-table-column property="company_code" label="公司编号" width="250"></el-table-column>
            <el-table-column property="content_desc" label="公司描述" width="250"></el-table-column>
            <el-table-column property="create_by" label="创建人" width="250"></el-table-column>
            <el-table-column property="information_code" label="详情编号" width="250"></el-table-column>
            <el-table-column label="公司详情包含标签内容" width="400">
                <template v-slot="{ row }">
                    <el-button type="text" @click="showEnterpriseInfoLabelsDialog(row.index)">公司详情包含标签内容</el-button>
                    <el-dialog :append-to-body="true" title="标签列表" :visible.sync="enterpriseInfoLabelsDialogFormVisibles[row.index]">
                      <el-table :data="row.enterprise_labels" style="width: 100%;">
                        <el-table-column property="label" label="标签" width="250"></el-table-column>
                        <el-table-column property="label_code" label="标签编号" width="250"></el-table-column>
                        <el-table-column property="label_type" label="标签类型" width="250"></el-table-column>
                        <el-table-column property="create_by" label="创建人" width="250"></el-table-column>
                        <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
                        <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
                      </el-table>
                      <div slot="footer" class="dialog-footer">
                        <el-button type="default" @click="closeEnterpriseInfoLabelsDialog(row.index)" class="cancel-button">取 消</el-button>
                        <el-button type="primary" @click="closeEnterpriseInfoLabelsDialog(row.index)" class="confirm-button">确 定</el-button>
                      </div>
                    </el-dialog>
                </template>
            </el-table-column>
            <el-table-column label="公司详情包含文档内容" width="400">
                <template v-slot="{ row }">
                    <el-button type="text" @click="showEnterpriseInfoDocumentsDialog(row.index)">公司详情包含文档内容</el-button>
                    <el-dialog :append-to-body="true" title="文档列表" :visible.sync="enterpriseInfoDocumentsDialogFormVisibles[row.index]">
                      <el-table :data="row.enterprise_documents" style="width: 100%;">
                        <el-table-column property="code" label="文档编号" width="250"></el-table-column>
                        <el-table-column property="file_category" label="文档分类" width="250"></el-table-column>
                        <el-table-column label="文件地址" width="400">
                          <template v-slot="{ row }">
                              <a :href="row.file_url" target="_blank" class="file-url-link">{{ row.file_url }}</a>
                          </template>
                        </el-table-column>
                        <el-table-column property="group_code" label="文件类型" width="250"></el-table-column>
                        <el-table-column property="create_by" label="创建人" width="250"></el-table-column>
                        <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
                        <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
                      </el-table>
                      <div slot="footer" class="dialog-footer">
                        <el-button type="default" @click="closeEnterpriseInfoDocumentsDialog(row.index)" class="cancel-button">取 消</el-button>
                        <el-button type="primary" @click="closeEnterpriseInfoDocumentsDialog(row.index)" class="confirm-button">确 定</el-button>
                      </div>
                    </el-dialog>
                </template>
            </el-table-column>
            <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
            <el-table-column property="information_name" label="详情内容" width="250"></el-table-column>
            <el-table-column property="label_code" label="标签编号" width="250"></el-table-column>
            <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
          </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button type="default" @click="closeEnterpriseInfoDialog(scope.index)" class="cancel-button">取 消</el-button>
          <el-button type="primary" @click="closeEnterpriseInfoDialog(scope.index)" class="confirm-button">确 定</el-button>
        </div>
        </el-dialog>
      </template>

      <template v-slot:enterprise_labelsSlot="scope">
        <el-button type="text" @click="showEnterpriseLabelsDialog(scope.index)">查看公司标签详情</el-button>
        <el-dialog :append-to-body="true" title="公司标签详情列表" :visible.sync="enterpriseLabelsDialogFormVisibles[scope.index]">
          <el-table :data="scope.row.enterprise_labels" style="width: 100%;">
            <el-table-column property="label" label="标签" width="250"></el-table-column>
            <el-table-column property="label_code" label="标签编号" width="250"></el-table-column>
            <el-table-column property="create_by" label="创建人" width="250"></el-table-column>
            <el-table-column property="label_type" label="标签类型" width="250"></el-table-column>
            <el-table-column property="create_time" label="创建时间" width="250"></el-table-column>
            <el-table-column property="is_delete" label="数据库状态" width="250"></el-table-column>
            <el-table-column property="modify_time" label="最新修改时间" width="250"></el-table-column>
          </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button type="default" @click="closeEnterpriseLabelsDialog(scope.index)" class="cancel-button">取 消</el-button>
          <el-button type="primary" @click="closeEnterpriseLabelsDialog(scope.index)" class="confirm-button">确 定</el-button>
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

export default {
  name: 'enterpriseInfo',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      files: [],
      dialogTableVisible: false,
      enterpriseInfoDialogFormVisibles: [],
      enterpriseInfoLabelsDialogFormVisibles: [],
      enterpriseInfoDocumentsDialogFormVisibles: [],
      enterpriseKnowledgeBaseDialogFormVisibles: [],
      enterpriseProjectDialogFormVisibles: [],
      enterpriseLabelsDialogFormVisibles: [],
      labelDialogFormVisibles: [],
      enterpriseDialogFormVisibles: []
    }
  },
  methods: {
    getCrudOptions () {
      this.crud.searchOptions.form.user_type = 0
      this.crud.searchOptions.form.is_delete = 0
      this.crud.searchOptions.form.is_backend = 1
      return crudOptions(this)
    },
    showEnterpriseInfoDialog (index) {
      this.$set(this.enterpriseInfoDialogFormVisibles, index, true)
    },
    closeEnterpriseInfoDialog (index) {
      this.$set(this.enterpriseInfoDialogFormVisibles, index, false)
    },
    showEnterpriseInfoLabelsDialog (index) {
      this.$set(this.enterpriseInfoLabelsDialogFormVisibles, index, true)
    },
    closeEnterpriseInfoLabelsDialog (index) {
      this.$set(this.enterpriseInfoLabelsDialogFormVisibles, index, false)
    },
    showEnterpriseInfoDocumentsDialog (index) {
      this.$set(this.enterpriseInfoDocumentsDialogFormVisibles, index, true)
    },
    closeEnterpriseInfoDocumentsDialog (index) {
      this.$set(this.enterpriseInfoDocumentsDialogFormVisibles, index, false)
    },
    showEnterpriseKnowledgeBaseDialog (index) {
      this.$set(this.enterpriseKnowledgeBaseDialogFormVisibles, index, true)
    },
    closeEnterpriseKnowledgeBaseDialog (index) {
      this.$set(this.enterpriseKnowledgeBaseDialogFormVisibles, index, false)
    },
    showEnterpriseProjectDialog (index) {
      this.$set(this.enterpriseProjectDialogFormVisibles, index, true)
    },
    closeEnterpriseProjectDialog (index) {
      this.$set(this.enterpriseProjectDialogFormVisibles, index, false)
    },
    showEnterpriseLabelsDialog (index) {
      this.$set(this.enterpriseLabelsDialogFormVisibles, index, true)
    },
    closeEnterpriseLabelsDialog (index) {
      this.$set(this.enterpriseLabelsDialogFormVisibles, index, false)
    },
    getAvatarUrl (url) {
      if (url.startsWith('/static')) {
        return `https://umi-intelligence.oss-cn-shenzhen.aliyuncs.com${url}`
      }
      return url
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
