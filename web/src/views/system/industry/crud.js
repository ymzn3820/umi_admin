import * as apiIndustry from "@/views/system/industry/api";
import {request} from "@/api/service";

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'id',
      rowId: 'industry_id'
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
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: {
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      // {
      //   title: 'TabID',
      //   key: 'tab_id',
      //   minWidth: 90,
      //   type: 'select',
      //   show: false,
      //   dict: {
      //     label: 'name',
      //     value: 'tab_id',
      //     cache: false,
      //     url: '/api/system/tab_dict/',
      //     getData: (url, dict, { form, component }) => {
      //       return request({ url: url, params: { is_hidden: 0, is_delete: 0 } }).then(ret => {
      //         const data = []
      //
      //         for (const item of ret.data.data) {
      //           const obj = {}
      //           obj.tab_id = item.tab_id
      //           obj.name = item.name
      //           data.push(obj)
      //         }
      //         console.log(data)
      //         return data
      //       })
      //     }
      //   },
      //   search: {
      //     disabled: false
      //   },
      //   form: {
      //     component: {
      //       placeholder: '请选择Tab'
      //     },
      //     rules: [
      //       {
      //         required: true,
      //         message: '必填项'
      //       }
      //     ],
      //     itemProps: {
      //       class: { yxtInput: true }
      //     }
      //   }
      // },
      {
        title: '行业ID',
        key: 'industry_id',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入行业id'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '名称',
        key: 'name',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          component: {
            placeholder: '请输入名称'
          },
          rules: [
            {
              required: true,
              message: '必填项'
            }
          ],
          editDisabled: false,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '描述',
        key: 'description',
        minWidth: 160,
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
            placeholder: '请输入描述'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: 'NAICS代码',
        key: 'naics_code',
        search: {
          disabled: true
        },
        minWidth: 100,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入NAICS代码',
            clearable: true
          }
        }
      },
      {
        title: 'SIC代码',
        key: 'sic_code',
        search: {
          disabled: true
        },
        minWidth: 90,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入SIC代码',
            clearable: true
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

