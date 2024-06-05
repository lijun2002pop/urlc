<template>
    <a-row>
      <a-col :span="6">
        <div class="add_host" style="margin: 15px;">
  
          <a-button @click="showHostModal" type="primary">
            新建
          </a-button>
          <a-button type="primary" style="margin-left: 20px;">
            批量导入
          </a-button>
        </div>
      </a-col>
  
    </a-row>
    <a-table bordered :dataSource="hostList.data" :columns="hostFormColumns">
      <template #bodyCell="{ column, text, record }">
        <template v-if="column.dataIndex === 'action'">
          <a-popconfirm
              v-if="hostList.data.length"
              title="Sure to delete?"
              @confirm="deleteHost(record)"
          >
            <a>Delete</a>
          </a-popconfirm>
        </template>
      </template>
  
    </a-table>
  
    <div>
  
      <a-modal v-model:open="hostFormVisible" title="添加主机" @ok="onHostFormSubmit" @cancel="resetForm()" :width="800">
        <a-form
            ref="formRef"
            name="custom-validation"
            :model="hostForm.form"
            :rules="hostForm.rules"
            v-bind="layout"
            @finish="handleFinish"
            @validate="handleValidate"
            @finishFailed="handleFinishFailed"
        >
          <a-form-item label="主机类别" prop="zone" name="category">
            <a-row>
              <a-col :span="12">
                <a-select
                    ref="select"
                    v-model:value="hostForm.form.category"
                    @change="handleCategorySelectChange"
  
                >
                  <a-select-option :value="category.id" v-for="category in categoryList.data" :key="category.id">
                    {{ category.name }}
                  </a-select-option>
                </a-select>
              </a-col>
              <a-col :span="12">
                <a-button @click="showHostCategoryFormModal" type="primary">
                    新建主机类别
                </a-button>
              </a-col>
  
            </a-row>
  
          </a-form-item>
  
          <a-form-item has-feedback label="主机名称" name="name">
            <a-input v-model:value="hostForm.form.name" type="text" autocomplete="off"/>
          </a-form-item>
  
  
          <a-form-item has-feedback label="连接地址" name="username">
  
            <a-row>
              <a-col :span="8">
                <a-input placeholder="用户名" addon-before="ssh" v-model:value="hostForm.form.username" type="text"
                         autocomplete="off"/>
              </a-col>
              <a-col :span="8">
                <a-input placeholder="ip地址" addon-before="@" v-model:value="hostForm.form.ip_addr" type="text"
                         autocomplete="off"/>
              </a-col>
              <a-col :span="8">
                <a-input placeholder="端口号" addon-before="-p" v-model:value="hostForm.form.port" type="text"
                         autocomplete="off"/>
              </a-col>
            </a-row>
          </a-form-item>
  
          <a-form-item has-feedback label="连接密码" name="password">
            <a-input v-model:value="hostForm.form.password" type="password" autocomplete="off"/>
          </a-form-item>
  
          <a-form-item has-feedback label="备注信息" name="remark">
            <a-textarea placeholder="请输入主机备注信息" v-model:value="hostForm.form.remark" type="text"
                        :auto-size="{ minRows: 3, maxRows: 5 }" autocomplete="off"/>
          </a-form-item>
  
  
          <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
            <a-button @click="resetForm">Reset</a-button>
          </a-form-item>
        </a-form>
  
  
      </a-modal>
      <a-modal
          :width="600"
          title="新建主机类别"
          :open="HostCategoryFromVisible"
          @cancel="hostCategoryFormCancel"
      >
        <template #footer>
          <a-button key="back" @click="hostCategoryFormCancel">取消</a-button>
          <a-button key="submit" type="primary" :loading="loading" @click="onHostCategoryFromSubmit">提交</a-button>
        </template>
        <a-form-model ref="hostCategoryRuleForm" v-model:value="hostCategoryForm.form" :rules="hostCategoryForm.rules"
                      :label-col="hostCategoryForm.labelCol" :wrapper-col="hostCategoryForm.wrapperCol">
          <a-form-model-item ref="name" label="类别名称" prop="name">
            <a-row>
              <a-col :span="24">
                <a-input placeholder="请输入主机类别名称" v-model:value="hostCategoryForm.form.name"/>
              </a-col>
            </a-row>
          </a-form-model-item>
        </a-form-model>
      </a-modal>
    </div>
  
  </template>
  <script>
  import {defineComponent, ref, reactive} from 'vue';
  import {message} from 'ant-design-vue';
  import axios from 'axios'
  import store from "@/store";
  export default {
    setup() {
  
      const handleChange = value => {
        console.log(`selected ${value}`);
      };
  
      const handleCategorySelectChange = (value) => {
        // 切换主机类别的回调处理
        console.log(value)
      };
  
  
      const formRef = ref();
      const HostCategoryFromVisible = ref(false);
      const hostList = reactive({
        data: [
          
        ]
      })
      const categoryList = reactive({
        data: [
        ]
      })
  
      const hostForm = reactive({
        labelCol: {span: 6},
        wrapperCol: {span: 14},
        other: '',
        form: {
          name: '',
          category: "",
          ip_addr: '',
          username: '',
          port: '',
          remark: '',
          password: ''
        },
        rules: {
          name: [
            {required: true, message: '请输入主机名称', trigger: 'blur'},
            {min: 3, max: 10, message: '长度在3-10位之间', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入连接密码', trigger: 'blur'},
            {min: 3, max: 10, message: '长度在3-10位之间', trigger: 'blur'}
          ],
          category: [
            {required: true, message: '请选择类别', trigger: 'change'}
          ],
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
            {min: 3, max: 10, message: '长度在3-10位', trigger: 'blur'}
          ],
          ip_addr: [
            {required: true, message: '请输入连接地址', trigger: 'blur'},
            {max: 15, message: '长度最大15位', trigger: 'blur'}
          ],
          port: [
            {required: true, message: '请输入端口号', trigger: 'blur'},
            {max: 5, message: '长度最大5位', trigger: 'blur'}
          ]
        }
      });
      let validateName = async (_rule, value) => {
        if (value === '') {
          return Promise.reject('请输入类别名称');
        } else {
          return Promise.resolve();
        }
      };
      const hostCategoryForm = reactive({
        labelCol: {span: 6},
        wrapperCol: {span: 14},
        other: '',
        form: {
          name: ''
        },
        rules: {
          name: [{
            required: true,
            message: '请输入类别名称',
            validator: validateName,
            trigger: 'blur'
          },
            {min: 3, max: 10, message: '长度在3-10位之间', trigger: 'blur'}
          ]
        }
      })
      const layout = {
        labelCol: {
          span: 4,
        },
        wrapperCol: {
          span: 14,
        },
      };
  
      const handleFinish = values => {
        console.log(values, hostForm);
      };
  
      const handleFinishFailed = errors => {
        console.log(errors);
      };
  
      const resetForm = () => {
        formRef.value.resetFields();
      };
  
      const handleValidate = (...args) => {
        console.log(args);
      };
  
      const hostFormVisible = ref(false);
  
      const showHostModal = () => {
        hostFormVisible.value = true;
      };
  
      const showHostCategoryFormModal = () => {
        // 显示添加主机类别的表单窗口
        HostCategoryFromVisible.value = true
      }
      const hostCategoryFormCancel = () => {
        // 添加主机类别的表单取消
        hostCategoryForm.form.name = ""; // 清空表单内容
        HostCategoryFromVisible.value = false // 关闭对话框
      }
  
      const onHostCategoryFromSubmit = () => {
        // 添加主机类别的表单提交处理
        // 添加主机类别的表单提交处理
      // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存
        axios.post('/host/category', hostCategoryForm.form, {
          headers: {
            Authorization: store.getters.token
          }
        }).then(response => {
          message.success({
            content: "创建主机类别成功!",
            duration: 1,
          }).then(() => {
            console.log("response:::", response)
            categoryList.data.unshift(response.data)
            hostCategoryFormCancel()
          })
        })
      }
  
      const onHostFormSubmit = () => {
        // 添加主机的表单提交处理
        const formData = new FormData();
        for (let attr in hostForm.form) {
            formData.append(attr, hostForm.form[attr])
        }

        axios.post(`/host/`, formData, {
                headers: {
                Authorization: store.getters.token,
                }
            }
        ).then((response) => {
            console.log("response>>>", response)
            hostList.data.unshift(response.data)

            // 清空
            resetForm()
            hostFormVisible.value = false; // 关闭对话框
            message.success('成功添加主机信息！')

        }).catch((response) => {
            message.error(response.data)
        });
      }
  
      const get_host_list = () => {
        // 获取主机类别列表
        axios.get(`/host`, {
        headers: {
          Authorization: store.getters.token
        }
      }).then(response => {
        hostList.data = response.data

      }).catch(err => {
        message.error('无法获取主机类别列表信息！')
      })
    }
      const get_category_list = () => {
        // 获取主机类别列表
        axios.get(`/host/category`, {
        headers: {
          Authorization: store.getters.token
        }
        }).then(response => {
            categoryList.data = response.data
        }).catch(err => {
            message.error('无法获取主机类别列表信息！')
        })
      }
  
      const deleteHost = record => {
        // 删除主机接口
        axios.delete(`/host/${record.id}`, {
        headers: {
          Authorization: store.getters.token
        }
        }).then(response => {
            let index = hostList.data.indexOf(record)
            hostList.data.splice(index, 1);

        }).catch(err => {
            message.error('删除主机失败！')
        })

      }
  
      get_host_list()
      get_category_list()
  
      return {
        selectHostCategory: ref('yuan'),
        hostForm,
        formRef,
        layout,
        HostCategoryFromVisible,
        handleCategorySelectChange,
        handleFinishFailed,
        handleFinish,
        resetForm,
        handleValidate,
        hostFormVisible,
        showHostModal,
        onHostFormSubmit,
        deleteHost,
        showHostCategoryFormModal,
        hostCategoryForm,
        hostCategoryFormCancel,
        onHostCategoryFromSubmit,
        hostFormColumns: [
          {
            title: '类别',
            dataIndex: 'category_name',
            key: 'category_name'
          },
          {
            title: '主机名称',
            dataIndex: 'name',
            key: 'name',
            sorter: true,
            width: 230
  
          },
          {
            title: '连接地址',
            dataIndex: 'ip_addr',
            key: 'ip_addr',
            ellipsis: true,
            sorter: true,
            width: 150
          },
          {
            title: '端口',
            dataIndex: 'port',
            key: 'port',
            ellipsis: true
          },
          {
            title: '备注信息',
            dataIndex: 'remark',
            key: 'remark',
            ellipsis: true
          },
  
          {
            title: '操作',
            key: 'action',
            width: 200,
            dataIndex: "action",
            scopedSlots: {customRender: 'action'}
          }
        ],
        hostList,
        categoryList,
  
      };
    },
  };
  </script>
  