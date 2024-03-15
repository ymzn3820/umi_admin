export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      rowKey: 'id',
      rowId: 'tab_id'
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
    // indexRow: {
    //   title: '序号',
    //   align: 'center',
    //   width: 60
    // },
    columns: [
      {
        title: '序号',
        key: 'weight',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '栏目ID',
        key: 'tab_id',
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
      },
      // {
      //   title: 'icon',
      //   key: 'icon',
      //   type: 'image-uploader',
      //   search: {
      //     disabled: true
      //   },
      //   form: {
      //     rules: [
      //       {
      //         required: true,
      //         message: '必填项'
      //       }
      //     ],
      //     component: {
      //       span: 12,
      //       placeholder: '请上传图片'
      //     },
      //     itemProps: {
      //       class: { yxtInput: true }
      //     }
      //   },
      //   minWidth: 300
      // },
      {
        title: '上传者',
        key: 'uploader_id',
        minWidth: 100,
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          editDisabled: true,
          value: vm.$store.state.d2admin.user.info.name,
          component: {
            span: 12,
            placeholder: '请输入上传者ID',
            disabled: true // 禁用输入框

          }
        }
      },
      // {
      //   title: '文件夹',
      //   show: false,
      //   key: 'cate',
      //   // width: 150,
      //   // type: 'input',
      //   form: {
      //     rules: [
      //       {
      //         required: true,
      //         message: '必填项'
      //       }
      //     ],
      //     itemProps: {
      //       class: { yxtInput: true }
      //     },
      //     disabled: false,
      //     component: {
      //       placeholder: '请输入上传至文件夹名称'
      //     },
      //     helper: '如果不涉及图片更新，此处可不填'
      //
      //   },
      //   component: { props: { color: 'auto' } } // 自动染色
      // },
      // {
      //   title: '是否更新图片',
      //   show: false,
      //   key: 'is_update_icon',
      //   // width: 150,
      //   type: 'select',
      //   dict: {
      //     data: [{ value: '1', label: '是', color: 'success' }, { value: '0', label: '否', color: 'danger' }]
      //   },
      //   form: {
      //     rules: [
      //       {
      //         required: true,
      //         message: '必填项'
      //       }
      //     ],
      //     itemProps: {
      //       class: { yxtInput: true }
      //     },
      //     disabled: false,
      //     component: {
      //       placeholder: '请选择是否涉及到更新图片'
      //     }
      //   },
      //   component: { props: { color: 'auto' } } // 自动染色
      // }
    ]
  }
}
