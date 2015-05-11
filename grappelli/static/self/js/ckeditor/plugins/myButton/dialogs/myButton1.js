CKEDITOR.dialog.add( 'myButton', function(editor)
		{
	return {
		title :'是谁在笑？',
		minWidth : 350,
		minHeight : 100,
		contents : [
		            {
		            	id : 'myModal',
		            	label : '啊啊',
		            	title : '啊啊',
		            	elements :
		            		[
		            		 {
		            			 id : 'personName',
		            			 type : 'text',
		            			 label : '请输入'
		            		 }
		            		 ]
		            }
		            ],
		            onOk : function()
		            {
		            	editor.insertHtml(this.getValueOf( 'myModal', 'personName' )+"在笑！");
		            }

	}
		});