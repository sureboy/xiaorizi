//初始化查询所有数据
$(document).ready(function(){
    var timeflag = $(".select_order").find("option:selected").val();
    var cityflag = $(".select_city").find("option:selected").val();
    $.get(
        "/weibo/show/",function(data) {
            var addtime_city = [];
            var addtime_count = [];
            var addtime_style = [];
            var addtime_all = [];
            console.log(data);
            $('.div_title').html("<p>"+data.data[0].city+"分类情况</p>")
            for(var j=0;j<data.data[0].style.length;j++){
                addtime_city.push(data.data[0].style[j].name);
                addtime_all.push({
                    name: data.data[0].style[j].name,
                    value: data.data[0].style[j].count
                });
            }



//            for (var e = 0; e < data.data.length; e++) {
//                addtime_city.push(data.data[e].city);
//                //addtime_style.push(data.data[e].style.name);
//                addtime_count.push(data.data[e].count);
//                addtime_all.push({
//                    name: data.data[e].city,
//                    value: data.data[e].count
//                })
//            }

            require.config({
                paths: {
                    echarts: 'http://echarts.baidu.com/build/dist'
                }
            });



            require(
                [
                    'echarts',
                    'echarts/chart/pie'
                ],
                function (ec) {
                    // 基于准备好的dom，初始化echarts图表
                    var myChart = ec.init(document.getElementById('main'));
                    option = {
                        title : {
                            text: '活动家订单分类占百分比',
                            subtext: '活动家',
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
                                name:'来源',
                                type:'pie',
                                radius : '55%',
                                width: '100%',
                                center: ['50%', '60%'],
                                data:addtime_all
                            }
                        ]
                    };
                    // 为echarts对象加载数
                    myChart.setOption(option);
                    myChart.on('click', function(param) {
                        alert("sdf")
                    });
                });
        });
});


//点击进行数据过滤
$(".search_order").click(function() {
    var catflag = $(".select_cat").find("option:selected").val();
    var cityflag = $(".select_city").find("option:selected").val();
    $.get(
        "/weibo/show/",
        {'city':cityflag,'style':catflag},
        function(data) {
            var addtime_city = [];
            var addtime_count = [];
            var addtime_style = [];
            var addtime_all = [];
            var arr_bar_y = []
            console.log(data);
            $('.div_title').html("<p>"+data.data[0].city+"分类情况</p>")
            for(var j=0;j<data.data[0].style.length;j++){
                addtime_city.push(data.data[0].style[j].name);
                arr_bar_y.push(data.data[0].style[j].count);
                addtime_all.push({
                    name: data.data[0].style[j].name,
                    value: data.data[0].style[j].count
                });
            }



//            for (var e = 0; e < data.data.length; e++) {
//                addtime_city.push(data.data[e].city);
//                //addtime_style.push(data.data[e].style.name);
//                addtime_count.push(data.data[e].count);
//                addtime_all.push({
//                    name: data.data[e].city,
//                    value: data.data[e].count
//                })
// //            }

//             require.config({
//                 paths: {
//                     echarts: 'http://echarts.baidu.com/build/dist'
//                 }
//             });

//             require(
//                             [
//                                 'echarts',
//                                 'echarts/chart/bar'
//                             ],
//                             function (ec) {
//                                 // 基于准备好的dom，初始化echarts图表
//                                 var myChart = ec.init(document.getElementById('main'));
//                                 option = {
//                                     title : {
//                                         text: '某地区蒸发量和降水量',
//                                         subtext: '纯属虚构'
//                                     },
//                                     tooltip : {
//                                         trigger: 'axis'
//                                     },
//                                     legend: {
//                                         data:['数量']
//                                     },

//                                     calculable : true,
//                                     xAxis : [
//                                         {
//                                             type : 'category',
//                                             data :addtime_city
//                                         }
//                                     ],
//                                     yAxis : [
//                                         {
//                                             type : 'value'
//                                         }
//                                     ],
//                                     series : [
//                                         {
//                                             name:'数量',
//                                             type:'bar',
//                                             data:arr_bar_y,
//                                             markPoint : {
//                                                 data : [
//                                                     {type : 'max', name: '最大值'},
//                                                     {type : 'min', name: '最小值'}
//                                                 ]
//                                             },
//                                             markLine : {
//                                                 data : [
//                                                     {type : 'average', name: '平均值'}
//                                                 ]
//                                             }
//                                         }
//                                     ]
//                                 };
                                         var ecConfig = require('echarts/config');

                                        myChart.on('click',function (param) {
                                        alert("Sdf")
                                        });
                                // });
                                // });


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
//                            text: '活动家订单分类占百分比',
//                            subtext: '活动家',
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
//                                name:'来源',
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
//                });







        });
});