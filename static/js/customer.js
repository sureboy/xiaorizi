function color() {
	if ($("#colorColumn").length <= 0) {
		return false;
	} else {
		var colorColumn = $("#colorColumn");
		var rows = colorColumn.find(".inner_wrapper");
		var first = $(rows[0]).find("div.service");
		var serviceTmp = null;
		if (first) {
			for (var i = 0; i < first.length; i++) {
				serviceTmp = $(first[i]);
				if (i <= 1) {
					serviceTmp.addClass("color_1");
				} else {
					serviceTmp.addClass("gray");
					if (serviceTmp.find('span.glyphicon-tag').length >= 0) {
						serviceTmp.find('span.glyphicon-tag').addClass("color_11");
					}
				}
			}
		}
		var second = $(rows[1]).find("div.service");
		if (second) {
			for (var j = 0; j < second.length; j++) {
				serviceTmp = $(second[j]);
				if (j <= 1) {
					serviceTmp.addClass("color_2");
				} else {
					serviceTmp.addClass("gray");
					if (serviceTmp.find('span.glyphicon-tag').length >= 0) {
						serviceTmp.find('span.glyphicon-tag').addClass("color_22");
					}
				}
			}
		}
		var third = $(rows[2]).find("div.service");
		if (third) {
			for (var k = 0; k < third.length; k++) {
				serviceTmp = $(third[k]);
				if (k <= 1) {
					serviceTmp.addClass("color_3");
				} else {
					serviceTmp.addClass("gray");
					if (serviceTmp.find('span.glyphicon-tag').length >= 0) {
						serviceTmp.find('span.glyphicon-tag').addClass("color_33");
					}
				}
			}
		}
	}
}
function disabledBtn() {
	if ($("#priceList").attr("data-soure-price").indexOf("收费") != -1) {
		$(".hiddenByTime").attr("disabled", "disabled");
		$("#priceList").find(".priceLabel").css("backgroundImage","none").css("border","1px solid #c1c1c1");
		$(".spotTip").text("此活动为收费活动，具体价格待定，如需购买请致电400-003-3879");
	}
	if ($("#priceList").attr("data-soure-price").indexOf("待定") != -1) {
		$(".hiddenByTime").attr("disabled", "disabled");
		$("#priceList").find(".priceLabel").css("backgroundImage","none").css("border","1px solid #c1c1c1");
		$(".spotTip").text("此活动为收费活动，具体价格待定，如需购买请致电400-003-3879");
	}
	if ($("#priceList").attr("data-soure-price").indexOf("免费") != -1) {
		$(".hiddenByTime").attr("disabled", "disabled");
		$("#priceList").find(".priceLabel").css("backgroundImage","none").css("border","1px solid #c1c1c1");
		$(".spotTip").text("此活动为免费活动，名额有限，如需参加请到现场报名。");
	}
	if ($("#priceList").attr("data-soure-price").indexOf("售完") != -1) {
		var disabledArray = $("#priceList").find(".priceLabel").filter(function(){
			return $(this).find("a").text().indexOf("售完")!=-1;
		});
		disabledArray.css("backgroundImage","none").css("border","1px solid #c1c1c1").removeClass("selected");
		if(disabledArray.length === $("#priceList").attr("data-soure-price").split("/").length) {
			$(".spotTip").text("抱歉,此活动名额已完，您可以去瞧瞧其它活动");
		} else {
			$($("#priceList").find(".priceLabel").filter(function(){
			return $(this).find("a").text().indexOf("售完") ==-1;
		})[0]).addClass("selected");
		}
	}
	if($("#priceList").attr("data-soure-price").indexOf("现场") != -1) {
		$(".hiddenByTime").attr("disabled", "disabled");
		$("#priceList").find(".priceLabel").css("backgroundImage","none").css("border","1px solid #c1c1c1");
	}
	if ($(".hiddenByTime").text().indexOf("已过期") != -1) {
		$(".hiddenByTime").attr("disabled", "disabled");
		$("#priceList").find(".priceLabel").css("backgroundImage","none").css("border","1px solid #c1c1c1");
		$(".spotTip").text("此活动已过期，您可以去瞧瞧其它活动");
	}

}
function submitForm() {
	$(".searchInput").on('keyup',
	function(e) {
		if (e.keyCode == 13) {
			$(this).parents("form").submit();
		}
	});
	$("#searchIcon").on('click',
	function() {
		$(this).parents("form").submit();
	});
}
function selectPrice() {
	var priceList = $("#priceList");
	if (priceList.length <= 0) {
		return false;
	} else {
		var dataSp = priceList.attr("data-soure-price");
		if(dataSp == "") {
			dataSp = "待定";
			priceList.attr("data-soure-price",dataSp);
		}
		var priceAry = dataSp.split("/");
		var priceAry2 = dataSp.split("/");
		if(priceAry.length>1) {
			priceAry= priceAry.sort(function(a,b){
			return parseInt(a)-parseInt(b);
		});
		}
		var tmpStr = "";
		if (dataSp != "") {
			if ($.trim(priceList.attr("data-discount-price")) == "") {
				for (var i = 0; i < priceAry.length; i++) {
					if (i == 0) {
						if (priceAry[i].indexOf("售完") != -1) { 
							     ($("<li></li>").append($("<div></div>").addClass("disabledPriceLabel").addClass("priceLabel").addClass("selected").append($("<a></a>").attr("data-disabled", "true").addClass("currentPrice").text(priceAry[i])))).appendTo(priceList);
						} else { ($("<li></li>").append($("<div></div>").addClass("priceLabel").addClass("selected").append($("<a></a>").attr("data-disabled", "false").addClass("currentPrice").text(priceAry[i])))).appendTo(priceList);
						}
					} else {
						if (priceAry[i].indexOf("售完") != -1) { ($("<li></li>").append($("<div></div>").addClass("priceLabel").addClass("disabledPriceLabel").append($("<a></a>").attr("data-disabled", "true").addClass("currentPrice").text(priceAry[i])))).appendTo(priceList);
						} else { ($("<li></li>").append($("<div></div>").addClass("priceLabel").append($("<a></a>").attr("data-disabled", "false").addClass("currentPrice").text(priceAry[i])))).appendTo(priceList);
						}
					}
				}
			} else if ($.trim(priceList.attr("data-discount-price")) != "") {
				var discountPriceAry = priceList.attr("data-discount-price").split("/");
				var dicountAry = priceList.attr("data-discount").split("/");
				while(discountPriceAry.length<priceAry2.length) {
					discountPriceAry[discountPriceAry.length] = priceAry2[discountPriceAry.length];
				}
				discountPriceAry = discountPriceAry.sort(function(a,b){
						return parseInt(a) - parseInt(b);
					});
				var discountHow = "";
				for (var j = 0; j < priceAry.length; j++) {
					discountHow = parseFloat((parseFloat(discountPriceAry[j])/parseFloat(priceAry[j])).toFixed(1)*10).toFixed(1);
					if(parseInt(discountHow) == 10) {
						discountHow = "";
					} else {
						discountHow+="折";
					}
					if (j == 0) {
						if (priceAry[j].indexOf("售完") != -1) {
							$("<li></li>").append($("<div></div>").addClass("priceLabel").addClass("disabledPriceLabel").addClass("selected").append($("<a></a>").css("display", "block").attr("data-disabled", "true").append($("<span></span>")
								.addClass("currentPrice").text(discountPriceAry[j])))).appendTo(priceList);
						} else {
							$("<li></li>").append($("<span></span>").addClass("spanDiscountTip").text(discountHow)).append($("<div></div>").addClass("priceLabel").addClass("discountPriceLabel").addClass("selected").append($("<a></a>").css("display", "block").attr("data-disabled", "false").append($("<span></span>")
								.addClass("currentPrice").text(discountPriceAry[j])).append($("<span></span>")
								.addClass("sourcePrice").text("原价" + priceAry[j])))).appendTo(priceList);
						}
					} else {
						if (priceAry[j].indexOf("售完") != -1) {
							$("<li></li>").append($("<div></div>").addClass("priceLabel").addClass("disabledPriceLabel").append($("<a></a>").css("display", "block").attr("data-disabled", "true").append($("<span></span>")
								.addClass("currentPrice").text(discountPriceAry[j])))).appendTo(priceList);
						} else {
							$("<li></li>").append($("<span></span>").addClass("spanDiscountTip").text(discountHow)).append($("<div></div>").addClass("priceLabel").addClass("discountPriceLabel").append($("<a></a>").css("display", "block").attr("data-disabled", "false").append($("<span></span>")
								.addClass("currentPrice").text(discountPriceAry[j])).append($("<span></span>")
								.addClass("sourcePrice").text("原价" + priceAry[j])))).appendTo(priceList);
						}
					}
				}
			}
			priceList.find("a").on('click',
			function() {
				if ($(this).attr("data-disabled") == "false") {
					priceList.find("div").removeClass("selected");
					$(this).parent("div").addClass("selected");
				}
				return false;
			});
		}
	}
}
function discount() {
	if ($(".discountNum").length > 0) {
		$(".discountNum").each(function() {
			var tmp = $(this);
			var discount = tmp.attr("data-discount").split("/")[0];
			tmp.text(discount + "折");
		});
	}
}
function fillForm() {
	var price = $.trim($("#oneprice .purePrice").text());
	var sourcePrice = "";
	var sourceTotalPrice = "";
	if($.trim($("#oneprice .purePrice").attr("data-price")) !="") {
		sourcePrice = $("#oneprice .purePrice").attr("data-price"); 
	}
	if (price == "") {
		$(".totalMoney .purePrice").text("0");
	} 
	var num = 1;
	$("#total_num").attr("value", num);
	$("#ticketNum").change(function() {
		if (price != "") {
			var totalPrice = (parseFloat($.trim($("#oneprice .purePrice").text())) * parseInt($("#ticketNum")[0].value)).toFixed(2);
			if(sourcePrice != "") {
				sourceTotalPrice = (parseFloat( $("#oneprice .purePrice").attr("data-price"))*parseInt($("#ticketNum")[0].value)).toFixed(2);;
				$(".totalMoney .purePrice").attr("data-price",sourceTotalPrice);
			}
			$(".totalMoney .purePrice").text(totalPrice);
		}
		num = parseInt($("#ticketNum")[0].value);
		$("#total_num").attr("value", num);
	});
	if($("#transformMoney").length>0) {
		$("#transformMoney").toggle(function(){
			var tmpPrice = $("#oneprice .purePrice").text();
			$("#oneprice .purePrice").text($("#oneprice .purePrice").attr("data-price"));
			$("#oneprice .purePrice").attr("data-price",tmpPrice);
			$("#oneprice .priceUnit").text("(人民币)");
			var totalTmpPrice = $($(".totalMoney .purePrice")[0]).text();
			$(".totalMoney .purePrice").text($(".totalMoney .purePrice").attr("data-price"));
			$(".totalMoney .purePrice").attr("data-price",totalTmpPrice);
			$(".totalMoney .priceUnit").text("(人民币)");

		},function(){
			var tmpPrice = $("#oneprice .purePrice").text();
			$("#oneprice .purePrice").text($("#oneprice .purePrice").attr("data-price"));
			$("#oneprice .purePrice").attr("data-price",tmpPrice);
			$("#oneprice .priceUnit").text("("+$("#oneprice .priceUnit").attr("data-unit")+")");
			var totalTmpPrice = $($(".totalMoney .purePrice")[0]).text();
			$(".totalMoney .purePrice").text($(".totalMoney .purePrice").attr("data-price"));
			$(".totalMoney .purePrice").attr("data-price",totalTmpPrice);
			$(".totalMoney .priceUnit").text("("+$("#oneprice .priceUnit").attr("data-unit")+")");
		});
	}
}
function countTimeStr() {
	if ($("#endTime").length > 0) {
		var dateValue = $("#endTime").attr("data-time");
		countDown("endTime","timeTag", dateValue);
	}
}
function crumbsTag() {
	var crumbsTag = $(".crumbsTag");
	if (crumbsTag.length <= 0) {
		return false;
	} else {
		var strtmp = "";
		var strArr = null;
		for (var i = 0; i < crumbsTag.length; i++) {
			strArr = ($(crumbsTag[i]).attr("data-tag")).split("/");
			for (var j = 0; j < strArr.length; j++) {
				if (j < strArr.length - 1) {
					strtmp += "<li><a href=\"" + (strArr[i].split("$"))[0] + ">" + (strArr[i].split("$"))[1] + "</a></li>";
				} else {
					strtmp += "<li><span class=\"currentStage\">" + (strArr[i].split("$"))[1] + "</span></li>";
				}
			}
			$(crumbsTag[i]).parent("ul").html(strtmp);
		}
	}
}
function parseUrl() {
	var url = window.location.href;
	var length = url.length;
	var index = url.indexOf("order");
	var event_id = parseInt(url.substring(index + 6, length - 1));
	$("#event_id").attr("value", event_id);
}
function shotPrice() {
	if ($(".picPrice").length > 0) {
		$(".picPrice").each(function() {
			var tmp = $(this);
			var styleprice = $(this).attr("data-priceStyle");
			if (tmp.text().indexOf("/") != -1) {
				tmp.text(tmp.text().split("/")[0]);
			}
			if (tmp.text().indexOf("收费") != -1) {
				tmp.text("收费");
			}
			if (tmp.text().indexOf("免费") != -1) {
				tmp.text("免费");
			}
			if (tmp.text().indexOf("待定") != -1) {
				tmp.text("待定");
			}
			if ($.trim(tmp.text()) == "") {
				tmp.text("待定");
			}
			if($.trim(tmp.text()) !== "" && $.trim(tmp.text()) !== "收费" && $.trim(tmp.text()) !== "免费" && $.trim(tmp.text()) !== "待定") {
				tmp.append($("<span class='styleprice'>"+styleprice+"</span>"));
			}
		});
	}
}

