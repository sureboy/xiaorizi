(function()
{
  var saveCmd =
  {
    modes : { wysiwyg:1, source:1 },
    exec : function( editor )
    {
      //editor.updateElement(); 
	  alert(editor.getData())
 
    }
  }
  var pluginName = 'AjaxSave';
  CKEDITOR.plugins.add( pluginName,
  {
     init : function( editor )
     {
        var command = editor.addCommand( pluginName, saveCmd );
        //command.modes = { wysiwyg : !!( editor.element.$.form ) };
        editor.ui.addButton( 'AjaxSave',
         {
            label : editor.lang.save,
            command : pluginName,
			className: 'cke_button_save'
             
         });
     }
   });
})();
