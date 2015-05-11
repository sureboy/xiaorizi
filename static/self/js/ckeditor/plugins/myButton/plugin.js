//注册“myButton”插件到编辑器
 
  var saveCmd =
  {
    modes : { wysiwyg:1, source:1 },
    exec : function( editor )
    {
	
	//alert(ids)
 
	  //alert(editor.getData())
	  
	  (function($){	  
	  ids=$("#con_neweventparagraph").attr('data_id')//document.getElementById("con_neweventparagraph").getAttribute("data_id");
	  //tag_id=$("#con_neweventparagraph").attr('data_tag_id')	  
	  tab_txt=$("#tab_txt").val()
	  event_ids=$("#con_neweventparagraph").attr('data_event_id')
	  
	  
	  			$.ajax ({
				type: "POST",
				url: "/newevent/save_txt/",
				data:{'id':ids,'event_id':event_ids,'txts':editor.getData(),'tab_txt':tab_txt},
				cache: false,
				success: function(json) {
				
				if (json.msg=='save'){
				va=$("#id_paragraph").val()
				if (va){
					va+=','
				}
				$("#id_paragraph").val(va+json.txt_id)
				 $("#select_neweventparagraph").prepend("<option  value='"+json.txt_id+"'>"+json.txt_id+'—'+$("#tab_txt").val()+"</option>");
				}				
					alert(json.info)  
				}
			});
	  
	  
	  
	  	}(django.jQuery));
	  
	  
 
    }
  }

CKEDITOR.plugins.add( 'myButton', {
	//插件初始化方法
	init: function( editor ) {	
		//定义打开对话框的命令
		editor.addCommand( 'myButton', saveCmd );
		//创建一个工具栏按钮，它会执行我们上面定义的命令
		editor.ui.addButton( 'myButton', {
			icon: this.path+'icons/save.png',
			//按钮（如果是有效的话）的文本显示，以及鼠标悬停提示
			label: '保存',
			//单击按钮所执行的命令
			command: 'myButton'
			//toolbar: 'insert'
		});

		//注册我们的myButton.js
		//CKEDITOR.dialog.add( 'myButton', this.path + 'dialogs/myButton.js' );
	} 
});



 
