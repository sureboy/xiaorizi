function pr_type(id_Type_val){
	(function($){
	if (id_Type_val==1){
		  $("#id_pr").show();
		  $("#id_zpr").show();
		  $("#id_ppr").show();
		  $("#id_max_pr").hide();
		  $("#id_min_pr").hide();		  
		  
	  }else if(id_Type_val==2){
		  $("#id_pr").show();
		  $("#id_zpr").show();
		  $("#id_ppr").show();
		  $("#id_max_pr").hide();
		  $("#id_min_pr").hide();		  
		  
	  }else if(id_Type_val==3){
		  $("#id_pr").show();
		  $("#id_zpr").hide();
		  $("#id_ppr").hide();
		  $("#id_max_pr").show();
		  $("#id_min_pr").show();		  
		  
	  }else if(id_Type_val==4){
		  $("#id_pr").hide();
		  $("#id_zpr").hide();
		  $("#id_ppr").hide();
		  $("#id_max_pr").hide();
		  $("#id_min_pr").hide();		  
		  
	  }else if(id_Type_val==5){
		  $("#id_pr").hide();
		  $("#id_zpr").hide();
		  $("#id_ppr").hide();
		  $("#id_max_pr").hide();
		  $("#id_min_pr").hide();		  

	  }else if(id_Type_val==6){
		  $("#id_pr").show();
		  $("#id_zpr").hide();
		  $("#id_ppr").hide();
		  $("#id_max_pr").hide();
		  $("#id_min_pr").hide();		  
		  
	  }
	  else if(id_Type_val==7){
		  $("#id_pr").hide();
		  $("#id_zpr").hide();
		  $("#id_ppr").hide();
		  $("#id_max_pr").hide();
		  $("#id_min_pr").hide();		  
		  
	  }
	  else{		  
		  $("#id_pr").show();
		  $("#id_zpr").show();
		  $("#id_ppr").show();
		  $("#id_max_pr").show();
		  $("#id_min_pr").show();
		  
	  }
	}(django.jQuery));
}
function save_txt(){
	var i=false;
	(function($){
		  ids=$("#con_neweventparagraph").attr('data_id')//document.getElementById("con_neweventparagraph").getAttribute("data_id");
		  //tag_id=$("#con_neweventparagraph").attr('data_tag_id')	  
		  tab_txt=$("#tab_txt").val()
		  tab_order=$("#tab_order").val()
		  event_ids=$("#con_neweventparagraph").attr('data_event_id')
		  
		  
		  			$.ajax ({
					type: "POST",
					url: "/newevent/save_txt/",
					data:{'id':ids,'event_id':event_ids,'txts':editor.getData(),'tab_txt':tab_txt,'tab_order':tab_order},
					cache: false,
					success: function(json) {
					if (json.msg=='update'){
					i=true;
					}
					if (json.msg=='save'){
					i=true;
					va=$("#id_paragraph").val();
					if (va){
					va+=','
					}
					$("#id_paragraph").val(va+json.txt_id)
					 $("#select_neweventparagraph").prepend("<option  value='"+json.txt_id+"'>"+json.txt_id+'—'+$("#tab_txt").val()+"</option>");
					
					}
					
						//alert(json.info)					 
							
					}
					
				});
		  }(django.jQuery));
		  
 		if (i==false){

			return confirm("信息保存提示")
	 
		}
		else{return i}

}


