import * as apiIndustry from '../industry/api'
import * as apiOccupation from '../occupation/api'
import * as apiSubOccupation from '../secOccupation/api'
import { request } from '@/api/service' // Assuming you have a separate API for sub-occupations

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'emp_duration_id',
      rowId: 'id'
    },
    selectionRow: {
      align: 'center',
      width: 46
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
        title: '雇佣时长ID',
        key: 'emp_duration_id',
        show: true,
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入雇佣时长ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '行业ID',
        key: 'industry_id',
        show: false,
        minWidth: 90,
        type: 'select',
        dict: {
          label: 'name',
          value: 'industry_id',
          cache: false,
          getData: (url, dict, { form, component }) => {
            return apiIndustry.GetList().then(ret => { return ret.data.industry_maps })
          }
        },
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入行业ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            form.industry_id = value // 将“city”的值置空
            // form.county = undefined// 将“county”的值置空
            if (value) {
              getComponent('occu_id').reloadDict() // 执行city的select组件的reloadDict()方法，触发“city”重新加载字典
            }
          }
        }
      },
      {
        title: '职业ID',
        show: false,
        key: 'occu_id',
        minWidth: 90,
        type: 'select',
        dict: {
          label: 'name',
          value: 'occu_id',
          cache: false,
          url: '/api/system/occupation/',
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { industry_id: form.industry_id, is_hidden: 0, is_delete: 0 } }).then(ret => {
              const data = []

              for (const item of ret.data.data) {
                const obj = {}
                obj.occu_id = item.occu_id
                obj.name = item.name
                data.push(obj)
              }
              return data
            })
          }
        },
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入职业ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            form.occu_id = value // 将“city”的值置空
            // form.county = undefined// 将“county”的值置空
            if (value) {
              getComponent('sub_occu_id').reloadDict() // 执行city的select组件的reloadDict()方法，触发“city”重新加载字典
            }
          }
        }
      },
      {
        title: '次级职业ID',
        key: 'sub_occu_id',
        show: false,
        minWidth: 90,
        type: 'select',
        dict: {
          label: 'name',
          value: 'sub_occu_id',
          cache: false,
          url: '/api/system/sec_occupation/',
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { occu_id: form.occu_id, is_hidden: 0, is_delete: 0 } }).then(ret => {
              const data = []
              for (const item of ret.data.data) {
                const obj = {}
                obj.name = item.name
                obj.sub_occu_id = item.sub_occu_id
                data.push(obj)
              }
              return data
            })
          }
        },
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入次级职业ID',
            props: { color: 'auto' }
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '行业',
        key: 'industry_name',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入行业ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '职业',
        key: 'occu_name',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: true,

          component: {
            placeholder: '请输入职业ID'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '次级职业',
        key: 'sub_occu_name',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: true
        },
        form: {
          disabled: true,

          component: {
            placeholder: '请输入次级职业ID',
            props: { color: 'auto' }
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '从业时长',
        key: 'emp_duration_name',
        search: {
          disabled: true
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入雇佣时长ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '名称',
        key: 'emp_duration_name',
        minWidth: 70,
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            span: 12,
            placeholder: '请输入名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '描述',
        key: 'emp_duration_desc',
        search: {
          disabled: true
        },
        minWidth: 70,
        type: 'input',
        form: {
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            props: { multiple: false }
          }
        }
      },
      {
        title: '是否删除',
        search: {
          disabled: false
        },
        key: 'is_delete',
        type: 'radio',
        width: 70,
        dict: {
          data: vm.dictionary('is_delete')
        },
        form: {
          disabled: true,
          value: false,
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            value: false
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '创建时间',
        key: 'created_at',
        width: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '更新时间',
        key: 'updated_at',
        width: 150,
        type: 'datetime',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }
    ]
  }
}
