//初始化查询所有数据
$(document).ready(function(){
    $("#allmap").hide();
    var timeflag = $(".select_order").find("option:selected").val();
    var cityflag = $(".select_city").find("option:selected").val();
    $.get(
        "/weibo/show/",function(data) {
            var addtime_city = [];
            var addtime_count = [];
            var addtime_style = [];
            var addtime_all = [];
            //console.log(data);
            $('.div_title').html("<p>"+data.data[0].city+"分类情况</p>");

            for(var j=0;j<data.data[0].style.length;j++){
                addtime_city.push(data.data[0].style[j].name);
                addtime_all.push({
                    name: data.data[0].style[j].name,
                    value: data.data[0].style[j].count
                });
            }
            require.config({
                paths: {
                    echarts: 'http://echarts.baidu.com/build/dist'
                }
            });
            require(
                [
                    'echarts',
                    'echarts/chart/pie',
                    'echarts/chart/funnel'
                ],
                function (ec) {
                    // 基于准备好的dom，初始化echarts图表
                    var myChart = ec.init(document.getElementById('main'));
                    option = {
                        title : {
                            text: '小日子分类占百分比',
                            subtext: '小日子',
                            x:'center'
                        },
                        tooltip : {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        legend: {
                            orient : 'vertical',
                            x : 'left',
                            data:addtime_city
                        },
                        toolbox: {
                            show : true,
                            feature : {
                                mark : {show: true},
                                dataView : {show: true, readOnly: true},
                                magicType : {
                                    show: true,
                                    type: ['pie', 'funnel'],
                                    option: {
                                        funnel: {
                                            x: '25%',
                                            width: '100%',
                                            funnelAlign: 'left',
                                            max: 1548
                                        }
                                    }
                                },
                                restore : {show: true},
                                saveAsImage : {show: true}
                            }
                        },
                        calculable : true,
                        series : [
                            {
                                name:'所有城市分类',
                                type:'pie',
                                radius : '55%',
                                width: '100%',
                                center: ['50%', '60%'],
                                data:addtime_all
                            }
                        ]
                    };
                    // 为echarts对象加载数据
                    myChart.setOption(option);
                    myChart.on('click',function(param) {
                        $("#showtbl").show();
                        var city=param.seriesName;
                        $("table").remove()
                        console.log(param)
                        city=city.substring(0,city.length-2);
                        $.get("/weibo/table/",{city:city,style:param.name,page:1},function(data){
                            tblhtml = '<table class="table table-bordered" style="text-align:center"><caption><h3>'+
                                        city+param.name+'</h3></caption><thead>'+
                                        '<th>序号</th>'+
                                        '<th>名称</th>' +
                                        '<th>地址</th>' +
                                        '<th>类型</th>' +
                                        '<th>城市</th></thread><tbody class="shuju">'
                            
                            for(var i = 0; i<data.data.length ; i++) {
                                tblhtml+=("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                //$(".shuju").append("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].url+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                            }
                            tblhtml+='</tbody></table></div>';
                            $('#tbl').html(tblhtml);
                        
                        });
                            
                        //分页开始
                            $(function(){
                                //此demo通过Ajax加载分页元素
                                // 创建分页
                                $("#Pagination").pagination(param.value/20+1, {
                                    num_edge_entries: 1, //边缘页数
                                    num_display_entries: 4, //主体页数
                                    callback: setData,//function(){alert(1111)},
                                    items_per_page: 1, //每页显示1项
                                    prev_text: "前一页",
                                    next_text: "后一页",
                                });
                                
                                function setData(page_index,jq){
                                    
                                    $.get("/weibo/table/",{city:city,style:param.name,page:page_index},function(data){
                                            tblhtml = '<table class="table table-bordered" style="text-align:center"><thead>'+
                                                        '<th>序号</th>'+
                                                        '<th>名称</th>' +
                                                        '<th>地址</th>' +
                                                        '<th>类型</th>' +
                                                        '<th>城市</th></thread><tbody class="shuju">'
                                            
                                            for(var i = 0; i<data.data.length ; i++) {
                                                tblhtml+=("<tr><td>"+data.data[i].id+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                                //$(".shuju").append("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].url+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                            }
                                            tblhtml+='</tbody></table></div>';
                                            $('#tbl').html(tblhtml);
                                        
                                        });
                                    
                         
                                    
                                }
                                                
                        });
                        //分页结束
                        
                   });         
                            
                    
                });
        });
});
//
////点击显示地图开始
//$(".select_city ").change(function() {
//    $(".select_cat").val("");
//    var catflag = $(".select_cat").find("option:selected").val();
//    var cityflag = $(".select_city").find("option:selected").val();
//    //请求一个城市中活动地址的经纬度
//    $.get("/weibo/map/",
//        {'city':cityflag},
//        function(data){
//            console.log(data,11111111);
//            //显示地图
//            // 百度地图API功能
//            var map = new BMap.Map("baidumap");
//            map.centerAndZoom(new BMap.Point(116.404, 39.915), 15);
//            var i;
//            var markers = [];
//            var points = []
//            console.log(data,11111111);
//            for(var j=0;j<data.data.length;j++){
////                points.push(new BMap.Point(data.data[0].x,data.data[0].y));
//                points.push(new BMap.Point(116.38632786853032,39.90762965106183));
//                break;
//            }
//            
//            
//            
//            console.log(points,222222222);
//            
//            function callback(xyResults){
//                var xyResult = null;
//                for(var index in xyResults){
//                    xyResult = xyResults[index];
//                    if(xyResult.error != 0){continue;}//出错就直接返回;
//                    var point = new BMap.Point(xyResult.x, xyResult.y);
//                    var marker = new BMap.Marker(point);
//                    map.addOverlay(marker);
//                    map.setCenter(point);// 由于写了这句，每一个被设置的点都是中心点的过程
//                }
//            }
//            
//            setTimeout(function(){
//                BMap.Convertor.transMore(points,2,callback);        //一秒之后开始进行坐标转换。参数2，表示是从GCJ-02坐标到百度坐标。参数0，表示是从GPS到百度坐标
//            }, 1000);
//            
//            
//            //显示地图结束
//            console.log(data);
//        });
//    
//});
//点击显示地图结束



//点击进行数据过滤
$(".select_city ").change(function() {
    $(".select_cat").val("");
    $("#Pagination").html("");
    $("#tbl").html("");
    var catflag = $(".select_cat").find("option:selected").val();
    var cityflag = $(".select_city").find("option:selected").val();
    $.get(
        "/weibo/show/",
        {'city':cityflag,'style':catflag},
        function(data) {
            var addtime_city = [];
            var addtime_all = [];
            var arr_bar_y = [];
            console.log(data);
            for(var j=0;j<data.data[0].style.length;j++){
                addtime_city.push(data.data[0].style[j].name);
                arr_bar_y.push(data.data[0].style[j].count);
                addtime_all.push({
                    name: data.data[0].style[j].name,
                    value: data.data[0].style[j].count
                });
            }

            require.config({
                paths: {
                    echarts: 'http://echarts.baidu.com/build/dist'
                }
            });

            require(
                [
                    'echarts',
                    'echarts/chart/funnel',
                    'echarts/chart/pie'
                ],
                function (ec) {
                    // 基于准备好的dom，初始化echarts图表
                    myChart = ec.init(document.getElementById('main'));
                    option = {
                        title : {
                            text: data.data[0].city+'分类占百分比',
                            subtext: '小日子',
                            x:'center'
                        },
                        tooltip : {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        legend: {
                            orient : 'vertical',
                            x : 'left',
                            data:addtime_city
                        },
                        toolbox: {
                            show : true,
                            feature : {
                                mark : {show: true},
                                dataView : {show: true, readOnly: true},
                                magicType : {
                                    show: true,
                                    type: ['pie', 'funnel'],
                                    option: {
                                        funnel: {
                                            x: '25%',
                                            width: '100%',
                                            funnelAlign: 'left',
                                            max: 1548
                                        }
                                    }
                                },
                                restore : {show: true},
                                saveAsImage : {show: true}
                            }
                        },
                        calculable : true,
                        series : [
                            {
                                name:data.data[0].city+'分类',
                                type:'pie',
                                radius : '55%',
                                width: '100%',
                                center: ['50%', '60%'],
                                data:addtime_all
                            }
                        ]
                    };
                    // 为echarts对象加载数据
                    myChart.setOption(option);
                    myChart.on('click',function(param) {
                        $("#showtbl").show();
                        var city=param.seriesName;
                        city=city.substring(0,city.length-2);
                        
                        //开始
                        $.get("/weibo/table/",
                                {city:city,style:param.name},
                                function(data){
                                        tblhtml = '<table class="table table-bordered" style="text-align:center"><thead>'+
                                                    '<th>序号</th>'+
                                                    '<th>名称</th>' +
                                                    '<th>地址</th>' +
                                                    '<th>类型</th>' +
                                                    '<th>城市</th></thread><tbody class="shuju">'
                                        
                                        for(var i = 0; i<data.data.length ; i++) {
                                            tblhtml+=("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                            //$(".shuju").append("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].url+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                        }
                                        tblhtml+='</tbody></table></div>';
                                        $('#tbl').html(tblhtml);
                                    
                                    });
                                                    
                                //分页开始
                                    $(function(){
                                        //此demo通过Ajax加载分页元素
                                        // 创建分页
                                        $("#Pagination").pagination(param.value/20+1, {
                                            num_edge_entries: 1, //边缘页数
                                            num_display_entries: 4, //主体页数
                                            callback: setData,//function(){alert(1111)},
                                            items_per_page: 1, //每页显示1项
                                            prev_text: "前一页",
                                            next_text: "后一页"
                                        });
                                        
                                        function setData(page_index,jq){
                                            
                                            $.get("/weibo/table/",{city:city,style:param.name,page:page_index},function(data){
                                                    tblhtml = '<table class="table table-bordered" style="text-align:center"><thead>'+
                                                                '<th>序号</th>'+
                                                                '<th>名称</th>' +
                                                                '<th>地址</th>' +
                                                                '<th>url</th>' +
                                                                '<th>类型</th>' +
                                                                '<th>城市</th></thread><tbody class="shuju">'
                                                    
                                                    for(var i = 0; i<data.data.length ; i++) {
                                                        tblhtml+=("<tr><td>"+data.data[i].id+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].url+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                                        //$(".shuju").append("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].url+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                                    }
                                                    tblhtml+='</tbody></table></div>';
                                                    $('#tbl').html(tblhtml);
                                                
                                                });
                                            
                                 
                                            
                                        }
                                                        
                                });
                                //分页结束
                        
                        //结束
                        
                    });
                });
        });
        $("#allmap").show();
});

//$(".select_cat ").change(function() {
//    $(".select_city").val("");
//    var catflag = $(".select_cat").find("option:selected").val();
//    var cityflag = $(".select_city").find("option:selected").val();
//    $.get(
//        "/weibo/show/",
//        {'city':cityflag,'style':catflag},
//        function(data) {
//            var addtime_city = [];
//            var addtime_all = [];
//            var arr_bar_y = [];
//            for(var j=0;j<data.data[0].style.length;j++){
//                addtime_city.push(data.data[0].style[j].name);
//                arr_bar_y.push(data.data[0].style[j].count);
//                addtime_all.push({
//                    name: data.data[0].style[j].name,
//                    value: data.data[0].style[j].count
//                });
//            }
//
//
//            require.config({
//                paths: {
//                    echarts: 'http://echarts.baidu.com/build/dist'
//                }
//            });
//
//            require(
//                [
//                    'echarts',
//                    'echarts/chart/pie'
//                ],
//                function (ec) {
//                    // 基于准备好的dom，初始化echarts图表
//                    var myChart = ec.init(document.getElementById('main'));
//                    option = {
//                        title : {
//                            text: data.data[0].city+'分类各城市占百分比',
//                            subtext: '小日子',
//                            x:'center'
//                        },
//                        tooltip : {
//                            trigger: 'item',
//                            formatter: "{a} <br/>{b} : {c} ({d}%)"
//                        },
//                        legend: {
//                            orient : 'vertical',
//                            x : 'left',
//                            data:addtime_city
//                        },
//                        toolbox: {
//                            show : true,
//                            feature : {
//                                mark : {show: true},
//                                dataView : {show: true, readOnly: true},
//                                magicType : {
//                                    show: true,
//                                    type: ['pie', 'funnel'],
//                                    option: {
//                                        funnel: {
//                                            x: '25%',
//                                            width: '100%',
//                                            funnelAlign: 'left',
//                                            max: 1548
//                                        }
//                                    }
//                                },
//                                restore : {show: true},
//                                saveAsImage : {show: true}
//                            }
//                        },
//                        calculable : true,
//                        series : [
//                            {
//                                name:data.data[0].city+'分类',
//                                type:'pie',
//                                radius : '55%',
//                                width: '100%',
//                                center: ['50%', '60%'],
//                                data:addtime_all
//                            }
//                        ]
//                    };
//                    // 为echarts对象加载数据
//                    myChart.setOption(option);
//                    /
//                        
//                    
//                };
//        });
//});

//点击进行数据过滤
$(".select_cat ").change(function() {
    $(".select_city").val("");
    $("#Pagination").html("");
    $("#tbl").html("");
    $("#allmap").hide();
    var catflag = $(".select_cat").find("option:selected").val();
    var cityflag = $(".select_city").find("option:selected").val();
    $.get(
        "/weibo/show/",
        {'city':cityflag,'style':catflag},
        function(data) {
            var addtime_city = [];
            var addtime_all = [];
            var arr_bar_y = [];
            console.log(data);
            for(var j=0;j<data.data[0].style.length;j++){
                addtime_city.push(data.data[0].style[j].name);
                arr_bar_y.push(data.data[0].style[j].count);
                addtime_all.push({
                    name: data.data[0].style[j].name,
                    value: data.data[0].style[j].count
                });
            }

            require.config({
                paths: {
                    echarts: 'http://echarts.baidu.com/build/dist'
                }
            });

            require(
                [
                    'echarts',
                    'echarts/chart/funnel',
                    'echarts/chart/pie'
                ],
                function (ec) {
                    // 基于准备好的dom，初始化echarts图表
                    myChart = ec.init(document.getElementById('main'));
                    option = {
                        title : {
                            text: data.data[0].city+'分类占百分比',
                            subtext: '小日子',
                            x:'center'
                        },
                        tooltip : {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        legend: {
                            orient : 'vertical',
                            x : 'left',
                            data:addtime_city
                        },
                        toolbox: {
                            show : true,
                            feature : {
                                mark : {show: true},
                                dataView : {show: true, readOnly: true},
                                magicType : {
                                    show: true,
                                    type: ['pie', 'funnel'],
                                    option: {
                                        funnel: {
                                            x: '25%',
                                            width: '100%',
                                            funnelAlign: 'left',
                                            max: 1548
                                        }
                                    }
                                },
                                restore : {show: true},
                                saveAsImage : {show: true}
                            }
                        },
                        calculable : true,
                        series : [
                            {
                                name:data.data[0].city+'分类',
                                type:'pie',
                                radius : '55%',
                                width: '100%',
                                center: ['50%', '60%'],
                                data:addtime_all
                            }
                        ]
                    };
                    // 为echarts对象加载数据
                    myChart.setOption(option);
                    myChart.on('click',function(param) {
                        $("#showtbl").show();
                        var city=param.seriesName;
                        style=city.substring(0,city.length-2);
                        console.log(param,111111);
                        //开始
                        var total = 0;
                        $.get("/weibo/table/",
                                {city:param.name,style:style,page:1},
                                function(data){
                                        tblhtml = '<table class="table table-bordered" style="text-align:center"><thead>'+
                                                    '<th>序号</th>'+
                                                    '<th>名称</th>' +
                                                    '<th>地址</th>' +
                                                    '<th>类型</th>' +
                                                    '<th>城市</th></thread><tbody class="shuju">'
                                        
                                        for(var i = 0; i<data.data.length ; i++) {
                                            tblhtml+=("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                            //$(".shuju").append("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].url+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                        }
                                        tblhtml+='</tbody></table></div>';
                                        $('#tbl').html(tblhtml);
                                        total = data.data.length;
                                    });
                                //分页开始
                                    $(function(){
                                        //此demo通过Ajax加载分页元素
                                        // 创建分页
                                        $("#Pagination").pagination(param.value/20+1, {
                                            num_edge_entries: 1, //边缘页数
                                            num_display_entries: 4, //主体页数
                                            callback: setData,//function(){alert(1111)},
                                            items_per_page: 1, //每页显示1项
                                            prev_text: "前一页",
                                            next_text: "后一页"
                                        });
                                        
                                        function setData(page_index,jq){
                                            
                                            $.get("/weibo/table/",{city:param.name,style:style,page:page_index},function(data){
                                                    tblhtml = '<table class="table table-bordered" style="text-align:center"><thead>'+
                                                                '<th>序号</th>'+
                                                                '<th>名称</th>' +
                                                                '<th>地址</th>' +
                                                                '<th>类型</th>' +
                                                                '<th>城市</th></thread><tbody class="shuju">'
                                                    
                                                    for(var i = 0; i<data.data.length ; i++) {
                                                        tblhtml+=("<tr><td>"+data.data[i].id+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                                        //$(".shuju").append("<tr><td>"+(i+1)+"</td><td>"+data.data[i].name+"</td><td>"+data.data[i].address+"</td><td>"+data.data[i].url+"</td><td>"+data.data[i].style+"</td><td>"+data.data[i].city_name+"</td></tr>")
                                                    }
                                                    tblhtml+='</tbody></table></div>';
                                                    $('#tbl').html(tblhtml);
                                                
                                                });
                                            
                                 
                                            
                                        }
                                                        
                                });
                                //分页结束
                        
                        //结束
                        
                    });
                });
        });
});
