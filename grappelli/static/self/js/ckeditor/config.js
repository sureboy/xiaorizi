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
					{ name: 'extent', items: ['myButton','myNews','dropDownList' ] },
					'/',
                     { name: 'document', items: ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates'] },
                     { name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'] },
                     { name: 'editing', items: ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt'] },
                     { name: 'forms', items: ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'] },
                     '/',
                     { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'] },
                     { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'] },
                     { name: 'links', items: ['Link', 'Unlink', 'Anchor'] },
                     { name: 'insert', items: ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe'] },
                     '/',
                     { name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize'] },
                     { name: 'colors', items: ['TextColor', 'BGColor'] },
                     { name: 'tools', items: ['Maximize', 'ShowBlocks'] },
                     
                     
                 ];
     config.toolbar = 'Mine';
     config.extraPlugins += (config.extraPlugins ? ',myButton,myNews,dropDownList' : 'myButton,myNews,dropDownList');
     config.removePlugins= 'elementspath',
     //宸ュ叿鏍忕殑浣嶇疆
     config.toolbarLocation = 'bottom'; 
 
     
};
