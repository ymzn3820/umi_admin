
export const crudOptions = (vm) => {
  // util.filterParams(vm, ['dept_name', 'role_info{name}', 'dept_name_all'])
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      rowKey: 'prod_id',
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
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: 'ID',
        key: 'id',
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: '商品ID',
        key: 'prod_id',
        search: {
          disabled: false
        },
        minWidth: 130,
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入商品ID'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '商品名',
        key: 'prod_name',
        minWidth: 90,
        type: 'input',
        search: {
          disabled: false
        },
        form: {
          editDisabled: false,
          component: {
            placeholder: '请输入商品名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
        // disabled: true
      },
      {
        title: '平台',
        key: 'platform',
        // sortable: 'custom',
        minWidth: 100,
        search: {
          disabled: false
        },
        type: 'radio',
        dict: {
          data: vm.dictionary('prod_platform')
        },
        form: {
          component: {
            span: 12,
            placeholder: '请选择平台'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '商品描述',
        key: 'prod_description',
        search: {
          disabled: true
        },
        minWidth: 70,
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入商品描述',
            span: 12,
            pagination: true,
            props: { multiple: false }
          }
        }
      },
      {
        title: '商品详情',
        key: 'prod_details',
        search: {
          disabled: true
        },
        minWidth: 180,
        form: {
          value: '',
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入商品详情，会员类产品描述请根据手册指导',
            span: 24
          }
        }
      },
      {
        title: '商品原价',
        key: 'prod_origin_price',
        minWidth: 110,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入商品原价， 浮点数',
            clearable: true

          }
        }
      }, {
        title: '连续订阅价格',
        key: 'continuous_annual_sub_price',
        minWidth: 100,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            placeholder: '请输入连续订阅价格， 浮点数'

          }
        }
      },
      {
        title: '商品价格',
        key: 'prod_price',
        width: 150,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入商品现价价格， 浮点数'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '有效期',
        key: 'valid_period_days',
        width: 150,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入有效天数'
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '商品类别',
        key: 'prod_cate_id',
        width: 150,
        type: 'input',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入商品类别'
          }
        }
      },
      {
        title: '商品状态',
        search: {
          disabled: false
        },
        key: 'is_delete',
        width: 150,
        type: 'radio',
        dict: {
          data: vm.dictionary('is_delete')
        },
        form: {
          disabled: true,
          component: {
            value: false,
            placeholder: '请选择商品状态'
          }
        }
      },
      {
        title: '是否展示',
        search: {
          disabled: false
        },
        key: 'is_show',
        width: 150,
        type: 'radio',
        dict: {
          data: vm.dictionary('is_show')
        },
        form: {
          disabled: false,
          component: {
            value: false,
            placeholder: '请选择商品展示状态'
          }
        }
      },
      {
        title: '创建时间',
        key: 'created_at',
        width: 150,
        type: 'input',
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
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        }
      }
    ]
  }
}
