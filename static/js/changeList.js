$(function(){
    $(parent.document.getElementById("pageLoader")).hide();
    $("#beginTime").attr('value',$("#beginTimeDefault").attr('value'));
    $("#endTime").attr('value',$("#endTimeDefault").attr('value'));
    tmpArgsMap = {
      '%E4%BF%A1%E6%81%AF%E5%91%981':'信息员1',
      '%E4%BF%A1%E6%81%AF%E5%91%98':'信息员2',
      '%E5%86%AF%E7%A5%96%E4%B8%BD':'冯祖丽',
      '%E5%88%98%E4%B8%B9':'刘丹',
      '%E5%88%98%E5%86%AC':'刘冬',
      '%E5%88%98%E6%AC%A3':'刘欣',
      '%E5%90%B4%E6%A5%A0':'吴楠',
      '%E5%90%B4%E8%8C%9C':'吴茜',
      '%E5%91%A8%E4%B8%B9':'周丹',
      '%E5%B4%94%E4%B8%BD%E5%90%9B':'崔丽君',
      '%E5%B7%AB%E7%A7%80%E5%A8%9F':'巫秀娟',
      '%E5%BC%A0%E5%A9%89%E9%92%B0':'张婉钰',
      '%E6%96%87%E8%90%83':'文萃',
      '%E6%9B%B9%E4%BC%9F':'曹伟',
      '%E6%9B%B9%E6%B0%B8%E7%90%B4':'曹永琴',
      '%E6%9C%B1%E7%82%9C':'朱炜',
      '%E6%9D%8E%E4%BA%91%E7%9A%93':'李云皓',
      '%E6%9E%97%E6%A5%A0':'林楠',
      '%E7%8E%8B%E5%B7%A7%E6%85%A7':'王巧慧',
      '%E7%8E%8B%E5%B9%B3':'王平',
      '%E7%A7%A6%E5%B7%9D%E7%BF%94':'秦川翔',
      '%E7%A8%8B%E6%A2%A6%E5%B2%9A':'程梦岚',
      '%E7%AC%A6%E4%BF%8A':'符俊',
      '%E7%BD%97%E9%9D%99':'罗静',
      '%E8%8B%8F%E8%83%9C%E6%B3%A2':'苏胜波',
      '%E8%94%A1%E7%9D%BF':'蔡睿',
      '%E8%B0%A2%E4%B9%83%E6%80%A1':'谢乃怡',
      '%E8%B0%A2%E6%88%90%E6%9E%97':'谢成林',
      '%E8%B5%B5%E4%BC%9F%E6%9D%B0':'赵伟杰',
      '%E9%BB%84%E7%80%9A':'黄瀚'
    }
    if($('#timeList').length>0) {
      $('#timeList').find('a').click(function(){
        var storgeCondition = {};
        $("#filterGroup select").each(function(){
          var selectedOptionValue = $(this).val();
          if(selectedOptionValue !='?' ) {
            selectedOptionValue = selectedOptionValue.substring(1);
            if(selectedOptionValue.indexOf('&') !=-1) {
              var argsArray = selectedOptionValue.split('&');
              for(var i=0;i<argsArray.length;i++) {
                if(argsArray[i].indexOf('isshow__id__exact=') !=-1 ||argsArray[i].indexOf('edit_name=') !=-1 || argsArray[i].indexOf('edit_state=') !=-1 || argsArray[i].indexOf('event_isshow__exact=') !=-1 ||argsArray[i].indexOf('point__id__exact=') !=-1 || argsArray[i].indexOf('last_edit__id__exact=') !=-1 || argsArray[i].indexOf('city_p=') !=-1 || argsArray[i].indexOf('cat_p=') !=-1 || argsArray[i].indexOf('city_p=') !=-1 || argsArray[i].indexOf('date_state=') !=-1 || argsArray[i].indexOf('price_type=') !=-1 || argsArray[i].indexOf('begin_time__lt=') !=-1||argsArray[i].indexOf('edit_p')!=-1) {
                  var tmpStr  = argsArray[i];
                  var key = tmpStr.split('=')[0];
                  var value = tmpStr.split('=')[1];
                  if(key in storgeCondition) {
                    ;
                  } else {
                    if(key == $(this).attr('name')) {
                      if(argsArray[i].indexOf('edit_p') !=-1) {
                        value = tmpArgsMap[value];
                      }
                      storgeCondition[key] = value;
                    }
                  }
                }
              }
            } else {
              var tmpObj = {};
              var key = selectedOptionValue.split('=')[0];
              var value = selectedOptionValue.split('=')[1];
              if(key == $(this).attr('name')) {
                if(key.indexOf('edit_p') !=-1) {
                  value = tmpArgsMap[value];
                }
               storgeCondition[key] = value;
              } else {
                if(key in storgeCondition) {
                    ;
                } else {
                      if(key.indexOf('edit_p') !=-1) {
                        value = tmpArgsMap[value];
                      }
                     storgeCondition[key] = value;
                }
              }
            }
          }
        });
        var href = $(this).attr('href');
        for(key in storgeCondition) {
          if(storgeCondition.hasOwnProperty(key)) {
            var value = storgeCondition[key];
            var inputDom = $("<input type='hidden'>").attr('name',key).attr('value',value).appendTo($('#eventForm'));
            href += '&'+key+'='+value;
          }
        }
        $(this).attr('href',href);
        return true;
      })
    }
    $('input').each(function(){
      if(!$(this).hasClass('form-control') && $(this).attr('type')!='checkbox') {
        $(this).addClass('form-control');
      }
    })
    $('select').each(function(){
      if(!$(this).hasClass('form-control')) {
        $(this).addClass('form-control');
      }
    })
    $("#id_form-MAX_NUM_FORMS").attr('value',100);
    $("#searchWidhCondition").click(function(){
      var storgeCondition = {};
      $("#filterGroup select").each(function(){
        var selectedOptionValue = $(this).val();
        if(selectedOptionValue !='?' ) {
          selectedOptionValue = selectedOptionValue.substring(1);
          if(selectedOptionValue.indexOf('&') !=-1) {
            var argsArray = selectedOptionValue.split('&');
            for(var i=0;i<argsArray.length;i++) {
               if(argsArray[i].indexOf('isshow__id__exact=') !=-1 || argsArray[i].indexOf('create_time__year=') !=-1  || argsArray[i].indexOf('create_time__month=') !=-1 || argsArray[i].indexOf('create_time__day=') !=-1 ||argsArray[i].indexOf('edit_name=') !=-1 || argsArray[i].indexOf('edit_state=') !=-1 || argsArray[i].indexOf('event_isshow__exact=') !=-1 ||argsArray[i].indexOf('point__id__exact=') !=-1 || argsArray[i].indexOf('last_edit__id__exact=') !=-1 || argsArray[i].indexOf('city_p=') !=-1 || argsArray[i].indexOf('cat_p=') !=-1 || argsArray[i].indexOf('city_p=') !=-1 || argsArray[i].indexOf('date_state=') !=-1 || argsArray[i].indexOf('price_type=') !=-1 || argsArray[i].indexOf('begin_time__lt=') !=-1||argsArray[i].indexOf('edit_p')!=-1) {
                var tmpStr  = argsArray[i];
                var key = tmpStr.split('=')[0];
                var value = tmpStr.split('=')[1];
                if(key in storgeCondition) {
                  ;
                } else {
                  if(key == $(this).attr('name') || key == 'create_time__year'|| key == 'create_time__month'|| key == 'create_time__day') {
                    if(argsArray[i].indexOf('edit_p') !=-1) {
                      value = tmpArgsMap[value];
                    }
                    storgeCondition[key] = value;
                  }
                }
              }
            }
          } else {
            var tmpObj = {};
            var key = selectedOptionValue.split('=')[0];
            var value = selectedOptionValue.split('=')[1];
            if(key == $(this).attr('name')) {
              if(key.indexOf('edit_p') !=-1) {
                value = tmpArgsMap[value];
              }
             storgeCondition[key] = value;
            } else {
              if(key in storgeCondition) {
                  ;
              } else {
                    if(key.indexOf('edit_p') !=-1) {
                      value = tmpArgsMap[value];
                    }
                   storgeCondition[key] = value;
              }
            }
          }
        }
      });
      for(key in storgeCondition) {
        if(storgeCondition.hasOwnProperty(key)) {
          var value = storgeCondition[key];
          var inputDom = $("<input type='hidden'>").attr('name',key).attr('value',value).appendTo($('#eventForm'));
        }
      }
      $('#eventForm').submit();
    });
    if($("#action-toggle").length>0) {
      $("#action-toggle").click(function(){
        if($("#action-toggle")[0].checked) {
            $("#action-toggle").parents("table").find(".action-select").each(function(){
              this.checked = true;
              var checkboxValue = $(this).val();
              $('input[type="hidden"][value='+checkboxValue+']').attr('type','text').css('display','none');
            })
        } else {
            $("#action-toggle").parents("table").find(".action-select").each(function(){
              this.checked = false;
            })
        }
      });
    }
    $('.action-select').click(function(){
      var checkboxValue = $(this).val();
      if(this.checked) {
        $('input[type="hidden"][value='+checkboxValue+']').attr('type','text').css('display','none');
      } else {
        $('input[type="text"][value='+checkboxValue+']').attr('type','hidden');
      }
    })
    $(".form_datetime").datetimepicker({});
    $("#result_list>tbody>tr>th>a").on('click',function(){
      if(!$(this).hasClass('event_edit')) {
        var tmp = $(this);
        addRemoveTab(tmp);
        return false;
      }
    });
    addNewEvent();
    if($("#iconFresh").length>0) {
      var parentTmp = parent.window.document;
      var tmpHref = $(parentTmp).find(".tab-pane.active").find('iframe').attr('src');
       $("#iconFresh").attr('href',tmpHref);
    }
    var parentTmp = parent.window.document;
    var activeId = $(parentTmp).find("#tabDiv .rightListFrame li.active a").attr('href');
    if(activeId.indexOf('tab') == -1) {
      $(parentTmp).find("#tabDiv .rightListFrame li.active").addClass('remove').removeClass('active');
      $(parentTmp).find("#tabDiv .tab-content .active").addClass('remove').removeClass('active'); 
      $(parentTmp).find("#tabDiv .rightListFrame li:first-child").addClass('active');
      $(parentTmp).find("#tabDiv .tab-content .tab-pane:first-child").addClass('active');
      $(parentTmp).find("#tabDiv .rightListFrame li.remove").remove();
      $(parentTmp).find("#tabDiv .tab-content .remove").remove();
    }
  })
