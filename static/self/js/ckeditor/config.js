/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

//CKEDITOR.editorConfig = function( config ) {
//	// Define changes to default configuration here. For example:
//	config.uiColor = '#AADC6E';
////	config.extraPlugins = 'myButton';
//	//config.toolbar = 'Full';   //Add the plugin to the full toolbar
//
////	config.toolbar =[['Source','Styles', 'Format','FontSize','Font'],  
//		               //         ['TextColor', '-' ,'Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link','Unlink','-','Cut','Copy','Paste','-','Image','Flash','Smiley','Maximize']  
//		               //    ];
//
//
//};









CKEDITOR.editorConfig = function (config) {
     // Define changes to default configuration here. For example:
     // config.language = 'fr';
     // config.uiColor = '#AADC6E';
     config.toolbar_Mine =
                 [
					{ name: 'extent', items: ['myButton','myNews',] },					 
                     { name: 'document', items: ['Source', '-',   'DocProps', 'Preview', ] },
                     { name: 'tools', items: ['Maximize', 'ShowBlocks'] },
                     { name: 'paragraph', items: ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
                     { name: 'insert', items: ['Image', 'Flash', 'Table', 'HorizontalRule'] },
                    //'/',
                     { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'] },
                    { name: 'links', items: ['Link', 'Unlink'] },
                     
                      
                     { name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize'] },
                     { name: 'colors', items: ['TextColor', 'BGColor'] },
                     
                     
                     
                 ];
     config.toolbar = 'Mine';
     config.extraPlugins += (config.extraPlugins ? ',myButton,myNews,dropDownList' : 'myButton,myNews,dropDownList');
     config.removePlugins= 'elementspath',
    
     config.toolbarLocation = 'bottom'; 
	 config.height = 400;   
	
	 config.keystrokes = [ [ CKEDITOR.ALT + 65 /*A*/, 'Maximize' ]]

 
     
};
