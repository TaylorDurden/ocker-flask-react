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
    checkAllArray: {},
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
      yield put({
        type: 'save',
        payload: response,
      });
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
        entity: {},
        selectedPermissions: {},
      };
    },
    get(state, action) {
      const { data } = action.payload;
      const { permissions } = data;
      const template = state.data;
      let checkAllArr = {};
      template.items.forEach((item, index) => {
        const { module_permissions } = item;
        module_permissions.forEach((t, i) => {
          const checkedIndex = t.module; // 101或201等module值
          const checkedPermissions = permissions[checkedIndex]; // [0,2,4]
          if(checkedPermissions){
            const ps = t.permissions;
            checkAllArr[checkedIndex] = ps.length === checkedPermissions.length;
          }
        });
      });
      return {
        ...state,
        entity: action.payload.data,
        selectedPermissions: action.payload.data.permissions,
        checkAllArray: checkAllArr,
      };
    },
    changePermission(state, action) {
      // const checkdPermissions = action.payload;
      // Object.keys(action.payload).forEach((item) => {
      //   if(action.payload[item].length === 0) {
      //     delete checkdPermissions.payload[item]
      //   }
      // })
      const { newPermissions, checkAllArray } = action.payload;
      return {
        ...state,
        selectedPermissions: newPermissions || action.payload,
        checkAllArray: checkAllArray,
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
