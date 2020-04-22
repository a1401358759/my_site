// 已切换为leanapp国际版
new Valine({
  av: AV,
  el: '#vcomments',
  appId: 'n0hsEqsFy4WbCYQOfw05K8u1-MdYXbMMI',
  appKey: 'GMXGgt62FOylOKhMDYfb9tGc',
  avatar:'mp',
  placeholder: 'ヾﾉ≧∀≦)o 来啊，快活啊!',
  visitor: true,
  // emojiCDN: '/static/plugins/jQuery-emoji/images/emoji/qq/',
  // emojiMaps: {
  // }
});

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
