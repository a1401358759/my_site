// 已切换为leanapp国际版
new Valine({
  av: AV,
  el: '#vcomments',
  appId: 'n0hsEqsFy4WbCYQOfw05K8u1-MdYXbMMI',
  appKey: 'GMXGgt62FOylOKhMDYfb9tGc',
  avatar:'mp',
  placeholder: 'ヾﾉ≧∀≦)o 来啊，快活啊!',
  visitor: true,
  // emojiCDN: 'https://emoji.yangsihan.com/',
  // emojiMaps: {
  //   '133': '133.png'
  // }
});

function parse_emoji() {
  jQuery(".vcontent").emojiParse({
    basePath: '/static/plugins/jQuery-emoji/images/emoji',
    icons: emojiLists   // 注：详见 js/emoji.list.js
  });
}

setTimeout(function() {
  // jQuery emoji 解析
  parse_emoji();

  jQuery(".vmore").on("click", function() {
    setTimeout(function() {
      parse_emoji();
    }, 500);
  });
}, 800)
