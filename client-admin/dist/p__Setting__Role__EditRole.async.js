(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[37],{x0KT:function(e,a,n){"use strict";n.r(a);n("U3G+");var t,l,r,s,o=n("Q2qM"),c=n("U1Sa"),i=n.n(c),m=(n("+iD4"),n("uDpN")),p=(n("u0Ms"),n("mE2p")),d=(n("cgt6"),n("aRya")),u=(n("/9XJ"),n("itzS")),h=n("smUt"),g=n.n(h),y=(n("EMia"),n("ujxS")),f=n("Pjwa"),E=n.n(f),k=n("2cji"),v=n.n(k),C=n("sp3j"),b=n.n(C),P=n("vZkh"),F=n.n(P),w=n("+KCP"),j=n.n(w),D=(n("UZy/"),n("q+O/")),S=(n("gYqB"),n("ybht")),x=(n("4B7h"),n("UFLp")),M=(n("o6y/"),n("t2Zo")),V=n("uqIC"),q=n.n(V),A=n("LneV"),B=(n("a/LZ"),n("df/D"),n("NdDt"),n("kjjE")),U=n("Pt3h"),L=(n("CkN6"),n("zHco")),T=(M["a"].RangePicker,x["a"].Item),Z=S["a"].Panel,J=D["a"].Group;function N(e){return{name:x["a"].createFormField({value:e.roles.entity.name}),desc:x["a"].createFormField({value:e.roles.entity.desc})}}function z(e,a,n){console.log("allValues:",n),console.log("changedValue:",a),console.log("props:",e);var t=e.dispatch;t({type:"roles/changeFormValues",payload:n})}var G=(t=Object(A["connect"])(function(e){var a=e.roles,n=e.loading;return{roles:a,loading:n.models.roles}}),l=x["a"].create({mapPropsToFields:N,onValuesChange:z}),t(r=l((s=function(e){function a(){var e,n;E()(this,a);for(var t=arguments.length,l=new Array(t),r=0;r<t;r++)l[r]=arguments[r];return n=b()(this,(e=F()(a)).call.apply(e,[this].concat(l))),n.state={formValues:{},indeterminate:!0,checkAll:!1},n.handleBackClick=function(){B["a"].push("/setting-center/role-index")},n.handleSubmit=function(e){var a=n.props,t=a.dispatch,l=a.form,r=a.roles,s=r.entity,o=r.selectedPermissions;e.preventDefault(),l.validateFieldsAndScroll(function(e,a){e||(t({type:"roles/update",payload:{id:s.id,name:a.name,desc:a.desc,permissions:o}}),y["a"].success("\u4fdd\u5b58\u6210\u529f"),n.handleBackClick())})},n.onChange=function(e,a,t){var l=n.props,r=l.dispatch,s=l.roles.selectedPermissions,o={};t.length>0?o[e]=t:delete s[e];var c=g()({},s,o);r({type:"roles/changePermission",payload:c})},n.onCheckAllChange=function(e,a,t){var l=n.props,r=l.dispatch,s=l.roles.selectedPermissions,o=a.map(function(e){return e.value}),c={};t.target.checked?c[e]=o:delete s[e];var i=g()({},s,c);r({type:"roles/changePermission",payload:i})},n}return j()(a,e),v()(a,[{key:"componentDidMount",value:function(){var e=this.props,a=e.dispatch,n=e.match;a({type:"roles/template"}),a({type:"roles/getrole",payload:{id:n.params.id}})}},{key:"callback",value:function(e){console.log(e)}},{key:"render",value:function(){var e=this,a=this.props,n=a.roles,t=n.data,l=(n.entity,n.selectedPermissions),r=a.loading,s=a.form,c=s.getFieldDecorator,h={labelCol:{xs:{span:4},sm:{span:2}},wrapperCol:{xs:{span:18},sm:{span:20}}},g={wrapperCol:{xs:{span:24,offset:4},sm:{span:10,offset:2}}},y=t.items||[];return q.a.createElement(L["a"],null,q.a.createElement(o["a"],{bordered:!1},q.a.createElement(x["a"],i()({},h,{onSubmit:this.handleSubmit}),q.a.createElement(d["a"],null,q.a.createElement(T,{label:"\u89d2\u8272\u540d\u79f0"},c("name",{rules:[{required:!0,message:"\u8bf7\u586b\u5199\u89d2\u8272\u540d\u79f0!"}]})(q.a.createElement(u["a"],null)))),q.a.createElement(d["a"],null,q.a.createElement(T,{label:"\u89d2\u8272\u63cf\u8ff0"},c("desc",{rules:[]})(q.a.createElement(u["a"],null)))),q.a.createElement(d["a"],null,q.a.createElement(T,{label:"\u89d2\u8272\u6743\u9650"},y.map(function(a,n){return q.a.createElement(S["a"],{onChange:e.callback,key:a.name},q.a.createElement(Z,{header:a.name,key:a.name},a.module_permissions.map(function(a,n){return q.a.createElement(d["a"],{key:a.module},q.a.createElement(p["a"],{span:8},q.a.createElement(D["a"],{onChange:e.onCheckAllChange.bind(e,a.module,a.permissions)},a.module_name)),q.a.createElement(p["a"],{span:16},q.a.createElement(J,{options:a.permissions,value:l[a.module],onChange:e.onChange.bind(e,a.module,a.permissions)})))})))}))),q.a.createElement(d["a"],null,q.a.createElement(T,i()({},g,{style:{marginTop:32}}),q.a.createElement(m["a"],{type:"primary",htmlType:"submit",loading:r},q.a.createElement(U["FormattedMessage"],{id:"form.save"})),q.a.createElement(m["a"],{style:{marginLeft:8},onClick:this.handleBackClick},q.a.createElement(U["FormattedMessage"],{id:"form.back"})))))))}}]),a}(V["PureComponent"]),r=s))||r)||r);a["default"]=G}}]);