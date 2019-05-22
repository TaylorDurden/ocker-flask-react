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

/* eslint react/no-multi-comp:0 */
@connect(({ roles, loading }) => ({
  roles,
  loading: loading.models.roles,
}))
@Form.create()
class CreateUser extends PureComponent {
  state = {
    formValues: {},
    // permissions: {},
    //selectedPermissions: {},
    indeterminate: true,
    checkAll: false,
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'roles/template',
    });
  }

  handleBackClick = () => {
    router.push(`/setting-center/user-index`);
  };

  handleSubmit = e => {
    const { dispatch, form, roles:{ selectedPermissions } } = this.props;
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
        message.success('添加成功');
        this.handleBackClick();
      }
    });
  };

  callback(key) {
    console.log(key);
  }

  // onChange = (module, items, checkedList) => {
  //   const modulePermissions = {};
  //   modulePermissions[module] = checkedList;
  //   const { selectedPermissions } = this.state;
  //   const newPermissions = {...selectedPermissions, ...modulePermissions};
  //   this.setState({
  //     selectedPermissions: newPermissions,
  //     // checkAll: checkedList.length === items.length,
  //   });
  // };
  onChange = (module, items, checkedList) => {
    const { dispatch, roles: { selectedPermissions }, } = this.props;
    const modulePermissions = {};
    modulePermissions[module] = checkedList;
    const newPermissions = {...selectedPermissions, ...modulePermissions};
    dispatch({
      type: 'roles/changePermission',
      payload: newPermissions
    });
    
  };

  onCheckAllChange = (module, items, e) => {
    const { dispatch, roles: { selectedPermissions }, } = this.props;
    const allValues = items.map(item => item.value);
    const modulePermissions = {};
    modulePermissions[module] = e.target.checked ? allValues : [];
    const newPermissions = {...selectedPermissions, ...modulePermissions};
    dispatch({
      type: 'roles/changePermission',
      payload: newPermissions
    });
  };

  // onCheckAllChange = (module, items, e) => {
  //   const allValues = items.map(item => item.value);
  //   const modulePermissions = {};
  //   modulePermissions[module] = e.target.checked ? allValues : [];
  //   const { selectedPermissions, } = this.state;
  //   const newPermissions = {...selectedPermissions, ...modulePermissions};
  //   this.setState({
  //     selectedPermissions: newPermissions,
  //     // selectedPermissions,
  //     // checkAll: e.target.checked,
  //   });
  // };


  render() {
    const {
      roles: { data, selectedPermissions },
      loading,
      form,
    } = this.props;
    console.log(data);
    const {  } = this.state;
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
              <FormItem label="用户名称">
                {getFieldDecorator('username', {
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
              <FormItem label="用户邮箱">
                {getFieldDecorator('email', {
                  rules: [],
                })(<Input />)}
              </FormItem>
            </Row>
            <Row>
              <FormItem {...submitFormLayout} style={{ marginTop: 32 }}>
                <Button type="primary" htmlType="submit" loading={loading}>
                  <FormattedMessage id="form.save" />
                </Button>
                <Button style={{ marginLeft: 8 }} onClick={this.handleBackClick}>
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

export default CreateUser;
