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
		  $("#id_pr").show();
		  $("#id_zpr").hide();
		  $("#id_ppr").hide();
		  $("#id_max_pr").hide();
		  $("#id_min_pr").hide();		  
		  
	  }else{
		  
		  $("#id_pr").show();
		  $("#id_zpr").show();
		  $("#id_ppr").show();
		  $("#id_max_pr").show();
		  $("#id_min_pr").show();
		  
	  }
	}(django.jQuery));
}

(function($){
	$("#con_neweventparagraph").attr('style','')	
	url='<input class="" name="tab_txt" id="tab_txt" type="text">'
		$("#con_neweventparagraph").html(url) 
	
}(django.jQuery));
 
 
editor = CKEDITOR.appendTo( 'con_neweventparagraph', config={} );
editor.setData( '' ); 