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
  Popover,
  Progress,
} from 'antd';
import StandardTable from '@/components/StandardTable';
import PageHeaderWrapper from '@/components/PageHeaderWrapper';
import styles from './CreateUser.less';

const { RangePicker } = DatePicker;
const { Option } = Select;
const FormItem = Form.Item;
const Panel = Collapse.Panel;
const CheckboxGroup = Checkbox.Group;

const passwordStatusMap = {
  ok: (
    <div className={styles.success}>
      <FormattedMessage id="validation.password.strength.strong" />
    </div>
  ),
  pass: (
    <div className={styles.warning}>
      <FormattedMessage id="validation.password.strength.medium" />
    </div>
  ),
  poor: (
    <div className={styles.error}>
      <FormattedMessage id="validation.password.strength.short" />
    </div>
  ),
};

const passwordProgressMap = {
  ok: 'success',
  pass: 'normal',
  poor: 'exception',
};

/* eslint react/no-multi-comp:0 */
@connect(({ users, loading }) => ({
  users,
  loading: loading.models.users,
}))
@Form.create()
class EditUser extends PureComponent {
  state = {
    confirmDirty: false,
    visible: false,
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch({
      type: 'users/getRoleSelectList',
    });
  }

  handleBackClick = () => {
    router.push(`/user-center/user-list`);
  };

  handleAdd = fields => {
    const { dispatch } = this.props;
    dispatch({
      type: 'users/add',
      payload: {
        username: fields.username,
      },
    });

    message.success('添加成功');
    this.handleBackClick();
  };

  handleSubmit = e => {
    const {
      dispatch,
      form,
      users: { role_ids },
    } = this.props;
    e.preventDefault();
    form.validateFieldsAndScroll((err, values) => {
      if (!err) {
        dispatch({
          type: 'users/update',
          payload: {
            username: values.username,
            email: values.email,
            password: values.password,
            role_ids: role_ids,
          },
        });
        message.success('添加成功');
        this.handleBackClick();
      }
    });
  };

  handleRoleChange = value => {
    console.log(`selected ${value}`);
    const { dispatch } = this.props;
    dispatch({
      type: 'users/setRoleIds',
      payload: value,
    });
  };

  callback(key) {
    console.log(key);
  }
  render() {
    const {
      users: { roleSelectList },
      loading,
      form,
    } = this.props;
    const { visible } = this.state;
    const { getFieldDecorator } = form;

    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 7 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 12 },
        md: { span: 10 },
      },
    };

    const submitFormLayout = {
      wrapperCol: {
        xs: { span: 24, offset: 0 },
        sm: { span: 10, offset: 7 },
      },
    };
    // const { selectedRows, modalVisible, updateModalVisible, stepFormValues } = this.state;
    const text = `
      A dog is a type of domesticated animal.
      Known for its loyalty and faithfulness,
      it can be found as a welcome guest in many households across the world.
    `;
    return (
      <PageHeaderWrapper>
        <Card bordered={false}>
          <Form {...formItemLayout} onSubmit={this.handleSubmit}>
            <Row>
              <FormItem label="用户名">
                {getFieldDecorator('username', {
                  rules: [
                    {
                      required: true,
                      message: '请填写用户名!',
                    },
                  ],
                })(<Input disabled placeholder="请输入用户名" />)}
              </FormItem>
            </Row>
            <Row>
              <FormItem label="邮箱" placeholder="请输入邮箱">
                {getFieldDecorator('email', {
                  rules: [
                    {
                      required: true,
                      message: formatMessage({ id: 'validation.email.required' }),
                    },
                    {
                      type: 'email',
                      message: formatMessage({ id: 'validation.email.wrong-format' }),
                    },
                  ],
                })(<Input disabled placeholder="请输入邮箱" />)}
              </FormItem>
            </Row>
            <Row>
              <FormItem
                {...formItemLayout}
                label="角色权限"
                // help="多选"
              >
                {getFieldDecorator('role_ids')(
                  <Select
                    mode="multiple"
                    placeholder="请选择角色权限"
                    onChange={this.handleRoleChange}
                  >
                    {roleSelectList.map((item, index) => {
                      return (
                        <Option value={item.key} key={item.key}>
                          {item.name}
                        </Option>
                      );
                    })}
                  </Select>
                )}
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

export default EditUser;
