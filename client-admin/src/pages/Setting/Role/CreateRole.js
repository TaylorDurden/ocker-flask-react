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
    permissions: {},
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

  handleSubmit = fields => {
    const { dispatch } = this.props;
    dispatch({
      type: 'roles/add',
      payload: {
        name: fields.name,
        desc: fields.desc,
        permissiongs: [],
      },
    });

    message.success('添加成功');
    this.handleBackClick();
  };

  callback(key) {
    console.log(key);
  }

  onChange = checkedList => {
    this.setState({
      checkedList,
      indeterminate: !!checkedList.length && checkedList.length < plainOptions.length,
      checkAll: checkedList.length === plainOptions.length,
    });
  };

  onCheckAllChange = e => {
    this.setState({
      checkedList: e.target.checked ? plainOptions : [],
      indeterminate: false,
      checkAll: e.target.checked,
    });
  };

  render() {
    const {
      roles: { data },
      loading,
      form,
    } = this.props;
    console.log(data);
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
                              indeterminate={this.state.indeterminate}
                              onChange={this.onCheckAllChange}
                              checked={this.state.checkAll}
                            >
                              {item.module_name}
                            </Checkbox>
                          </Col>
                          <Col span={16}>
                            <CheckboxGroup
                              options={item.permissions&&item.permissions.map(x => x.name)}
                              value={item.permissions&&item.permissions.map(x => x.value)}
                              onChange={this.onChange}
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
