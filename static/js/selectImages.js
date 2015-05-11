$(function () {
    $("#result_list tbody tr").each(function(){
        $(this).find("th:eq(0) a").removeAttr("onclick")
    })
    $("#result_list tbody tr th").eq(0).on('click','a',function(){
        window.opener.$("#retrunId").append("<li><img src='"+$(this).text()+"' alt='""+retrunId+'<span>图片ID:"+retrunId+"</span></li>")
        return false;
    })
})