function addRemoveTab(tmp){
        var isAgain = false;
        var parentTmp = parent.window.document;
        var tmpHref = tmp.attr("href");
        var keyId = getNumberFormUrl(tmpHref);
        $(parentTmp).find("#tabDiv ul.rightListFrame li a").each(function(){
          if(getNumberFormUrl(tmp.attr("href")) === $(this).attr("href").substring(1)) {
            isAgain = true;
          }
        });
        if(!isAgain ) {
          $(parentTmp).find("#tabDiv .rightListFrame li").removeClass("active");
          $(parentTmp).find("#tabDiv .tab-content .tab-pane").removeClass("active");
          $("<li></li>").addClass("active").append($("<a></a>").append($("<span></span>").text(tmp.text()).addClass('textSpan')).attr("href","#"+keyId).attr("data-toggle","tab").append($("<span class='icon-remove removeTab'></span>").bind('click',tabClick))).appendTo($(parentTmp).find("#tabDiv ul.rightListFrame"));
          $("<div></div>").addClass("tab-pane").addClass("active").attr("id",keyId).append($("<iframe></iframe>").css({"width":"100%","height":"2722px"}).attr("marginheight",0).attr("marginwidth",0).attr("scrolling","no").attr("frameborder","no").
            attr("name","iframepage").attr("src",tmp.attr("href"))).appendTo($(parentTmp).find("#tabDiv .tab-content"));
          $(parent.document.getElementById("pageLoader")).show();
           // iFrameHeight("iFrame"+tmp.attr("data-name"));
        } else {
          $(parentTmp).find("#tabDiv .rightListFrame li").removeClass("active");
          $(parentTmp).find("#tabDiv .tab-content .tab-pane").removeClass("active");
          $(parentTmp).find("#tabDiv").find("a[href="+"#"+keyId+"]").parent("li").addClass("active");
          $(parentTmp).find("#"+keyId).addClass("active");
        }
      }
