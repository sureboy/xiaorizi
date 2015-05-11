CKEDITOR.editorConfig = function (config) {
     // Define changes to default configuration here. For example:
     // config.language = 'fr';
     // config.uiColor = '#AADC6E';
     config.toolbar_Mine =
                 [			 
                     { name: 'document', items: ['Source', '-',   'DocProps', 'Preview' ] },
                     { name: 'tools', items: ['Maximize', 'ShowBlocks'] },
                     { name: 'paragraph', items: ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
                     { name: 'insert', items: ['Image', 'Flash', 'Table', 'HorizontalRule'] },
                    //'/',
                     { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'] },
                    { name: 'links', items: ['Link', 'Unlink'] },
                     
                      
                     { name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize'] },
                     { name: 'colors', items: ['TextColor', 'BGColor'] }
                     
                     
                     
                 ];

    
     config.toolbarLocation = 'top'; 
	 config.height = 400;   
	
	 config.keystrokes = [ [ CKEDITOR.ALT + 65 /*A*/, 'Maximize' ]]

 
     
};
