import * as apiOiInfoTypes from './api'
import { request } from '@/api/service'

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'info_type_id',
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
        key: 'info_type_id',
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入信息类型ID'
          }
        }
      },
      {
        title: '附加类型名称',
        key: 'info_type_name',
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入信息类型名称'
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
        title: '附加类型中文',
        key: 'info_type_name_cn',
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入附加类型中文'
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
        search: {
          disabled: false
        },
        dict: {
          data: vm.dictionary('button_whether_bool')
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