function addNewEvent() {
  $("#addNewEvent").click(function(){
    var parentTmp = parent.window.document;
    $(parentTmp).find("#tabDiv .rightListFrame li").removeClass("active");
    $(parentTmp).find("#tabDiv .tab-content .tab-pane").removeClass("active");
    var maxIndex = 0;
    $(parentTmp).find("#tabDiv .rightListFrame li a").each(function(){
      if($(this).attr('href').indexOf('addNewEvent') !=-1) {
        maxIndex++;
      }
    });
    var indexFoText = maxIndex+1;
    var keyId = 'addNewEvent'+maxIndex;
    $("<li></li>").addClass("active").append($("<a></a>").append($("<span></span>").text('新增数据'+indexFoText).addClass('textSpan')).attr("href","#"+keyId).attr("data-toggle","tab").append($("<span class='icon-remove removeTab'></span>").bind('click',tabClick))).appendTo($(parentTmp).find("#tabDiv ul.rightListFrame"));
    $("<div></div>").addClass("tab-pane").addClass("active").addClass('addNewEvent').attr("id",keyId).append($("<iframe></iframe>").css({"width":"100%","height":"2722px"})
      .attr("marginheight",0).attr("marginwidth",0).attr("scrolling","no").attr("frameborder","no").
      attr("name","iframepage").attr("src",'/admin/new_event/neweventtable/add/')).appendTo($(parentTmp).find("#tabDiv .tab-content"));
    $(parent.document.getElementById("pageLoader")).show();
    return false;
  })
}
function getNumberFormUrl(urlStr) {
  return $.trim(urlStr.replace(/[^0-9]/ig,""));
}
function tabClick() {
        var href = $(this).parent("a").attr("href");
        var targetId = "";
        if($(this).parents("li").hasClass("active")) {
          if($(this).parents("li").next().length>0) {
            $(this).parents("li").next().addClass("active");
            targetId = $(this).parents("li").next().find("a").attr("href");
          } else if($(this).parents("li").prev().length>0) {
            $(this).parents("li").prev().addClass('active');
            targetId = $(this).parents("li").prev().find("a").attr("href");
          }
          $(top.document).find(targetId).addClass("active");
        }
        $(this).parents("li").remove();
        $(top.document).find(href).remove();
        return  false;
}