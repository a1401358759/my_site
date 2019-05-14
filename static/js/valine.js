new Valine({
  av: AV,
  el:'#vcomments',
  appId:'2pSOFwxMUB0mHbMHpCH9bhRL-gzGzoHsz',
  appKey:'zkBqvFzJ7NswaFW6oGICyKpq',
  notify:false,
  verify: false,
  avatar:'mp',
  placeholder:'ヾﾉ≧∀≦)o来啊，快活啊!',
  visitor:true,
});

$(".v .vbtn").html("提交");
$(".vemoji-btn").html("表情");
$(".vpreview-btn").html("预览");

window.onload=function(){
  // jQuery emoji 解析
  jQuery(".vcontent").emojiParse({
    basePath: '/static/plugins/jQuery-emoji/images/emoji',
    icons: emojiLists   // 注：详见 js/emoji.list.js
  });
  // jquery emoji 初始化
  jQuery(".veditor").emoji({
    showTab: true,
    animation: 'slide',
    basePath: '/static/plugins/jQuery-emoji/images/emoji',
    icons: emojiLists  // 注：详见 js/emoji.list.js
  });
};
