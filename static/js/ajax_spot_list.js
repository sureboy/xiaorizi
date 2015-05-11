(function($){
	$("#id_txt_code_in").live('click',function(event){ 
		if(event.target){
			
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/admin/spot/sysspotcode/'+id+'" target="_blank" >编辑选中</a>'
			$("#html_code").html(url)
			 }		 		
		}
	})
	
	$("#id_txt_code_from").live('click',function(event){ 
		if(event.target){
			
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/admin/spot/sysspotcode/'+id+'" target="_blank" >编辑选中</a>'
			$("#html_code").html(url)
			 }		 		
		}
	})
	
	$("#id_txt_img_to").live('click',function(event){ 
		if(event.target){			 
			var url=$(event.target).attr("data-img")
			
			$("#img_show").attr('src',url)
			$("#img_show").attr('height',300)	
			
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/admin/spot/sysspotimg/'+id+'" target="_blank" >编辑选中</a>'
			$("#html_img").html(url)
			 }
		}
	})
	
	$("#id_spot_img_to").live('click',function(event){ 
		if(event.target){			 
			var url=$(event.target).attr("data-img")
			
			$("#img_show").attr('src',url)
			$("#img_show").attr('height',300)	
			
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
				url='<a href="/admin/spot/sysspotimg/'+id+'" target="_blank" >编辑选中</a>'
				$("#html_img").html(url)
			 }
		}
	})
	
	$("#id_txt_img_from").live('click',function(event){ 
		if(event.target){			 
			var url=$(event.target).attr("data-img")
			
			$("#img_show").attr('src',url)
			$("#img_show").attr('height',300)	
			
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/admin/spot/sysspotimg/'+id+'" target="_blank" >编辑选中</a>'
			$("#html_img").html(url)
			 }
		}
	})
	
	$("#id_spot_img_from").live('click',function(event){ 
		if(event.target){			 
			var url=$(event.target).attr("data-img")
			
			$("#img_show").attr('src',url)
			$("#img_show").attr('height',300)	
			
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
				url='<a href="/admin/spot/sysspotimg/'+id+'" target="_blank" >编辑选中</a>'
				$("#html_img").html(url)
			 }
		}
	})
		$("#id_spot_txt_to").live('click',function(event){ 
		if(event.target){			 
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/admin/spot/sysspottxt/'+id+'" target="_blank" >编辑选中</a>'
			$("#html_txt").html(url)
			 }
			 		
		}
	})
	$("#id_spot_txt_from").live('click',function(event){ 
		if(event.target){			 
			 
			
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/admin/spot/sysspottxt/'+id+'" target="_blank" >编辑选中</a>'
			$("#html_txt").html(url)
			 }
			
			 		
		}
	})
	$("#id_spot_code_to").live('click',function(event){ 
		if(event.target){			 
			 
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/admin/spot/sysspotcode/'+id+'" target="_blank" >编辑选中</a>'
			$("#html_code").html(url)
			 }
			 		
		}
	})
	
	$("#id_spot_code_from").live('click',function(event){ 
		if(event.target){			 
			 
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/admin/spot/sysspotcode/'+id+'" target="_blank" >编辑选中</a>'
			$("#html_code").html(url)
			 }
			 		
		}
	})
	
	
		$("#id_spot_event_to").live('click',function(event){ 
		if(event.target){			 
			 
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/event-'+id+'" target="_blank" >查看活动</a>'
			$("#html_event").html(url)
			 }
			 		
		}
	})
	
	$("#id_spot_event_from").live('click',function(event){ 
		if(event.target){			 
			 
			var id=$(event.target).attr("value")
			//$("#html_txt").html(event.target)
			 if(id){
			url='<a href="/event-'+id+'" target="_blank" >查看活动</a>'
			$("#html_event").html(url)
			 }
			 		
		}
	})
	
 
//$("#img_show").find("option:selected").text();
	
$("#id_spot_img_input").live("keyup", function(){
    var querystring = $("#id_spot_img_input").val();
    if (querystring) {
        $.ajax ({
            type: "GET",
            url: "/spot/get_json_img/"+querystring+"/",
            cache: false,
            success: function(json) {
                if (json) {
                    var list_from = $("#id_spot_img_from option").map(function() {
                        return parseInt($(this).val());
                    });
                    var list_to = $("#id_spot_img_to option").map(function() {
                        return parseInt($(this).val());
                    });
                    for (var pid in json) {
                        if ($.inArray(json[pid].id, list_from) == -1 && $.inArray(json[pid].id, list_to) == -1) {
                            $("#id_spot_img_from").prepend("<option data-img='"+json[pid].urls+"'  value='"+json[pid].id+"'> "+json[pid].name+"  </option>");
                        }
                    }
                    SelectBox.init('id_spot_img_from');
                    SelectBox.init('id_spot_img_to');
                }
            }
        });
    }
})

