import { queryRule, batchInactive, inactive, addRule, updateRule } from '@/services/api';
import { query, addUser, editUser } from '@/services/user';
import { getRoleSelectList } from '@/services/role';

export default {
  namespace: 'users',

  state: {
    data: {
      list: [],
      pagination: {},
    },
    entity: {},
    roleSelectList: [],
    role_ids: [],
  },

  effects: {
    *fetch({ payload }, { call, put }) {
      const response = yield call(query, payload);
      yield put({
        type: 'save',
        payload: response,
      });
    },
    *add({ payload, callback }, { call, put }) {
      const response = yield call(addUser, payload);
      // yield put({
      //   type: 'save',
      //   payload: response,
      // });
      if (callback) callback();
    },
    *edit({ payload, callback }, { call, put }) {
      const response = yield call(editUser, payload);
      // yield put({
      //   type: 'save',
      //   payload: response,
      // });
      if (callback) callback();
    },
    *inactive({ payload, callback }, { call, put }) {
      const response = yield call(inactive, payload);
      yield put({
        type: 'save',
        payload: response,
      });
      if (callback) callback();
    },
    *batchInactive({ payload, callback }, { call, put }) {
      const response = yield call(batchInactive, payload);
      yield put({
        type: 'save',
        payload: response,
      });
      if (callback) callback();
    },
    *update({ payload, callback }, { call, put }) {
      const response = yield call(editUser, payload);
      if (callback) callback();
    },
    *getRoleSelectList({ payload, callback }, { call, put }) {
      const response = yield call(getRoleSelectList);
      yield put({
        type: 'initRoleSelect',
        payload: response,
      });
      if (callback) callback();
    }
  },

  reducers: {
    save(state, action) {
      return {
        ...state,
        data: action.payload,
      };
    },
    changeFormValues(state, action) {
      const { entity } = state;
      const newEntity = { ...entity, ...action.payload };
      return {
        ...state,
        entity: newEntity
      };
    },
    changeRoles(state, action) {
      return {
        ...state,
        entity: action.payload
      };
    },
    initRoleSelect(state, action) {
      return {
        ...state,
        roleSelectList: action.payload
      };
    },
    setRoleIds(state, action) {
      return {
        ...state,
        role_ids: action.payload
      };
    },
  },
};
