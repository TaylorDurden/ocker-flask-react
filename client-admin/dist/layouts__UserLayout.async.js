(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[3],{BOD2:function(e,a,t){e.exports={container:"antd-pro-layouts-user-layout-container",lang:"antd-pro-layouts-user-layout-lang",content:"antd-pro-layouts-user-layout-content",top:"antd-pro-layouts-user-layout-top",header:"antd-pro-layouts-user-layout-header",logo:"antd-pro-layouts-user-layout-logo",title:"antd-pro-layouts-user-layout-title",desc:"antd-pro-layouts-user-layout-desc"}},jH8a:function(e,a,t){"use strict";t.r(a);var n=t("Pjwa"),r=t.n(n),o=t("2cji"),l=t.n(o),s=t("sp3j"),u=t.n(s),c=t("vZkh"),i=t.n(c),m=t("+KCP"),p=t.n(m),d=(t("Im/E"),t("lCpv")),y=t("uqIC"),h=t.n(y),g=t("Pt3h"),f=t("LneV"),v=t("sQVf"),b=t("ggcP"),E=t("Cjad"),k=t.n(E),N=t("bfXr"),j=t("BOD2"),D=t.n(j),M=t("mxmt"),w=t.n(M),O=t("tGQQ"),C=[{key:"help",title:Object(g["formatMessage"])({id:"layout.user.link.help"}),href:""},{key:"privacy",title:Object(g["formatMessage"])({id:"layout.user.link.privacy"}),href:""},{key:"terms",title:Object(g["formatMessage"])({id:"layout.user.link.terms"}),href:""}],P=h.a.createElement(y["Fragment"],null,"Copyright ",h.a.createElement(d["a"],{type:"copyright"})," 2018 \u8682\u8681\u91d1\u670d\u4f53\u9a8c\u6280\u672f\u90e8\u51fa\u54c1"),Q=function(e){function a(){return r()(this,a),u()(this,i()(a).apply(this,arguments))}return p()(a,e),l()(a,[{key:"componentDidMount",value:function(){var e=this.props,a=e.dispatch,t=e.route,n=t.routes,r=t.authority;a({type:"menu/getMenuData",payload:{routes:n,authority:r}})}},{key:"render",value:function(){var e=this.props,a=e.children,t=e.location.pathname,n=e.breadcrumbNameMap;return h.a.createElement(k.a,{title:Object(O["a"])(t,n)},h.a.createElement("div",{className:D.a.container},h.a.createElement("div",{className:D.a.lang},h.a.createElement(N["a"],null)),h.a.createElement("div",{className:D.a.content},h.a.createElement("div",{className:D.a.top},h.a.createElement("div",{className:D.a.header},h.a.createElement(v["a"],{to:"/"},h.a.createElement("img",{alt:"logo",className:D.a.logo,src:w.a}),h.a.createElement("span",{className:D.a.title},"Ant Design"))),h.a.createElement("div",{className:D.a.desc},"Ant Design \u662f\u897f\u6e56\u533a\u6700\u5177\u5f71\u54cd\u529b\u7684 Web \u8bbe\u8ba1\u89c4\u8303")),a),h.a.createElement(b["a"],{links:C,copyright:P})))}}]),a}(y["Component"]);a["default"]=Object(f["connect"])(function(e){var a=e.menu;return{menuData:a.menuData,breadcrumbNameMap:a.breadcrumbNameMap}})(Q)}}]);