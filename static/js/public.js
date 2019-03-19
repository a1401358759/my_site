function get_csrf_token() {
  return $("input[name='csrfmiddlewaretoken']").val();
}

function add_csrf_token(data) {
  data["csrfmiddlewaretoken"] = get_csrf_token();
  return data;
}

$(document).ajaxSend(function(event, xhr, settings) {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function sameOrigin(url) {
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
  }

  function safeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  }
});

// 获取url中的参数
function getUrlParam(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");  // 构造一个含有目标参数的正则表达式对象
  var r = window.location.search.substr(1).match(reg);   // 匹配目标参数
  if (r != null) return unescape(r[2]); return null;  // 返回参数值
}

var count=0;
function submitOnce (){
  if (count == 0){
    count ++;
    return true;
  } else{
    msg_info("正在操作，请勿重复提交");
    return false;
  }
}

function msg_info(msg, type, timeout) {
  if (!type) type = 'info';
  if (!timeout) timeout = 3000;
  var id = (new Date).getTime() + '' + parseInt(Math.random() * 100);
  var msg_html = '<div class="pad margin no-print" id="' + id + '">' +
    '<div class="alert alert-' + type + '" style="padding-bottom: 0!important;">' +
    '<h4><i class="fa fa-info"></i>&nbsp;&nbsp;' + msg + '</h4>' +
    '</div>' +
    '</div>';
  $('.content-header').after(msg_html);
  setTimeout(function () {
    $("#" + id).fadeOut();
  }, timeout);
  window.location.href = '#message-top';
}

// 动态修改URL参数
function changeUrlArg(url, arg, val){
  var pattern = arg+'=([^&]*)';
  var replaceText = arg+'='+val;
  return url.match(pattern) ? url.replace(eval('/('+ arg+'=)([^&]*)/gi'), replaceText) : (url.match('[\?]') ? url+'&'+replaceText : url+'?'+replaceText);
}

// 分转元
function fen_to_yuan(val, fixed_num, number) {
  if(fixed_num == null){
    fixed_num = 0;
  }
  if (number){
    return Number(Decimal.div(val, 100).toFixed(fixed_num));
  }
  return Decimal.div(val, 100).toFixed(fixed_num);
};

// 元转分
function yuan_to_fen(val) {
  return Decimal.mul(Number(val).toFixed(2), 100).toNumber();
};

// 折扣
function discount_trans(val) {
  return Decimal.div(Number(val).toFixed(2), 10).toNumber();
}

// 概率转换 *100
function chance_to_per(val) {
  return Decimal.mul(val, 100).toNumber();
}

// 概率转换 /100
function chance_to_dec(val) {
  return Decimal.div(val, 100).toNumber();
}

function percent_display(value, total) {
  // value相对于total以保留两位小数的百分比显示，比如 1 100 -> 1.00%
  if (total == 0) {
    return "0.00%";
  } else {
    return (value / total * 100).toFixed(2) + '%';
  }
}

function dateToString(date) {
  if (date instanceof Date) {
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    month = month < 10 ? '0' + month : month;
    var day = date.getDate();
    day = day < 10 ? '0' + day : day;
    return year + "" + month + "" + day;
  }
  return '';
}

function isIdCard(cardid) {
  // 身份证正则表达式(18位)
  var isIdCard2 = /^[1-9]\d{5}(19\d{2}|[2-9]\d{3})((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])(\d{4}|\d{3}X)$/i;
  var stard = "10X98765432";  // 最后一位身份证的号码
  var first = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];  // 1-17系数
  var sum = 0;
  if (!isIdCard2.test(cardid)) {
    return false;
  }
  var year = cardid.substr(6, 4);
  var month = cardid.substr(10, 2);
  var day = cardid.substr(12, 2);
  var birthday = cardid.substr(6, 8);
  if (birthday != dateToString(new Date(year+'/'+month+'/'+day))) {  // 校验日期是否合法
    return false;
  }
  for (var i = 0; i < cardid.length - 1; i++) {
    sum += cardid[i] * first[i];
  }
  var result = sum % 11;
  var last = stard[result]; // 计算出来的最后一位身份证号码
  if (cardid[cardid.length - 1].toUpperCase() == last) {
    return true;
  } else {
    return false;
  }
}

// 验证中文名称
function isChinaName(name) {
  var pattern = /^[\u4E00-\u9FA5]{1,6}$/;
  return pattern.test(name);
}

// 验证手机号
function isPhoneNo(phone) {
  var pattern = /^1[3|4|5|6|7|8|9][0-9]{9}$/;
  return pattern.test(phone);
}

// 验证邮箱
function isEmail(email) {
  var pattern = /\w+[@]{1}\w+[.]\w+/;
  return pattern.test(email);
}
