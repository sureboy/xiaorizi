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
          $("<div></div>").addClass("tab-pane").addClass("active").attr("id",keyId).append($("<iframe></iframe>").css({"width":"100%","height":"2122px"}).attr("marginheight",0).attr("marginwidth",0).attr("scrolling","no").attr("frameborder","no").
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
function addNew() {
  $(".addNew").click(function(){
    var parentTmp = parent.window.document;
    $(parentTmp).find("#tabDiv .rightListFrame li").removeClass("active");
    $(parentTmp).find("#tabDiv .tab-content .tab-pane").removeClass("active");
    var maxIndex = 0;
    $(parentTmp).find("#tabDiv .rightListFrame li a").each(function(){
      maxIndex++;
    });
    var indexFoText = maxIndex+1;
    var keyId = $(this).attr('id')+maxIndex;
    var href = $(this).attr('href');
    var keyStr = $(this).text();
    $("<li></li>").addClass("active").append($("<a></a>").append($("<span></span>").text(keyStr+indexFoText).addClass('textSpan')).attr("href","#"+keyId).attr("data-toggle","tab").append($("<span class='icon-remove removeTab'></span>").bind('click',tabClick))).appendTo($(parentTmp).find("#tabDiv ul.rightListFrame"));
    $("<div></div>").addClass("tab-pane").addClass("active").attr("id",keyId).append($("<iframe></iframe>").css({"width":"100%","height":"2122px"})
      .attr("marginheight",0).attr("marginwidth",0).attr("scrolling","no").attr("frameborder","no").
      attr("name","iframepage").attr("src",href)).appendTo($(parentTmp).find("#tabDiv .tab-content"));
    $(parent.document.getElementById("pageLoader")).show();
    return false;
  })
}
$(function(){
    $(parent.document.getElementById("pageLoader")).hide();
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
    $('table').each(function(){
      if(!$(this).hasClass('table')) {
        $(this).addClass('table');
      }
    })
    if($("#action-toggle").length>0) {
      $("#action-toggle").click(function(){
        if($("#action-toggle").attr("selected") == undefined) {
            $("#action-toggle").parents("table").find(".action-select").attr("selected","true");
        } else {
            $("#action-toggle").parents("table").find(".action-select").removeAttr("selected");
        }
      });
    }
    $("#result_list>tbody>tr>th>a").on('click',function(){
      if(!$(this).hasClass('event_edit')) {
        var tmp = $(this);
        addRemoveTab(tmp);
        return false;
      }
    });
    addNew();
    $("#searchWidhCondition").click(function(){
      var storgeCondition = {};
      $("#filterGroup select").each(function(){
        var selectedOptionValue = $(this).val();
        if(selectedOptionValue !='?' ) {
          selectedOptionValue = selectedOptionValue.substring(1);
          if(selectedOptionValue.indexOf('&') !=-1) {
            var argsArray = selectedOptionValue.split('&');
            for(var i=0;i<argsArray.length;i++) {
              if(argsArray[i].indexOf('order_pay_status__exact=') !=-1 || argsArray[i].indexOf('order_status__exact') !=-1) {
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
      });
      for(key in storgeCondition) {
        if(storgeCondition.hasOwnProperty(key)) {
          var value = storgeCondition[key];
          var inputDom = $("<input type='hidden'>").attr('name',key).attr('value',value).appendTo($('#orderForm'));
        }
      }
      $("#filterGroup select").remove();
      $('#eventForm').submit();
    });
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