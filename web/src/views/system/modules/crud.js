import * as apiIndustry from '../industry/api'
import { request } from '@/api/service'

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    keys: {},
    options: {
      height: '100%',
      rowKey: 'module_id',
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
        title: '模块ID',
        key: 'module_id',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入模块ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '行业ID',
        key: 'industry_id',
        minWidth: 90,
        type: 'select',
        show: false,

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
        key: 'occu_id',
        minWidth: 90,
        type: 'select',
        show: false,
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
        minWidth: 90,
        type: 'select',
        show: false,
        dict: {
          label: 'name',
          value: 'sub_occu_id',
          cache: false,
          url: '/api/system/sec_occupation/',
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { occu_id: form.occu_id, is_hidden: 0, is_delete: 0 } }).then(ret => {
              const data = []
              // if ('occu_id' in vm.crud.keys && vm.crud.keys.occu_id !== undefined) {
              //   vm.crud.keys.occu_id += ',' + form.occu_id
              // } else {
              //   vm.crud.keys.occu_id = form.occu_id
              // }
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
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            form.sub_occu_id = value // 将“city”的值置空
            // form.county = undefined// 将“county”的值置空

            if (value) {
              getComponent('emp_duration_id').reloadDict() // 执行city的select组件的reloadDict()方法，触发“city”重新加载字典
            }
          }
        }
      },
      {
        title: '从业时长ID',
        key: 'emp_duration_id',
        search: {
          disabled: false
        },
        show: false,
        minWidth: 130,
        type: 'select',
        dict: {
          label: 'emp_duration_name',
          value: 'emp_duration_id',
          cache: false,
          url: '/api/system/duration/',
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { sub_occu_id: form.sub_occu_id, is_hidden: 0, is_delete: 0 } }).then(ret => {
              const data = []
              // if ('sub_occu_id' in vm.crud.keys && vm.crud.keys.sub_occu_id !== undefined) {
              //   vm.crud.keys.sub_occu_id += ',' + form.sub_occu_id
              // } else {
              //   vm.crud.keys.sub_occu_id = form.sub_occu_id
              // }
              for (const item of ret.data.data) {
                const obj = {}
                obj.emp_duration_id = item.emp_duration_id
                obj.emp_duration_name = item.emp_duration_name
                data.push(obj)
              }
              return data
            })
          }
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入雇佣时长ID'
          },
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            form.emp_duration_id = value // 将“city”的值置空
            // form.county = undefined// 将“county”的值置空
            if (value) {
              getComponent('expertise_level_id').reloadDict() // 执行city的select组件的reloadDict()方法，触发“city”重新加载字典
            }
          }
        }
      },
      {
        title: '技能等级ID',
        key: 'expertise_level_id',
        search: {
          disabled: false
        },
        show: false,
        minWidth: 130,
        type: 'select',
        dict: {
          label: 'name',
          value: 'expertise_level_id',
          cache: false,
          url: '/api/system/expertise_level/',
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { emp_duration_id: form.emp_duration_id, is_hidden: 0, is_delete: 0 } }).then(ret => {
              const data = []
              // if ('emp_duration_id' in vm.crud.keys && vm.crud.keys.emp_duration_id !== undefined) {
              //   vm.crud.keys.emp_duration_id += ',' + form.emp_duration_id
              // } else {
              //   vm.crud.keys.emp_duration_id = form.emp_duration_id
              // }
              for (const item of ret.data.data) {
                const obj = {}
                obj.expertise_level_id = item.expertise_level_id
                obj.name = item.name
                data.push(obj)
              }
              return data
            })
          }
        },
        form: {
          disabled: false,
          component: {
            placeholder: '请输入技能等级ID'
          },
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
        title: '技能等级',
        key: 'expertise_level_name',
        search: {
          disabled: true
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入技能等级ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '名称',
        key: 'name',
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
        key: 'description',
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
        title: 'icon',
        key: 'icon',
        type: 'image-uploader',
        search: {
          disabled: true
        },
        minWidth: 300,
        form: {
          value: '',
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            props: {
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1 // 限制5个文件
              }
              // sizeLimit:  * 1024 // 不能超过限制
            },
            span: 24
          },
          helper: '更换新图片请将是否更新图片设置为【是】'
        }
      },
      {
        title: '联系客服二维码',
        key: 'contact_qr_code',
        type: 'image-uploader',
        search: {
          disabled: true
        },
        minWidth: 300,
        form: {
          value: '',
          // rules: [ // 表单校验规则
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            props: {
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1 // 限制5个文件
              }
              // sizeLimit:  * 1024 // 不能超过限制
            },
            span: 24
          },
          helper: '更换新图片请将是否更新图片设置为【是】'
        }
      },
      {
        title: '联系客服二维码描述',
        key: 'contact_qr_code_desc',
        type: 'input',
        search: {
          disabled: true
        },
        minWidth: 300,
        form: {
          value: '',
          // rules: [ // 表单校验规则
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            props: {
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1 // 限制5个文件
              }
              // sizeLimit:  * 1024 // 不能超过限制
            },
            span: 24
          },
          helper: '更换新图片请将是否更新图片设置为【是】'
        }
      },
      {
        title: '兴趣群二维码',
        key: 'interest_group',
        type: 'image-uploader',
        search: {
          disabled: true
        },
        minWidth: 300,
        form: {
          value: '',
          // rules: [ // 表单校验规则
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            props: {
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1 // 限制5个文件
              }
              // sizeLimit:  * 1024 // 不能超过限制
            },
            span: 24
          },
          helper: '更换新图片请将是否更新图片设置为【是】'
        }
      },
      {
        title: '兴趣群二维码描述',
        key: 'interest_group_desc',
        type: 'input',
        search: {
          disabled: true
        },
        minWidth: 300,
        form: {
          value: '',
          // rules: [ // 表单校验规则
          //   {
          //     required: true,
          //     message: '必填项'
          //   }
          // ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            props: {
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1 // 限制5个文件
              }
              // sizeLimit:  * 1024 // 不能超过限制
            },
            span: 24
          },
          helper: '更换新图片请将是否更新图片设置为【是】'
        }
      },

      {
        title: '文件夹',
        show: false,
        key: 'cate',
        // width: 150,
        // type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          editDisabled: false,
          value: 'icon',
          component: {
            placeholder: '请输入上传至文件夹名称',
            disabled: true // 禁用输入框

          }
          // helper: '如果不涉及图片更新，此处可不更改'

        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '是否更新图片',
        show: false,
        key: 'is_update_icon',
        // width: 150,
        type: 'select',
        dict: {
          data: [{ value: '1', label: '是', color: 'success' }, { value: '0', label: '否', color: 'danger' }]
        },
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          value: '0',
          disabled: false,
          component: {
            placeholder: '请选择是否涉及到更新ICON'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '是否隐藏',
        show: true,
        key: 'is_hidden',
        // width: 150,
        type: 'select',
        dict: {
          data: [{ value: true, label: '是', color: 'success' }, { value: false, label: '否', color: 'danger' }]
        },
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          value: false,
          disabled: false,
          component: {
            span: 24,
            props: {
              elProps: {
                allowCreate: true,
                filterable: true,
                clearable: true
              }

            }
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
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
