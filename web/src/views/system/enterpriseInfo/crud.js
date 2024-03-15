
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'company_code',
      rowId: 'company_code'
    },
    rowHandle: {
      width: 240,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12
    },
    indexRow: {
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: '公司编号',
        width: 170,
        key: 'company_code',
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          rules: [{ required: true, message: '请输入公司编号' }],
          component: {
            placeholder: '请输入公司编号',
            clearable: true

          }

        }
      },
      {
        title: '公司名称',
        width: 170,
        search: {
          disabled: false
        },
        key: 'company_name',
        type: 'input',
        form: {
          rules: [{ required: true, message: '请输入公司名称' }],
          component: {
            placeholder: '请输入公司名称',
            clearable: true

          }
        },
        component: {
          render (h, params) {
            const content = params.row.company_name.length > 30 ? params.row.company_name.substring(0, 30) + '...' : params.row.company_name
            return h('el-tooltip', {
              props: {
                content: params.row.company_name,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      },
      {
        title: '简称',
        key: 'company_abbreviation',
        type: 'input'
      },
      {
        title: '职位',
        key: 'position',
        type: 'input'
      },
      {
        title: '行业编号',
        key: 'industry_code',
        type: 'input'
      },
      {
        title: '注册地址',
        key: 'registered_address',
        type: 'input'
      },
      {
        title: '公司描述',
        width: 170,
        key: 'company_desc',
        type: 'textarea',
        component: {
          render (h, params) {
            const content = params.row.company_desc.length > 30 ? params.row.company_desc.substring(0, 30) + '...' : params.row.company_desc
            return h('el-tooltip', {
              props: {
                content: params.row.company_desc,
                placement: 'top'
              }
            }, [
              h('span', {}, content)
            ])
          }
        }
      },
      {
        title: '公司网址',
        key: 'company_url',
        type: 'input'
      },
      {
        title: 'ipc备案号',
        key: 'ipc_code',
        type: 'input'
      },
      {
        title: '公司电话',
        key: 'company_mobile',
        type: 'input'
      },
      {
        title: '公司邮箱',
        key: 'company_mailbox',
        type: 'input'
      },
      {
        title: '公司地址',
        key: 'company_address',
        type: 'input'
      },
      {
        title: '公司详情',
        width: 130,
        key: 'enterprise_info',
        type: 'input',
        rowSlot: true
      },
      {
        title: '企业知识库',
        width: 150,
        key: 'enterprise_knowledge_base',
        type: 'input',
        rowSlot: true
      },
      {
        title: '企业项目',
        width: 150,
        key: 'enterprise_project',
        type: 'input',
        rowSlot: true
      },
      {
        title: '企业标签',
        width: 150,
        key: 'enterprise_labels',
        type: 'input',
        rowSlot: true
      },
      {
        title: '状态',
        key: 'status',
        search: {
          disabled: false
        },
        type: 'radio',
        dict: {
          data: [
            { value: 1, label: '保存' },
            { value: 2, label: '提交' }
          ]
        }
      },
      {
        title: '创建人',
        width: 100,
        key: 'create_by',
        type: 'input',
        form: {
          disabled: true // 创建人可能由后端自动填充，所以在前端可能不允许编辑
        }
      },
      {
        title: '创建日期',
        width: 100,
        key: 'create_time',
        type: 'datetime',
        form: {
          disabled: true
        }
      },
      {
        title: '最近修改日期',
        width: 100,
        key: 'modify_time',
        type: 'datetime',
        form: {
          disabled: true
        }
      },
      {
        title: '是否删除',
        search: {
          disabled: false
        },
        key: 'is_delete',
        type: 'radio',
        dict: {
          data: [
            { value: 0, label: '正常' },
            { value: 1, label: '已删除' }
          ]
        }
      }
    ]
  }
}
