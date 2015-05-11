$(function(){
  if($("#aboutUsTab").length>0) {
  $("#aboutUsTab div").hide();
  var id = $("#aboutUs li.activeItem")[0].name;
  var text = $("#aboutUs li.activeItem a").text();
  $("#placeArea").text(text);
  $("#aboutUsTab").find("#"+id).show();
  if($("#placeArea").length > 0) {
    $("#placeArea").text(text);
  }
  var links =  $("#aboutUs>div>div>ul>li>a");
  if(links.length > 0) {
      links.click(function() {
      var id = this.name;
      $("#aboutUsTab>div").hide().end().find("#"+id).show();
      $("#placeArea").text($(this).text());
      $("#aboutUs li").removeClass("selected").removeClass("activeItem");
      $(this).parent("li").addClass("selected").addClass("activeItem");
      $("#listUl").css("height",$("#aboutUsTab").css("height"));
      return false;
    });
    links.hover(function(){
      $(this).parents('ul').find('li:not(.selected)').removeClass('activeItem').end().end().parent().addClass('activeItem');
    });
  };
  var key = "";
  var url = window.location.href;
  $("#aboutUs li").removeClass("activeItem").removeClass("selected");
  if(url.indexOf('#') != -1) {
     key = url.split("#")[1].substring(0,url.split("#")[1].length-1);
  } else {
    key = "introduction";
  }
   $("a[name="+key+"]").parent("li").addClass("activeItem").addClass("selected");
     $("#aboutUsTab div").hide();
     $("#"+key).show();
     $("#placeArea").text($("a[name="+key+"]").text());
  if($("#aboutUsDl").length>0 && $("#aboutUs").length>0) {
    $("#aboutUsDl").find("dt a").on('click',function(){
        var href = $(this).attr("href");
        var index = href.indexOf("#");
        var name = href.substring(index+1,href.length-1);
        $("a[name="+name+"]").trigger("click");
    });
  }
  }
});
