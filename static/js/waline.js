// 已切换为 Waline
Waline({
  el: '#waline',
  serverURL: 'https://waline-5gsb5pbr4d74c22a-1256044091.ap-guangzhou.app.tcloudbase.com/waline',
  copyright: false,
});

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
