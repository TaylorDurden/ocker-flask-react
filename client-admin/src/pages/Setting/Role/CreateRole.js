import React, { PureComponent, Fragment } from 'react';
import { connect } from 'dva';
import moment from 'moment';
import mt from 'moment-timezone';
import 'moment/locale/zh-cn';
import router from 'umi/router';
import { formatMessage, FormattedMessage } from 'umi-plugin-react/locale';
import {
  Row,
  Col,
  Card,
  Form,
  Input,
  Select,
  Icon,
  Button,
  Dropdown,
  Menu,
  InputNumber,
  DatePicker,
  Modal,
  message,
  Badge,
  Divider,
  Steps,
  Radio,
  Collapse,
  Checkbox,
} from 'antd';
import StandardTable from '@/components/StandardTable';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';

const { RangePicker } = DatePicker;
const FormItem = Form.Item;
const Panel = Collapse.Panel;
const CheckboxGroup = Checkbox.Group;

const plainOptions = ['Apple', 'Pear', 'Orange'];
const defaultCheckedList = ['Apple', 'Orange'];

/* eslint react/no-multi-comp:0 */
@connect(({ roles, loading }) => ({
  roles,
  loading: loading.models.roles,
}))
@Form.create()
class CreateRole extends PureComponent {
  state = {
    formValues: {},
    // permissions: {},
    selectedPermissions: {},
    checkedList: defaultCheckedList,
    indeterminate: true,
    checkAll: false,
  };

  columns = [
    {
      title: '角色名称',
      dataIndex: 'name',
    },
    {
      title: '角色描述',
      dataIndex: 'desc',
    },
    {
      title: '操作',
      fixed: 'right',
      width: 100,
      render: (text, record) => (
        <Fragment>
          <a onClick={() => this.handleUpdateModalVisible(true, record)}>编辑</a>
        </Fragment>
      ),
    },
  ];

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'roles/template',
    });
  }

  handleBackClick = () => {
    router.push(`/setting-center/role-index`);
  };

  handleAdd = fields => {
    const { dispatch } = this.props;
    dispatch({
      type: 'roles/add',
      payload: {
        desc: fields.desc,
      },
    });

    message.success('添加成功');
    this.handleBackClick();
  };

  handleSubmit = e => {
    const { dispatch, form } = this.props;
    const { selectedPermissions } = this.state;
    e.preventDefault();
    form.validateFieldsAndScroll((err, values) => {
      if (!err) {
        dispatch({
          type: 'roles/add',
          payload: {
            name: values.name,
            desc: values.desc,
            permissions: selectedPermissions,
          },
        });
      }
    });
    // dispatch({
    //   type: 'roles/add',
    //   payload: {
    //     name: fields.name,
    //     desc: fields.desc,
    //     selectedPermissions,
    //   },
    // });

    message.success('添加成功');
    this.handleBackClick();
  };

  callback(key) {
    console.log(key);
  }

  onChange = (module, items, checkedList) => {
    const modulePermissions = {};
    modulePermissions[[module]] = checkedList;
    const { selectedPermissions } = this.state;
    const newPermissions = {...selectedPermissions, ...modulePermissions};
    this.setState({
      selectedPermissions: newPermissions,
      // checkAll: checkedList.length === items.length,
    });
  };

  onCheckAllChange = (module, items, e) => {
    const allValues = items.map(item => item.value);
    const modulePermissions = {};
    modulePermissions[module] = e.target.checked ? allValues : [];
    const { selectedPermissions, } = this.state;
    const newPermissions = {...selectedPermissions, ...modulePermissions};
    this.setState({
      selectedPermissions: newPermissions,
      // selectedPermissions,
      // checkAll: e.target.checked,
    });
  };

  render() {
    const {
      roles: { data },
      loading,
      form,
    } = this.props;
    console.log(data);
    const { selectedPermissions } = this.state;
    const { getFieldDecorator } = form;

    const formItemLayout = {
      labelCol: {
        xs: { span: 4 },
        sm: { span: 2 },
      },
      wrapperCol: {
        xs: { span: 18 },
        sm: { span: 20 },
      },
    };

    const submitFormLayout = {
      wrapperCol: {
        xs: { span: 24, offset: 4 },
        sm: { span: 10, offset: 2 },
      },
    };
    // const { selectedRows, modalVisible, updateModalVisible, stepFormValues } = this.state;

    // const parentMethods = {
    //   handleAdd: this.handleAdd,
    // };
    const text = `
      A dog is a type of domesticated animal.
      Known for its loyalty and faithfulness,
      it can be found as a welcome guest in many households across the world.
    `;
    const permissions = data.items || [];
    return (
      <PageHeaderWrapper>
        <Card bordered={false}>
          <Form {...formItemLayout} onSubmit={this.handleSubmit}>
            <Row>
              <FormItem label="角色名称">
                {getFieldDecorator('name', {
                  rules: [
                    {
                      required: true,
                      message: '请填写角色名称!',
                    },
                  ],
                })(<Input />)}
              </FormItem>
            </Row>
            <Row>
              <FormItem label="角色描述">
                {getFieldDecorator('desc', {
                  rules: [],
                })(<Input />)}
              </FormItem>
            </Row>
            <Row>
              <FormItem label="角色权限">
                {permissions.map((item, index) => (
                  <Collapse onChange={this.callback} key={item.name}>
                    <Panel header={item.name} key={item.name}>
                      {item.module_permissions.map((item, i) => (
                        <Row key={item.module}>
                          <Col span={8}>
                            <Checkbox
                              //indeterminate={this.state.indeterminate}
                              onChange={this.onCheckAllChange.bind(this, item.module, item.permissions)}

                            >
                              {item.module_name}
                            </Checkbox>
                          </Col>
                          <Col span={16}>
                            {/* {item.permissions &&
                              item.permissions.map((checkbox, index) => (
                                <Checkbox
                                  key={index}
                                  //indeterminate={this.state.indeterminate}
                                  onChange={this.onChange}
                                  // checked={!checkbox.disable}
                                >
                                  {checkbox.name}
                                </Checkbox>
                              ))} */}
                            <CheckboxGroup
                              options={item.permissions}
                              value={selectedPermissions[item.module]}
                              onChange={this.onChange.bind(this, item.module, item.permissions)}
                            />
                          </Col>
                        </Row>
                      ))}
                    </Panel>
                  </Collapse>
                ))}
              </FormItem>
            </Row>
            <Row>
              <FormItem {...submitFormLayout} style={{ marginTop: 32 }}>
                <Button type="primary" htmlType="submit" loading={loading}>
                  <FormattedMessage id="form.save" />
                </Button>
                <Button style={{ marginLeft: 8 }}>
                  <FormattedMessage id="form.back" />
                </Button>
              </FormItem>
            </Row>
          </Form>
        </Card>
      </PageHeaderWrapper>
    );
  }
}

export default CreateRole;
