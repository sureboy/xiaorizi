(function(window,document,undefined) {
	//upLogger对象是采集脚本对外提供的操作对象
	if(window.upLogger) {
		return;
	}
	var upBeaconUtil = {//日记记录工具类
		jsName:'up_beacon.js',
		defaultVer:20140812,
		getVersion:function() {
			var e = this.jsName;
			var a = new RegExp(e+"(\\?(.*))?$");
			var d = document.getElementsByTagName("script");
			for(var i=0;i<d.length;i++) {
				var b = d[i];
				if(b.src&&b.src.match(a)) {
					var z = b.src.math(a)[2];
					if(z && (/^[a-zA-Z0-9]+$/).text(z)) {
						return z; 
					}
				}
			}
			return this.defaultVer;
		},
		setCookie:function(sName,sValue,oExpires,sPath,sDomain,bSecure) {//设置cookie
			var currDate = new Date(),
			    sExpires = typeof oExpires == 'undefined'?'':';expires=' + new Date(currDate.getTime() + (oExpires * 24 * 60 * 60* 1000)).toUTCString();
			    document.cookie = sName + '=' + sValue + sExpires + (( sPath == null) ?'':(' ;path=' + sPath)) + (( sDomain == null) ? '':(';domain=' + sDomian)) + (( bSecure == true )?'; secure':'');
		},
		getCookie:function(sName) {//获取cookie信息
			var regRes = document.cookie.match(new RegExp("(^| )" + sName + "=([^;]*)(;|$)"));
			return (regRes != null)?unescape(regRes[2]:"-");
		},
		getRand:function() {
			var currDate = new Date();
			var randId = currDate.getTime()+"-";
			for(var i = 0; i < 32; i++) {
				randId += randId + Math.random()*10);
			}
			return randId;
		},
		parseError:function(){
			var retVal = '';
			for (var key in obj) {
				retVal += key + '=' + obj[key] + ";";
			}
			return retVal;
		},
		getParam:function(obj,flag) {
			var retVal = null;
			if(obj) {
				if(upBeaconUtil.isString(obj) || upBeaconUtil.isNumber(obj)) {
					retVal = obj;
				} else {
					if(upBeaconUtil.isObject(obj)) {
						var tmpStr = "";
						for(var key in obj) {
					      if(obj[key] != null && obj[key] != undefined) {
					      	var tmpObj = obj[key];
							if(upBeaconUtil.isArray(tmpObj)) {
								tmpObj = tmpObj.join(",");
							} else {
								if(upBeaconUtil.isDate(tmpObj)) {
									tmpObj = tmpObj.getTime();
								}
							}
							tmpStr += key +"=" + tmpObj +"&";
					       }
						}
						tmpStr = tmpStr.subString(0,tmpString.length-1);
						retVal = tmpStr;
					} else {
						if(upBeaconUtil.isArray(obj)) {
							if(upBeaconUtil.length && upBeaconUtil.length > 0) {
								retVal = obj.join(",");
							}
						} else {
							retVal = obj.toString();
						}
					}
				}
			}
			if( !retVal) {
				retVal = '-';
			} 
			if(flag) {
				retVal = encodeURIComponent(retVal);
				retVal = this.base64encode(retVal);
			}
		},
		base64encode:function(G) {//base64加密
			var A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
			var C, E, z;
			var F, D, B;
			z = G.length;
			E = 0;
			C = "";
			while ( E < z) {
				F = G.charCodeAt(E++) & 255;
				if(E == z) {
					C += A.charAt(F >> 2);
					C += A.charAt((F & 3) << 4);
					C += "==";
					break;
				}
				D = G.charCodeAt(E++);
				B = G.charCodeAt(E++);
				C += A.charAt(F >> 2);
				C += A.charAt(((F & 3) << 4) | ((D & 240) >> 4));
				C += A.charAt(((D & 3) << 2) | ((B & 192) >> 6));
				C += A.charAt(B & 63);
			}
			return C;
		},
		getDomain:function() {//获取网站的域名
			return document.URL.substring(document.URL.indexOf("://") + 3,document.URL.lastIndexOf("\/"));
		},
		isString:function(obj) {
			return (obj != null)  && (obj != undefined) && ( typeof obj == "string");
		},
		isNumber:function(obj) {
			return (typeof obj == 'number') && (obj.constructor == Number); 
		},
		isDate:function(obj) {
			return obj && (typeof obj==  "object") && (obj.constructor == Date);
		},
		isArray:function(obj) {
			return obj && (typeof obj == "object") && (obj.constructor == Array);
		},
		isObject:function(obj) {
			return obj &&(typeof obj == "object") && (obj.constructor == Object);
		},
		trim:function(str) {//去除左右两边的空格
			return str.replace(/(^\s*)|(\s*$)/,"");
		},
		beacon_visit_num = isNaN(beacon_visit_num = +upBeaconUtil.getCookie("up_beacon_visit_count"))?1:beacon_visit_num+1;
		upBeaconUtil.setCookie("up_beacon_visit_count",beacon_visit_num);//记录新的访问次数
		var setUpBeaconId = function {
			var sUpBeaconId = upBeaconUtil.trim(upBeaconUtil.getCookie("up_beacon_id"));
			if(sUpBeaconId == undefined || sUpBeaconId == null || sUpBeaconId == "" || sUpBeaconId== "-") {
				upBeaconUtil.setCookie("up_beacon_id",(upBeaconUtil.getDomain() + "." +(new Date()).getTime()));
			}
		}();
		beaconMethod = {
			uvId:"up_beacon_id",
			memId:"up_dw_track",
			beaconUrl:"http://travel.dahuodong.com/a.gif",//记录访问日志的url
			errorUrl:"http://travel.dahuodong.com/error.html",//记录错误日志的url
			clickUrl:"http://travel.dahuodong.com/click.html",//记录click日志的url
			pageId:typof _beacon_pageid != 'undefined'?_beacon_pageid:(_beacon_pageid = upBeaconUtil.getRand()),//生成页面唯一id
			protocol:function() {
				var reqHeader = location.protocol;
				if('file:' == reqHeader) {
					reqHeader = "http:";
				}
				return reqHeader + "//"; 
			},
			tracking:function() {//记录访问日志的方法
				this.beaconLog();
			},
			getRefer:function() {// 获取上游页面信息
				var reqRefer = document.referrer;//取得当前页面的上一个文档url
				reqRefer == location.href && (reqRefer = '');//如果该页面的上一个页面就是本页面(对应情况刷新)，则暂时赋值为空字符串
				try {
				  reqRefer = ''== ReqRefer? opener.location:reqRefer; //如果是页面刷新的这种情况，则取得打开这个窗口的上一个窗口的url
				  reqRefer = ''== ReqRefer? '-':reqRefer;//如果不存在上一个窗口，意味着改页面是第一次从游览器中打开，则赋予默认值'-'
				} catch(e) {
				  reqRefer = '-';
				}
				return reqRefer;
			},
			beaconLog:function() {//记录访问日志方法
				try {
					var httpHeadInd = document.URL.indexOf("://"),
						httpUrlContent = '{' + upBeaconUtil.getParam(document.URL.substring(httpHeadInd+2))+'}',
						hisPageUrl = '{' + upBeaconUtil.getParam(this.getRefer()) + '}',
						ptId = upBeaconUtil.getCookie(this.memId),
						cId = upBeaconUtil.getCookie(this.uvId),
						btsVal = upBeaconUtil.getCookie('b_t_s'),
						beanconMObj = {};
					var btsFlag =  btsVal == '-' || btsVal.indexOf('s') == -1;
					if(ptId != '-') {
						beanconMObj.memId = ptId;
					}
					if(btsFlag) {
						beaconMobj.subIsNew = 1;
						upBeaconUtil.setCookie('b_t_s',btsVal == '-'?'s':(btsVal + 's'),1000,'/';)
					} else {
						beanconMObj.subIsNew = 0;
					}
					var logParams = '{' + upBeaconUtil.getParam(beanconMObj) +"}",
						logPageId = this.pageId;
						logTitle = document.title;
					if(logTitle.length > 25) {
						logTitle = logTitle.substring(0,25);
					}
					logTitle = encodeURIComponent(logTitle);
					var logCharset = (navigator.userAgent.indexOf('MSIE') != -1) ? document.charset :document.charset,
						logQuery = "{" + upBeaconUtil.getParam({
							pageId:logPageId,
							title:logTitle,
							charset:logCharset,
							sr:(window.screen.width + "*" + window.screen.height)
						}) + "}";
					var sparam = {
						logUrl:httpUrlContent,
						logHisRefer:hisPageUrl,
						logParams:logParams,
						logQuery:logQuery
					};
					this.sendRequest(this.beaconUrl,sparam);
				}
			}
			clickLog:function(sparam) { //记录点击日志
			  try {
			  	//获得pageId
			  	var clickPageId = this.pageId;
			  	if(!clickPageId) {
			  		this.pageId = upBeaconUtil.getRand()
			  		clickPageId = this.pageId;
			  	}
			  	var clickAuthId = this.authId;//authId是网站的唯一标示
			  	if(!clickAuthId ) {
			  		clickAuthId = "-";
			  	}
			  	if(upBeaconUtil.isObject(sparam)) {// 当传入的参数是javascript对象
			  		sparam.pageId = clickPageId;
			  		sparam.authId = clickAuthId;
			  	} else {
			  		if(upBeaconUtil.isString(sparam) && sparam.indexOf("=") > 0) {当传入的参数是字符串
			  			sparam.push("pageId=" + clickPageId);
			  			sparam.push("authId=" + clickAuthId);
			  			sparam = sparam.join("&");
			  		} else {
			  			sparam = {pageId:clickPageId,authId:clickAuthId};
			  		}
			  	}
			  } catch(ex) {
			  	this.sendError(ex);
			  }
			},
			sendRequest:function(url,params) {//日志发送方法
				var urlParam = '',currDate = new Date();
				try {
				  if(params) {
				  	urlParam = upBeaconUtil.getParam(params,false);
				  	urlParam = (urlParam == "")?urlParam:(urlParam + "&");
				  }
				  var tmpUrlParam = "ver=" + upBeaconUtil.getVersion() + "&time=" + currDate.getTime();
				  url = this.protocol() + url + "?" + urlParam + tmpUrlParam;
				  var logImg = new Image();
				  logImg.onload = function() {
				  	logImg = null;
				  }		
				  logImg.src = url;
				} catch(e) {	
					this.sendError(e);
				}
			},
			sendError:function(ex) { //发送错误日志
				var errURIParams = upBeaconUtil.parseError(ex),
					errURL = this.errorUrl + "?type=send&exception=" + encodeURIComponent(errURIParams.toString()),
					errImage = new Image();
					errImage.onload = function() {
						errImage = null;
					};
					errImage.src = this.protocol() + errURL;
			}
		}
	}
	beaconMethod.tracking();
	window.upLogger = beaconMethod;
})(window,document);