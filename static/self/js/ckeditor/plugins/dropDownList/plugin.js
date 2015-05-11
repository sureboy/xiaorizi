CKEDITOR.plugins.add( 'dropDownList',
{   
   requires : ['richcombo'], //, 'styles' ],
   init : function( editor )
   {
      var config = editor.config,
         lang = editor.lang.format;

      // Gets the list of tags from the settings.
      var tags = []; //new Array();
	  
	  
		(function($){	  
			k=$("#id_cat").val()
			if (!k | k==null )k='0'
	  			$.ajax ({
				type: "GET",
				url: "/newevent/get_paragraph_tag/"+k+"/",
				data:'',
				cache: false,
				success: function(json) {
				
					for (var pid in json) {	
						tags[pid]=[json[pid].id,json[pid].name,json[pid].name]
							}
					 
				 
				
				 
  
				}
			});
			}(django.jQuery));
	  
      //this.add('value', 'drop_text', 'drop_label');
 
      
      // Create style objects for all defined styles.

      editor.ui.addRichCombo( 'dropDownList',
         {
            label : "选择Tab",
            title :"选择Tab",
            voiceLabel : "选择Tab",
            className : 'cke_format',
            multiSelect : false,			
            panel :
            {
               css : [ config.contentsCss, CKEDITOR.getUrl( CKEDITOR.skin.getPath('editor') ) ],
               voiceLabel : lang.panelVoiceLabel
            },

            init : function()
            {
               this.startGroup( "添加Tab" );
               //this.add('value', 'drop_text', 'drop_label');
               for (var this_tag in tags){
                  this.add(tags[this_tag][0], tags[this_tag][1], tags[this_tag][2]);
               }
            },

            onClick : function( value )
            {      
				(function($){	
					ik=$("#con_neweventparagraph").attr('data_tab_id')
					if (value!=ik){
					//$("#con_neweventparagraph").attr('data_tab_id',value)
					$("#select_newvenue option:selected").each(function(){
						$(this).attr("selected", false)
					})
					
				 
					for (var this_tag in tags){
						if (tags[this_tag][0]==value)
						{
						val_title=tags[this_tag][1]
						break;
						}
						}
					
					$("#tab_txt").val( val_title );
					 }
				
				
				
				}(django.jQuery));
				
				 
				/**
				for (var this_tag in tags){
						if (tags[this_tag][0]==value)
						{
						this.startGroup(tags[this_tag][1])
						break;
						}
				}
				
				 
				 
               editor.focus();
               editor.fire( 'saveSnapshot' );
               editor.insertHtml(value);
               editor.fire( 'saveSnapshot' );
			   **/
            }
         });
   }
});