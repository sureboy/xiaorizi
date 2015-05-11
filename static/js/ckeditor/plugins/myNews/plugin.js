//注册“myButton”插件到编辑器
 
  var saveCmds =
  {
    modes : { wysiwyg:1, source:1 },
    exec : function( editor )
    {
    	save_txt()
		editor.setData('')
	  (function($){	  
	   $("#con_neweventparagraph").attr('data_id','') 
	   $("#con_neweventparagraph").attr('data_tag_id','')
 
	  
	  
	  	}(django.jQuery));
	  
	  
 
    }
  }

CKEDITOR.plugins.add( 'myNews', {
	//插件初始化方法
	init: function( editor ) {	
		//定义打开对话框的命令
		editor.addCommand( 'myNews', saveCmds );
		//创建一个工具栏按钮，它会执行我们上面定义的命令
		editor.ui.addButton( 'myNews', {
			icon: this.path+'icons/new.png',
 
			label: '新建',
	 
			command: 'myNews'
 
		});

 
	} 
});



 
