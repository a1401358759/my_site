// 已切换为leanapp国际版
new Valine({
  av: AV,
  el: '#vcomments',
  appId: 'n0hsEqsFy4WbCYQOfw05K8u1-MdYXbMMI',
  appKey: 'GMXGgt62FOylOKhMDYfb9tGc',
  avatar: 'mp',
  placeholder: 'ヾﾉ≧∀≦)o 来啊，快活啊!',
  visitor: true,
  enableQQ: true,
  recordIP: true,
  requiredFields: ['nick', 'mail'],
  emojiCDN: 'https://valinecdn.bili33.top/',
  emojiMaps: emojiMaps,
  tagMeta: ['博主', '', ''],
  master: ['165de1e1c5d38358083e2c6dc8fe2886'],  // gravatar头像hash
});

// 解决valine-admin云引擎唤醒失败
var engine = document.cookie.replace(/(?:(?:^|.*;\s*)engine\s*\=\s*([^;]*).*$)|^.*$/, "$1") || '0';
if(engine!='1') {
  fetch('https://quan.suning.com/getSysTime.do')
  .then(function(response) {
    return response.json();
  })
  .then(function(date) {
    var hours = new Date(date.sysTime2).getHours();
    if(hours>7 && hours<23){
      fetch('https://daniel.avosapps.us');
      var exp = new Date(date.sysTime2);
      exp.setTime(exp.getTime() + 20*60*1000);
      document.cookie = "engine=1;path=/;expires="+ exp.toGMTString();
    }
  })
}

// 解析jQuery-emoji表情
var tur = true;
function parse_emoji() {
  jQuery(".vcontent").emojiParse({
    basePath: '/static/plugins/jQuery-emoji/images/emoji',
    icons: emojiLists   // 注：详见 js/emoji.list.js
  });
  tur = true;
}

window.onscroll = function(){
  if (tur) { setTimeout(parse_emoji, 100); tur = false;
  } else { }
}

jQuery(".vmore").on("click", function() {
  setTimeout(parse_emoji, 100);
});
