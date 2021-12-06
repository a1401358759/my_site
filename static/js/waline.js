// 中文默认
const locale = {
  nick: '昵称',
  nickError: '昵称不能少于3个字符',
  mail: '邮箱',
  mailError: '请填写正确的邮件地址',
  link: '网址',
  placeholder: '欢迎评论，评论需要审核，敬请谅解',
  sofa: '来发评论吧~',
  submit: '提交',
  reply: '回复',
  cancelReply: '取消回复',
  comment: '评论',
  more: '加载更多...',
  preview: '预览',
  emoji: '表情',
  uploadImage: '上传图片',
  seconds: '秒前',
  minutes: '分钟前',
  hours: '小时前',
  days: '天前',
  now: '刚刚',
  uploading: '正在上传',
  login: '登录',
  logout: '退出',
  admin: '博主',
  word: '字',
  wordHint: '评论字数应在 $0 到 $1 字之间！\n当前字数：$2',
};
// 已切换为 Waline
Waline({
  el: '#waline',
  serverURL: 'https://waline-5gsb5pbr4d74c22a-1256044091.ap-guangzhou.app.tcloudbase.com/waline',
  copyright: false,
  locale
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