(function($){
	//onclick="return showAddAnotherPopup(this);
	$("#neweventtable_form").attr("onsubmit","return save_txt();")
	
 
	//$(".grp-button").attr('onclick','return save_txt();')
	
	

		
		var id_img=$("#id_img").val().split(",")[0]
	
	if(id_img){			 
		url1='<div  style="float: left;width:25px" ><a href="javascript:void(0);" id="del_select_neweventimg"   ><img src="/static/grappelli/images/icons/tools-delete-handler_hover.png" width="23" height="23" alt="删除选中项" /></a>'
		url1+='<a onclick="return showAddAnotherPopup(this);" id="edit_select_neweventimg" href="/admin/new_event/neweventimg/'+id+'/"   ><img src="/static/grappelli/images/icons/tools-trash-list-toggle-handler.png" width="23" height="23" alt="删除选中项" /></a>'
		url1+='</div>' 
			
		$.ajax ({
		type: "GET",
		url: "/newevent/get_json_img/"+id_img+"/",
		data:'',
		cache: false,
		success: function(json) {
						if (json) {
						for (var pid in json) {
							var img = new Image();
							  img.onload=function(){
								  imgs= $(".img").children('.l-d-4').children('.c-1').html()
								  imgk="<p>w:"+img.width +" h:"+img.height+"</p>";
								  $(".img").children('.l-d-4').children('.c-1').html(imgs+ imgk)
							  };
							  img.src=json[pid].url; 
							
							
							  div_s1='<div style="float: left;width:240px;height:160px;overflow-y:auto;backgroundColor:#fff; " >'
							
							  div_s1+= '<a target="_blank" href="'+json[pid].url+'"><img alt="点击查看原图"  id="pre" width="200" src="'+json[pid].url+'" alt="'+json[pid].name+'" /> </a>'
							div_s1+='</div>'
							$("#con_neweventimg").html(url1+div_s1)
							
							
						}
					}
				}
			});
	 }
	
	
	
	
	$("#con_neweventparagraph").attr('style','')	
	url='<input class="" name="tab_txt" id="tab_txt" type="text">'
	url+='<input class="" stype="width:10px" maxlength="4"  name="tab_order" value="" id="tab_order" type="text">'	
		$("#con_neweventparagraph").html(url) 
		
		
		var id=$("#id_paragraph").val().split(",")[0]
		
		url='<div  style="float: left;width:25px" ><a href="javascript:void(0);" id="del_select_neweventparagraph"   ><img src="/static/grappelli/images/icons/tools-delete-handler_hover.png" width="23" height="23" alt="删除选中项" /></a>'
		url+='</div>'
			if (id){
				//var txt=$(event.target).html()
				var txt=$("#select_neweventparagraph option:selected").text()
				//$(event.target).attr("value")
				url+='<input class="" name="tab_txt" value="'+txt+'" id="tab_txt" type="text">'
				
			}else
				{
				id=0
				url='<input class="" name="tab_txt"  id="tab_txt" type="text">'
				}
			
			url+='<input class="" stype="width:10px" maxlength="4"  name="tab_order" value="" id="tab_order" type="text">'	
			$("#con_neweventparagraph").html(url)  	
			html=$("#con_neweventparagraph").html()
		
			
			
			if (id)
			{
			
			$.ajax ({
				type: "GET",
				url: "/newevent/get_json_txt/"+id+"/",
				data:'',
				cache: false,
				success: function(json) {
						if (json) {
							var div_s=''
						for (var pid in json) {
							 //div_s='<div id="txt_editor" >'
							 div_s+=json[pid].txt
							 img_s=''
							 for (var pi in json[pid].img) {
								img_s+='<a href="'+json[pid].img[pi].urls+'" target="_blank" ><img width="430" src="'+json[pid].img[pi].urls+'" alt="'+json[pid].img[pi].name+'" /> </a>'
							 }
							 div_s+=img_s
							 $("#con_neweventparagraph").attr('data_id',json[pid].id)
							 //$("#con_neweventparagraph").attr('data_tab_id',json[pid].tab_id)
							 $("#tab_txt").val(json[pid].tab_name)
							 $("#tab_order").val(json[pid].order)
							 
							 
							//div_s+='</div>'
							//$("#con_neweventparagraph").html(html+div_s)
						}
						 
						//$("#con_neweventparagraph").html(div)
						$("#con_neweventparagraph").attr('style','')
						editor = CKEDITOR.appendTo( 'con_neweventparagraph', config={} );
						//editor = CKEDITOR.instances.con_neweventparagraph;
						editor.setData( div_s ); 
					}
				}
			});
				
			}else
			{
				editor = CKEDITOR.appendTo( 'con_neweventparagraph', config={} );
				editor.setData( '' ); 
				
			}
		
		
		
	
}(django.jQuery));
 
 
//editor = CKEDITOR.appendTo( 'con_neweventparagraph', config={} );
//editor.setData( '' ); 


 