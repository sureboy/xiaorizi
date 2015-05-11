$(function(){
    if($(".nav-parent>a").length>0) {
      $(".nav-parent>a").toggle(function(e){
        if(!$('body').hasClass('leftpanel-collapsed')) {
          var that = $(this).parents(".nav-parent");
          $(this).parents("ul.nav-bracket").find(".nav-parent").removeClass("active").removeClass("nav-active");
          $(this).parent("li").addClass("active");
            that.find(".children").slideDown(function(){
              that.addClass("nav-active");
              return false;
          });
        }
      },function(e){
        if(!$('body').hasClass('leftpanel-collapsed')) {
          var that = $(this).parents(".nav-parent");
          $(this).parents("ul.nav-bracket").find(".nav-parent").removeClass("active").removeClass("nav-active");
          $(this).parent("li").addClass("active");
            that.find(".children").slideUp();
            that.removeClass("nav-active");
            return false;
        }
      });
    }
    if($("#leftpanel").length>0) {
      $("#leftpanel .children").find("a").click(function(){
        var tmp = $(this);
        $("#pageLoader").show();
        addRemoveTab(tmp);
        return false;
      });
      function iFrameHeight(idName) {
        var ifm = $("#" + idName)[0];
        var subWeb = null;
        if(ifm && !window.opera) {
          if(ifm.contentDocument && ifm.contentDocument.body.offsetHeight) {
            $(ifm).attr("height" ,ifm.contentDocument.body.offsetHeight+"px");
          } 
        }

      }
      function addRemoveTab(tmp){
        var isAgain = false;
        var targetId = tmp.attr("data-name");
        $("#tabDiv ul.rightListFrame li a").each(function(){
          if(tmp.attr("data-name") === $(this).attr("href").substring(1)) {
            isAgain = true;
          }
        });
        if(!isAgain ) {
          $("#tabDiv .rightListFrame li").removeClass("active");
            $("#tabDiv .tab-content .tab-pane").removeClass("active");
            $("<li></li>").addClass("active").append($("<a></a>").append($("<span></span>").text(tmp.text()).addClass('textSpan')).attr("href","#"+tmp.attr("data-name")).attr("data-toggle","tab").append($("<span class='icon-remove removeTab'></span>").bind('click',tabClick))).appendTo($("#tabDiv").find("ul.rightListFrame"));
            $("<div></div>").addClass("tab-pane").addClass("active").attr("id",tmp.attr("data-name")).append($("<iframe></iframe>").attr("id","iFrame"+tmp.attr("data-name")).css({"width":"100%","height":"2122px"}).attr("marginheight",0).attr("marginwidth",0).attr("scrolling","no").attr("frameborder","no").attr("name","iframepage").attr("src",tmp.attr("href"))).appendTo($("#tabDiv").find(".tab-content"));
           // iFrameHeight("iFrame"+tmp.attr("data-name"));
        } else {
          $("#tabDiv .rightListFrame li").removeClass("active");
          $("#tabDiv .tab-content .tab-pane").removeClass("active");
          $("#tabDiv").find("a[href="+"#"+targetId+"]").parent("li").addClass("active");
          $("#"+targetId).addClass("active");
        }
      }
      function tabClick() {
        var href = $(this).parent("a").attr("href");
        var targetId = "";
        if($(this).parents("li").hasClass("active")) {
          if($(this).parents("li").next().length>0) {
            $(this).parents("li").next().addClass("acitve");
            targetId = $(this).parents("li").next().find("a").attr("href");
            $(targetId).addClass("active");
          } else if($(this).parents("li").prev().length>0) {
            $(this).parents("li").prev().addClass('active');
            targetId = $(this).parents("li").prev().find("a").attr("href");
            $(targetId).addClass("active");
          }
        }
        $(this).parents("li").remove();
        $(href).remove();
        return  false;
      }
    }
    $('.menutoggle').click(function(){
      if($('body').hasClass('leftpanel-collapsed')) {
        $('body').removeClass('leftpanel-collapsed');
      } else {
        $('body').addClass('leftpanel-collapsed');
      }
    });
    $(".nav.nav-pills.nav-stacked.nav-bracket li").hover(function(){
      $(this).addClass('nav-hover');
    },function(){
      $(this).removeClass('nav-hover');
    })
    $(".dropdown-toggle").click(function(){
      if($(this).parent('div').hasClass('open')) {
        $(this).parent('div').removeClass('open');
      } else {
        $(this).parent('div').addClass('open');
      }
    })
});