import { queryRule, batchInactive, inactive, addRule, updateRule } from '@/services/api';
import { query, getPermissionTemplate, newRole, getRoleWithPermissions, editRole } from '@/services/role';

export default {
  namespace: 'roles',

  state: {
    data: {
      list: [],
      pagination: {},
    },
    entity: {},
    selectedPermissions: {},
  },

  effects: {
    *fetch({ payload }, { call, put }) {
      const response = yield call(query, payload);
      yield put({
        type: 'save',
        payload: response,
      });
    },
    *template({ payload }, { call, put }) {
      const response = yield call(getPermissionTemplate, payload);
      yield put({
        type: 'save',
        payload: response,
      });
    },
    *add({ payload, callback }, { call, put }) {
      const response = yield call(newRole, payload);
      yield put({
        type: 'save',
        payload: response,
      });
      if (callback) callback();
    },
    *update({ payload, callback }, { call, put }) {
      const response = yield call(editRole, payload);
      // yield put({
      //   type: 'save',
      //   payload: response,
      // });
      if (callback) callback();
    },
    *getrole({ payload, callback }, { call, put }) {
      const response = yield call(getRoleWithPermissions, payload);
      // type，effects与reducers里的定义不要重名
      yield put({
        type: 'get',
        payload: response,
      });
      if (callback) callback();
    },
  },

  reducers: {
    save(state, action) {
      return {
        ...state,
        data: action.payload,
      };
    },
    get(state, action) {
      return {
        ...state,
        entity: action.payload.data,
        selectedPermissions: action.payload.data.permissions
      };
    },
    changePermission(state, action) {
      // const checkdPermissions = action.payload;
      // Object.keys(action.payload).forEach((item) => {
      //   if(action.payload[item].length === 0) {
      //     delete checkdPermissions.payload[item]
      //   }
      // })
      return {
        ...state,
        selectedPermissions: action.payload
      };
    },
    changeFormValues(state, action) {
      const { entity } = state;
      const newEntity = { ...entity, ...action.payload };
      return {
        ...state,
        entity: newEntity
      };
    }
  },
};