$("#id_spot_event_input").live("keyup", function(){
    var querystring = $("#id_spot_event_input").val();
    if (querystring) {
        $.ajax ({
            type: "GET",
            url: "/spot/get_json_event/"+querystring+"/",
            cache: false,
            success: function(json) {
                if (json) {
                    var list_from = $("#id_spot_event_from option").map(function() {
                        return parseInt($(this).val());
                    });
                    var list_to = $("#id_spot_event_to option").map(function() {
                        return parseInt($(this).val());
                    });
                    for (var pid in json) {
                        if ($.inArray(json[pid].id, list_from) == -1 && $.inArray(json[pid].id, list_to) == -1) {
                            $("#id_spot_event_from").prepend("<option value='"+json[pid].id+"'>"+json[pid].name+"</option>");
                        }
                    }
                    SelectBox.init('id_spot_event_from');
                    SelectBox.init('id_spot_event_to');
                }
            }
        });
    }
})


$("#id_spot_txt_input").live("keyup", function(){
    var querystring = $("#id_spot_txt_input").val();
    if (querystring) {
        $.ajax ({
            type: "GET",
            url: "/spot/get_json_txt/"+querystring+"/",
            cache: false,
            success: function(json) {
                if (json) {
                    var list_from = $("#id_spot_txt_from option").map(function() {
                        return parseInt($(this).val());
                    });
                    var list_to = $("#id_spot_txt_to option").map(function() {
                        return parseInt($(this).val());
                    });
                    for (var pid in json) {
                        if ($.inArray(json[pid].id, list_from) == -1 && $.inArray(json[pid].id, list_to) == -1) {
                            $("#id_spot_txt_from").prepend("<option data-txt='"+json[pid].txt+"' value='"+json[pid].id+"'>"+json[pid].name+"</option>");
                        }
                    }
                    SelectBox.init('id_spot_txt_from');
                    SelectBox.init('id_spot_txt_to');
                }
            }
        });
    }
})
$("#id_spot_code_input").live("keyup", function(){
    var querystring = $("#id_spot_code_input").val();
    if (querystring) {
        $.ajax ({
            type: "GET",
            url: "/spot/get_json_code/"+querystring+"/",
            cache: false,
            success: function(json) {
                if (json) {
                    var list_from = $("#id_spot_code_from option").map(function() {
                        return parseInt($(this).val());
                    });
                    var list_to = $("#id_spot_code_to option").map(function() {
                        return parseInt($(this).val());
                    });
                    for (var pid in json) {
                        if ($.inArray(json[pid].id, list_from) == -1 && $.inArray(json[pid].id, list_to) == -1) {
                            $("#id_spot_code_from").prepend("<option  data-code='"+json[pid].code+"'  value='"+json[pid].id+"'>"+json[pid].name+"</option>");
                        }
                    }
                    SelectBox.init('id_spot_code_from');
                    SelectBox.init('id_spot_code_to');
                }
            }
        });
    }
})

$("#id_spot_cat_input").live("keyup", function(){
    var querystring = $("#id_spot_cat_input").val();
    if (querystring) {
        $.ajax ({
            type: "GET",
            url: "/spot/get_json_cat/"+querystring+"/",
            cache: false,
            success: function(json) {
                if (json) {
                    var list_from = $("#id_spot_cat_from option").map(function() {
                        return parseInt($(this).val());
                    });
                    var list_to = $("#id_spot_cat_to option").map(function() {
                        return parseInt($(this).val());
                    });
                    for (var pid in json) {
                        if ($.inArray(json[pid].id, list_from) == -1 && $.inArray(json[pid].id, list_to) == -1) {
                            $("#id_spot_cat_from").prepend("<option value='"+json[pid].id+"'>"+json[pid].name+"</option>");
                        }
                    }
                    SelectBox.init('id_spot_cat_from');
                    SelectBox.init('id_spot_cat_to');
                }
            }
        });
    }
})

$("#id_spot_city_input").live("keyup", function(){
    var querystring = $("#id_spot_city_input").val();
    if (querystring) {
        $.ajax ({
            type: "GET",
            url: "/spot/get_json_city/"+querystring+"/",
            cache: false,
            success: function(json) {
                if (json) {
                    var list_from = $("#id_spot_city_from option").map(function() {
                        return parseInt($(this).val());
                    });
                    var list_to = $("#id_spot_city_to option").map(function() {
                        return parseInt($(this).val());
                    });
                    for (var pid in json) {
                        if ($.inArray(json[pid].id, list_from) == -1 && $.inArray(json[pid].id, list_to) == -1) {
                            $("#id_spot_city_from").prepend("<option value='"+json[pid].id+"'>"+json[pid].name+"</option>");
                        }
                    }
                    SelectBox.init('id_spot_city_from');
                    SelectBox.init('id_spot_city_to');
                }
            }
        });
    }
})

}(django.jQuery));