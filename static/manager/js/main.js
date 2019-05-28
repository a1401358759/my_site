// 全局变量
var ERROR_CODE = {
  SUCCESS: 0,
  UNKNOWN: 1,
  FAILED: 2,
  IN_BLACKLIST: 6,
  PARAM_ERROR: 12,
  NOT_FOUND: 13,
  NOT_LOGIN: 14
};

// 高德地图js API
var AMAP_KEY = "298b1d5aea8d521f18485063c094a914"

function msg_info(msg, type, timeout) {
  if (!type) type = 'info';
  if (!timeout) timeout = 3000;
  var id = (new Date).getTime() + '' + parseInt(Math.random() * 100);
  var msg_html = '<div id="'+ id +'" class="new-alert alert-' + type + '">'+ msg +'</div>'
  $('.content-header').after(msg_html);
  setTimeout(function () {
    $("#" + id).fadeOut();
  }, timeout);
  window.location.href = '#message-top';
}

var count=0;
function submitOnce (){
  if (count == 0){
    count++;
    return true;
  } else{
    msg_info("正在操作，请勿重复提交");
    return false;
  }
}

$(function(){
  // 短时间显示错误提示 3s
  setTimeout(function () {
    $(".dmsg").fadeOut();
  }, 3000);
  // 长时间显示错误提示 10s
  setTimeout(function () {
    $(".dmsg-long").fadeOut();
  }, 10000);
});


$.fn.serializefiles = function() {
  var obj = $(this);
  /* ADD FILE TO PARAM AJAX */
  var formData = new FormData();
  $.each($(obj).find("input[type='file']"), function(i, tag) {
    $.each($(tag)[0].files, function(i, file) {
      formData.append(tag.name, file);
    });
  });
  var params = $(obj).serializeArray();
  $.each(params, function (i, val) {
    formData.append(val.name, val.value);
  });
  return formData;
};

//获取url中的参数
function getUrlParam(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");  // 构造一个含有目标参数的正则表达式对象
  var r = window.location.search.substr(1).match(reg);  // 匹配目标参数
  if (r != null) return unescape(r[2]); return null;  // 返回参数值
}

function select_and_reverse() {
  // 全选反选
  $("input[type='checkbox'][name='item_ids']").click(function(){
    if($(this).prop('checked')){
      if($("input[name='item_ids'][type='checkbox']:checked").length == $("input[name='item_ids'][type='checkbox']").length){
        $("input[name='check_all']").prop("checked",true);
      }
    }else{
      $("input[name='check_all']").prop("checked",false);
    }
  });
  $("input[name='check_all']").click(function(){
    if($(this).prop('checked')){
      $("input[type='checkbox'][name='item_ids']").prop("checked",true);
    }else{
      $("input[type='checkbox'][name='item_ids']").prop("checked",false);
    }
  });
}
