import * as apiOioInfoOptions from './api'
import { request } from '@/api/service'

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'option_id',
      rowId: 'id'
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
      defaultSpan: 12 // default form span
    },
    indexRow: {
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: '附加类型ID',
        key: 'option_id',
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入选项ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '附加类型名称',
        key: 'info_type_id',
        type: 'select',
        dict: {
          label: 'info_type_name',
          value: 'info_type_id',
          cache: false,
          url: '/api/system/info_type_dict/'
        },
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入附加类型名称',
            props: {
              clearable: true,
              filterable: true // 可过滤选择项
            }
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '附加类型内容',
        key: 'option_value',
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入附加类型内容',
            props: {
              clearable: true,
              filterable: true // 可过滤选择项
            }
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '是否删除',
        key: 'is_delete',
        type: 'select',
        dict: {
          data: vm.dictionary('button_whether_bool')
        },
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请选择是否删除'
          },
          value: false,
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ]
        }
      },
      {
        title: '创建时间',
        key: 'created_at',
        type: 'datetime',
        form: {
          disabled: true
        },
        component: {
          disabled: true
        }
      },
      {
        title: '更新时间',
        key: 'updated_at',
        type: 'datetime',
        form: {
          disabled: true
        },
        component: {
          disabled: true
        }
      }
    ]
  }
}
