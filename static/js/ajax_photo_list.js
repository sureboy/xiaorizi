(function($){
$("#id_spot_img_input").live("keyup", function(){
    var querystring = $("#id_spot_img_input").val();
    if (querystring) {
        $.ajax ({
            type: "GET",
            url: "/spot/get_json_photos/"+querystring+"/",
            cache: false,
            success: function(json) {
                if (json) {
                    var list_from = $("#id_spot_img_from option").map(function() {
                        return parseInt($(this).val());
                    });
                    var list_to = $("#id_spot_img_to option").map(function() {
                        return parseInt($(this).val());
                    });
                    for (var pid in json) {
                        if ($.inArray(json[pid].id, list_from) == -1 && $.inArray(json[pid].id, list_to) == -1) {
                            $("#id_spot_img_from").prepend("<option value='"+json[pid].id+"'> "+json[pid].name+"  </option>");
                        }
                    }
                    SelectBox.init('id_spot_img_from');
                    SelectBox.init('id_spot_img_to');
                }
            }
        });
    }
})
}(django.jQuery));