//清除在分页时多余的li标签(暂时不清除这是怎么造成的，只能先用js清理)
function clearMoreTagByPaginationWrapper() {
	if($(".dhd_pagination").length>0) {
		$(".dhd_pagination").each(function(){
			var liArray = $(".dhd_pagination").find("li");
			for(var i=0;i<liArray.length;i++) {
				if($.trim($(liArray[i]).html() ) == "") {
					liArray[i].remove();
				}
			}
		});
	}
}
//元素距离浏览器【底部】的距离，传入参数为ID
function scrollBottomDistance(mark){
	var markObj = $("#"+mark);
	var markTop = markObj.offset().top;//标记距顶部的高度
	var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;//卷去的高度
	var winHeight = document.documentElement.clientHeight;//浏览器窗口高度
	var intDistance=markTop-scrollTop-winHeight;//底部到标记的距离
	return intDistance;
}
//元素距离浏览器【顶部】的距离，传入参数为ID
function scrollTopDistance(mark){
	var markObj = $("#"+mark);
	var markTop = markObj.offset().top;//标记距顶部的高度
	var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;//卷去的高度
	var intDistance=markTop-scrollTop;
	return intDistance;
}

function returnTop() {
	$backToTopEle = $('<div class="backToTop"><i class="iconfont" style="font-size:24px">&#xe60c;</i></div>').appendTo($("body")).click(
		function() {
	        $("html, body").animate({ scrollTop: 0 }, 300);
		}), 
	    $backToTopFun = function() {
	      var st = $(document).scrollTop(), winh = $(window).height();
	      (st > 0)? $backToTopEle.show(): $backToTopEle.hide();
	      (st > 0)? $home.show(): $home.hide();
	      //IE6下的定位
	      if (!window.XMLHttpRequest) {
	        $backToTopEle.css("top", st + winh - 126);
	          $home.css("top", st + winh - 86);
	      }
	   };
	$home = $('<div class="home"><a href="/" target="_blank"><i class="iconfont" style="font-size:24px">&#xf0001;</i></a></div>').appendTo($("body"));
	$(window).bind("scroll", $backToTopFun);
	$backToTopFun();
}
function GetRandomNum(Min,Max)
{   
  var Range = Max - Min;   
  var Rand = Math.random();   
  return(Min + Math.round(Rand * Range));   
}   
function formatTime(i) {
  if(i < 10) {
    i = "0" + i;
  }
  return i;
}
function changeListStatus() {
	var jumbotronListItem = $(".jumbotronListItem");
	var length = jumbotronListItem.length;
	var i=0;
	var change = function() {
		i++;
		var k = i%length;
		jumbotronListItem.removeClass("active").eq(k).addClass("active");
	}
	setInterval(change,5000);
}
function replaceStr(replaceStr,tmp) {
	var strArray = replaceStr.split(",");
	for(var i=0;i<strArray.length;i++) {
		if(strArray[i] === tmp) {
			strArray.splice(i,1);
			break;
		}
	}
	return strArray.join(",");
}
function selectSubscription() {
	if($(".subscriptionList span").length>0) {
		var strSelected = $("#selectedSub").attr("value");
	    $(".subscriptionList span").bind("click",function(){
	      var selectedValue = $(this).text();
		  if($(this).hasClass("selected")) {
			$(this).removeClass("selected");
			if(strSelected.indexOf(selectedValue) != -1) {
				strSelected = replaceStr(strSelected,selectedValue);
			}
		  } else {
			$(this).addClass("selected");
			strSelected += selectedValue+",";
		  }
		  $("#selectedSub").attr("value",strSelected);
	    });
	     $("#subscriptionRow").click(function(e){
	     	if(e.target.nodeName.toLowerCase() === "span") {
	     		var $spanTarget = $(e.target);
	     		var selectedValue = $spanTarget.text();
	     		if($spanTarget.hasClass("selected")) {
	     			$spanTarget.removeClass("selected");
	     			if(strSelected.indexOf(selectedValue) !=-1) {
	     				strSelected = replaceStr(strSelected,selectedValue);
	     			}
	     			$spanTarget.parent().css("borderColor","#d8d8d8").find(".subscriptionIcon").hide();
	     		} else {
	     			$spanTarget.addClass("selected");
	     			strSelected += selectedValue + ",";
	     			$spanTarget.parent().css("borderColor","#2c3e50").find(".subscriptionIcon").show();
	     		}
	     		$("#selectedSub").attr("value",strSelected);
	     	}
	     });
	     $(".subscriptionList li").mouseenter(function(){
	     	if(!$(this).find("span").hasClass("selected")) {
	     	  $(this).css("borderColor","#2c3e50").find(".subscriptionIcon").show();
	     	}
	     });
	      $(".subscriptionList li").mouseleave(function(){
	      	if(!$(this).find("span").hasClass("selected")) {
	      	$(this).css("borderColor","#d8d8d8").find(".subscriptionIcon").hide();
	      	}
	     }); 
	}
}
$(document).ready(function() {
	$("#changecityHead").hover(function() {
		$("#changecityHead a span").addClass("transform");
		$("#cityMap").css("left","0");
	  },function() {
		$("#changecityHead a span").removeClass("transform");
		$("#cityMap").css("left","-10000px");
	});
	selectPrice();
	crumbsTag();
	var moreRecom = $(".moreRecom");
	if (moreRecom.length > 0) {
		moreRecom.click(function() {
			var that = this;
			$(this).siblings("div").slideDown('normal',function() {
				$(that).hide();
			});
		});
	}
	if($("#priceList").length>0) {
		disabledBtn();
	}
	$(".submitBtn").on("click",
	function() {
		var myprice = 0;
		if ($("#myPrice").length > 0 && parseFloat($("#myPrice")[0].value)) {
			myprice = parseFloat($("#myPrice")[0].value);
		}
		var selectedPrice = $(".priceLabel.selected").find(".currentPrice").text();
		if($(".priceLabel.selected").find(".currentPrice").length>0) {
			var rawPrice = $(".priceLabel.selected").find(".sourcePrice").text().substring(2);
			$("#rawPrice").attr("value",rawPrice);
		}
		if (myprice == 0 && parseFloat(selectedPrice)) {
			$("#myPrice").attr("value", parseFloat(selectedPrice));
		} else {
			$("#myPrice").attr("value", myprice);
		}
		$("#priceForm").submit();
	});
	if($("#oneprice").length>0) {
		fillForm();
	}
	parseUrl();
	//fillModal();
	submitForm();
	discount();
	shotPrice();
	$("#centerSearchIcon").click(function() {
		$(this).parent("form").submit();
	  });
	function bindClick1() {
		var elemClone = $("#contactModal").clone();
		$("#guestMessageButton").click(function(){
		    dialog({
			title:'留言咨询',
			content:elemClone,
			id:'questionMessage'
			}).showModal();
			$(".questionForm").validation();
	  	});
	  	$(".modal-body #contactModal").remove();
	}
	function bindClick2() {
	  var elemClone2 = $("#suggestionModal").clone();
	  $("#suggestionButton").click(function(){
	  	dialog({
	  		title:'检查纠错',
	  		content:elemClone2,
	  		id:'suggestionMessage'
	  	}).showModal();
	  	$(".suggestionForm").validation();
	  })
	  $(".modal-body #suggestionModal").remove();
	}
	if($("#guestMessageButton").length>0) {
	 bindClick1();
	}
	if($("#suggestionModal").length>0) {
	  bindClick2();
	}
	if ($(".slideLi").length > 0) {
		$(".slideLi").each(function(){
			$(this).parent().css("paddingLeft","0");
			if($(this).parent().find("ul").find("li").length<=0) {
				$(this).parent().css("paddingLeft",".6em");
				//$(this).parent().parent().css({"paddingTop":".5em","paddingBottom":".5em"})
				$(this).remove();
			} 
		});
		$(".slideLi").toggle(function() {
			var lls = $(this).parent().find("li");
			lls.slideUp();
		},
		function() {
			var lls = $(this).parent().find("li");
			lls.slideDown();
		});
	}
	returnTop();
	/*if($(".wx_qrcode").length>0 && $(".wx_qrcode").css("display").indexOf("block") ==-1) {
		$(".wx_qrcode").mouseenter(function(){
			var thisTop = $(this).offset().top;
			var thisLeft = $(this).offset().left;
			$("#bigWxCode").show();
			$("#bigWxCode").offset({ top: thisTop,left:thisLeft });
		});
		$("#bigWxCode").mouseleave(function(){
			$("#bigWxCode").hide();
		});
	}*/
	if($(".backToTop").css("display") !="none" && $("#textMark").length>0) {
		  window.onscroll = function(){
		  	var newSbd=scrollTopDistance("textMark");
			if(newSbd<= 0){
				$("#tabDiv .nav-tabs").addClass("fixedNav");
				$(".blank_block").show();
			  }else{
				$("#tabDiv .nav-tabs").removeClass("fixedNav");
				$(".blank_block").hide();
			  }
	   		}
		}
	if($(".canjiaNum").length>0) {
		$(".canjiaNum").each(function(){
			$(this).html(GetRandomNum(30,100)+"<span style='color:#b5b5b5;'>人参加</span>");
		})
	}
	if($(".likeNum").length>0) {
		$(".likeNum").each(function(){
			$(this).html(GetRandomNum(50,200)+"<span style='color:#b5b5b5;'>人喜欢</span>");
		});
	}
	if($(".tagNum").length>3) {
		var tagNumArray = $(".tagNum");
		for(var i=3;i<tagNumArray.length;i++) {
			$(tagNumArray[i]).css({"color":"#fff","backgroundColor":"#bbb"});
		}
	}
	if($(".crowdingDiv").length>0 && $("#beginPrice").length>0&& $("#endPrice").length>0) {
		var beginPrice = $("#beginPrice").text().substring(1);
		beginPrice = parseInt(beginPrice);
		var endPrice = $("#endPrice").text().substring(1);
		endPrice = parseInt(endPrice);
		var ss = 3;
		if( beginPrice !=0) {
			var ss = (parseInt(beginPrice)/parseInt(endPrice))*100;
		}
		$(".crowdingInnerDiv").css("width",ss+"%").attr("aria-valuenow",ss).find("sr-only").text("已筹集:"+ss+"%");
		if($("#timeH").length>0) {
			var leftTime = 0;
			var todyDay = new Date();
			var endTime = new Date($("#timeH").attr("data-end-time"));
			//获得距离规定时间的毫秒数
       		 var level1 = endTime.getTime() - todyDay.getTime();
        	//获得相差天数
        	var date =formatTime(Math.floor(level1/(24*3600*1000)));        	
        	$("<h5>剩余时间</h5>").appendTo($("#timeLeft"));
        	$("<h5></h5>").text(date+"天").appendTo($("#timeLeft"));
		}
	}
	countTimeStr();
	if($(".tagDiv").length>0) {
		$(".tagDiv").hover(function(){
			$(".tagDiv").removeClass("selectedTagDiv");
			$(this).addClass("selectedTagDiv");
		},function(){
			$(this).removeClass("selectedTagDiv");
		});
	}
	if($("#return").length>0) {
		var href=  window.location.href.replace("order/","event-");
		href = href.substring(0,href.length-1)+".html";  
		$("#return").attr("href",href);
	}

	if($("#ticketNum").length>0) {
		$("#ticketNum").blur(function(){
			var price = parseInt($(this).val());
			if (price) {
				$(this).attr("value", price);
			} else {
				$(this).attr("value", 1);
			}
			$("#ticketNum").trigger("change");
		});
		$("#ticketNum").trigger("change");
	}
	if($(".clickNum").length>0) {
		$("#minus").click(function(){
			var price = parseInt($("#ticketNum").val())-1;
			if(price<=0) {
				price = 1;
			}
			$("#ticketNum").attr("value",price);
			$("#ticketNum").trigger("change");
		});
		$("#plus").click(function(){
			var price = parseInt($("#ticketNum").val())+1;
			$("#ticketNum").attr("value",price);
			$("#ticketNum").trigger("change");
		});
	}
	if($(".telphoneA").length>0) {
		$(".telphoneA").attr("href","tel:4000033721");
	}
	if($("#captcha").length>0) {
		$("#captcha").blur(function(){
			var value = $(this).val();
			var url = '/verify_captcha/';
			if($.trim(value) != "" && $("#captcha").attr("btvd-el") == undefined) {
			  $.ajax({type:"post",url:url,data:{captcha:value},async:false,success:function(data){
				var flag = jQuery.parseJSON(data).flag;
				if(flag === "false") {
					$("#captcha").attr("btvd-el","errorValidateCode");
					$("#captcha").trigger("blur");
				}
			  	}});
			}
		});
		$("#captcha").change(function(){
			$("#captcha").removeAttr("btvd-el");
		});
	}
	if($("#captchaImg").length>0) {
		$("#captchaImg").trigger('click');
	}
	if($(".spotTip").length>0) {
		var dataTip = $(".spotTip").attr("data-tip");
		if(dataTip == 2 || dataTip == 3) {
			$(".spotTip").hide();
		}
	}
	if($("#colorColumn").length>0) {
		var leftSide = $("#colorColumn .inner_wrapper").eq(0).find(".col-md-6").clone();
		var rightSide = $("#colorColumn .inner_wrapper").eq(1).find(".col-md-6").clone();
		var leftLength = leftSide.length;
		var rightLength = rightSide.length;
		if((leftLength+rightLength<9) || ((leftLength+rightLength)>8 && Math.abs(leftLength-rightLength)>3)) {
			leftSide.removeClass("col-md-6").addClass("col-md-4");
			rightSide.removeClass("col-md-6").addClass("col-md-4");
			var hrefSpecial = $("#colorColumn .inner_wrapper").eq(0).find("h2 a").attr("href");
			$("#colorColumn").find("*").remove();
			$("#colorColumn").append($("<div class='inner_wrapper'></div>").append($("<h2></h2>").append($("<a></a>").attr("target","_blank").attr("href",hrefSpecial).text("玩乐活动"))).append($("<h3>玩所未玩，精彩没有上限</h3>").append($("<a></a>").attr("target","_blank").attr("href",hrefSpecial).text("更多"))).append($("<div class='row'></div>").append(leftSide).append(rightSide)));
		}
		/*如果是主页 需要倒序遍历菜单栏*/
		var navUl = $("#navUl");
		var lis = $("#navUl").find("li");
		var cloneNavLi = new Array();
		for(var u=0; u<lis.length;u++) {
			cloneNavLi[u] = lis[u];
		}
		navUl.find("li").remove();
		for(var k=cloneNavLi.length-1;k>0;k--) {
			navUl.append(cloneNavLi[k]);
		}
	}
	if($(".spotTab").length>0) {
		$(".spotTab").find("a").attr("target","_blank");
	}
	if($(".payAttention .weixing").length>0) {
		$(".payAttention .weixing").hover(function(){
			$(".weixingImg").addClass("transform");
		},function(){
			$(".weixingImg").removeClass("transform");
		})
	}
	if($("#categoryList").length>0) {
		createListBySelected();
	}

	selectSubscription();
	if($("#submitOrder").length>0) {
		$("#subscriptionAlert").hide();
		$("#submitOrder").bind('click',function(){
			if($("#selectedSub").attr("value") != "" || $("#customerKeywords").attr("value")!="") {
				$("#subscriptionForm").submit();
			} else {
				$("#subscriptionAlert").show();
			}
		});
	}
	if($("#tabDiv").length>0) {
		$("#tabDiv .tab-content .tab-pane").hide();
		$("#tabDiv .tab-content .active").show();
		$("#tabDiv .nav-tabs li").click(function(){
			$("#tabDiv .nav-tabs li").removeClass('active');
			$(this).addClass('active');
			var target = $(this).find("h2").attr("href").substring(1);
			$("#tabDiv .tab-content .tab-pane").hide();
			$("#tabDiv .tab-content .tab-pane").removeClass("active");
			$("#tabDiv").find("#"+target).addClass("active");
			$("#tabDiv .tab-content .active").show();
		})
	}
});


