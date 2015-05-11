CKEDITOR.plugins.add( 'dropDownList',
{   
   requires : ['richcombo'], //, 'styles' ],
   init : function( editor )
   {
      var config = editor.config,
         lang = editor.lang.format;

      // Gets the list of tags from the settings.
      var tags = []; //new Array();
      //this.add('value', 'drop_text', 'drop_label');
      tags[0]=["[新浪分享]", "新浪分享", "新浪分享"];
      tags[1]=["[人人分享]", "人人分享", "人人分享"];
      tags[2]=["[QQ分享]", "QQ分享", "QQ分享"];
      
      // Create style objects for all defined styles.

      editor.ui.addRichCombo( 'dropDownList',
         {
            label : "添加社区分享",
            title :"添加社区分享",
            voiceLabel : "添加社区分享",
            className : 'cke_format',
            multiSelect : false,

            panel :
            {
               css : [ config.contentsCss, CKEDITOR.getUrl( CKEDITOR.skin.getPath('editor') ) ],
               voiceLabel : lang.panelVoiceLabel
            },

            init : function()
            {
               this.startGroup( "添加社区分享" );
               //this.add('value', 'drop_text', 'drop_label');
               for (var this_tag in tags){
                  this.add(tags[this_tag][0], tags[this_tag][1], tags[this_tag][2]);
               }
            },

            onClick : function( value )
            {         
               editor.focus();
               editor.fire( 'saveSnapshot' );
               editor.insertHtml(value);
               editor.fire( 'saveSnapshot' );
            }
         });
   }
});