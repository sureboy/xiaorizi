    function countDown(id,timeTag,endTime) {
      var placeTime = $("#"+id);
      //如果不存在存放时间的dom对象则返回
      if(!placeTime) {
        return false;
      }
      endTime1 = new Date(endTime);
      //跟新时间
      function updateDate() {
        //获取当前时间
        var today = new Date();
        if (today > endTime1) {
          $("#"+id).hide();
          //$("."+timeTag).html("活动结束").css({"backgroundColor":"#b0b0b0","color":"#fff"});
          $(".hiddenByTime").attr("disabled","disabled");
          clearTimeout(t);
          return false;
        }
        //获得距离规定时间的毫秒数
        var level1 = endTime1.getTime() - today.getTime();
        //获得相差天数
        var date =formatTime(Math.floor(level1/(24*3600*1000)));
        var level2 = level1 % (24*3600*1000);
        var hour = formatTime(Math.floor(level2/(3600*1000)));
        var level3 = level2 %(3600*1000);
        var minute = formatTime(Math.floor(level3/(60*1000)));
        var level4 = level3 %(60*1000);
        var second = formatTime(Math.floor(level4 / 1000));
        var timeStr = ["<span>",date,"</span>"," 天 ","<span>",hour,"</span>"," 小时 ","<span>",minute,"</span>"," 分钟 ","<span>",second,"</span>"," 秒"].join('');
        $("#"+id).html(timeStr);
        if (level1 < 10) {
          clearTimeout(t);
          $("#"+id).hide();
        //  $("."+timeTag).html("活动结束").css({"backgroundColor":"#b0b0b0","color":"#fff"});
          $(".hiddenByTime").attr("disabled","disabled");
        }
      }
      function formatTime(i) {
          if(i < 10) {
            i = "0" + i;
          }
          return i;
      }
      var t = setInterval(updateDate,1000);
    }