function bindListA(tmpId) {
	$(".secondLevelUl").hide();
	var relativeId = "";
	if(tmpId.target) {
		relativeId = $(tmpId.target).attr("id");
	} else {
		relativeId = tmpId;
	}
	$(".secondLevelUl").filter(function(){
		return $(this).attr("data-id") == relativeId;
	}).show();
}
function createListBySelected() {
	var selectedFlag = false;
		var selectedLi = null;
		var levelFlag = 0;
		var secondUL = $("#categoryList>ul").eq(1);
		var cloneList = {};
		var firstObject = {};
		var secondArray = [];
		var secondLength = 0;
		var tmp1 = null;
		var tmp2 = null;
		var tmp3 = null;
		var tmp4 = null;
		var tmp5 = null;
		var tmp6 = null;
		var parent = null;
		secondUL.find("li").each(function(){
			if($(this).hasClass("selected")) {
				selectedFlag = true;
				selectedLi = $(this);
			}
			if( $(this).hasClass("selectedUl")) {
				selectedFlag = true;
				selectedLi = $(this);
				levelFlag = 1;
			}
		});
		if(levelFlag != 1) {
		  if(selectedFlag == true) {
			if(selectedLi.find(">ul").length < 1) {
				levelFlag = 3;
			} else {
				if(selectedLi.find(">ul>li>>ul").length<1) {
					levelFlag = 2;
				}
			}
		  }
		}
		if(levelFlag == 1) {
			parent = selectedLi;
		}
		if(levelFlag == 2) {
			parent = selectedLi.parent("ul").parent("li");
		}
		if(levelFlag == 3) {
			parent = selectedLi.parent("ul").parent("li").parent("ul").parent("li");
		}
		if(parent != null) {
          firstObject.name = parent.find(">a").text();
          firstObject.href = parent.find(">a").attr("href");
		  tmp1 = parent.find(">ul>li");
		  secondLength = tmp1.length;
		  for(var i=0;i<secondLength;i++) {
		 	tmp2 = tmp1.eq(i);
		 	tmp3 = {};
		 	tmp3.name = tmp2.find(">a").text();
		 	tmp3.href = tmp2.find(">a").attr("href");
		 	tmp3.objectArray = [];
		 	tmp4 = tmp2.find(">ul>li");
		 	if(tmp4.length>0) {
		 	  for(var j=0;j<tmp4.length;j++) {
		 	  	tmp5 = tmp4.eq(j);
		 	  	tmp6 = {};
		 	  	tmp6.name = tmp5.find(">a").text();
		 	  	tmp6.href = tmp5.find(">a").attr("href");
		 	  	tmp3.objectArray[j] = tmp6;
		 	  } 
		 	}
		 	secondArray[i] = tmp3;
		  }
		  firstObject.arrayObject = secondArray;
		}
		if(firstObject.arrayObject.length>0) {
			var fillDivArea = $("<div></div>").addClass("listArea").addClass("clearfix");
			var fillList = $("<ul></ul>").addClass("firstLevelUl");
			fillDivArea.append(fillList);
			var fillListSec = $("<ul></ul>").addClass("secondLevelUl");
			fillDivArea.append(fillListSec);
			var fillObjectArray = firstObject.arrayObject;
			for(var k=0;k<fillObjectArray.length;k++) {
				if(k == 0) {
				  $("<li></li>").append($("<a></a>").text("所有").css("color","#000")).appendTo(fillList);
				}
				var fillObject = fillObjectArray[k];
				var tmpId = "fillLi"+k;
				var tmpa =$("<a></a>");
				tmpa.html(fillObject.name).attr("id",tmpId).attr("href",fillObject.href);
				$("<li></li>").append(tmpa).appendTo(fillList);
				if(fillObject.objectArray.length>0) {
					var fillObjectArraySec = fillObject.objectArray;
					for(var h=0;h<fillObjectArraySec.length;h++) {
						var fillObjectSec = fillObjectArraySec[h];
						$("<li></li>").append($("<a></a>").text(fillObjectSec.name).attr("href",fillObjectSec.href)).appendTo(fillListSec.attr("data-id",tmpId));
					}
				}
			}
			fillDivArea.insertAfter("ul.navigationUlist");
			var selectedLiText = "";
			var relativeId = "";
			$("#categoryList>ul").eq(1).find("li").each(function(){
				if($(this).hasClass("selected")) {
					selectedLiText = $(this).find(">a").text();
				}
			})
			$(".listArea a").each(function(){
				if($(this).text() == selectedLiText) {
					$(this).css("color","#428bca");
					if($(this).parent("li").parent("ul").hasClass("firstLevelUl")) {
						relativeId = $(this).attr("id");
					} else {
						relativeId = $(this).parent("li").parent("ul").attr("data-id");
					}
					
				}
			});
			if(parent) {
				var parentClone = parent.clone();
				parent.remove();
				$("#categoryList>ul").eq(1).prepend(parentClone);
			}
			$("#"+relativeId).css("color","#428bca");
			bindListA(relativeId);
			//$(document).on('click','.firstLevelUl>li>a',bindListA);
		}
}