// 设置当前页面路径
$("#target").val(window.location.pathname);
// jQuery emoji 解析
jQuery(".needEmojiParse").emojiParse({
  basePath: '/static/plugins/jQuery-emoji/images/emoji',
  icons: emojiLists   // 注：详见 js/emoji.list.js
});
// jquery emoji 初始化
jQuery("#comment_content").emoji({
  showTab: true,
  animation: 'slide',
  basePath: '/static/plugins/jQuery-emoji/images/emoji',
  icons: emojiLists  // 注：详见 js/emoji.list.js
});
// 设置评论父级id
function set_parent_comment_id(comment_id, nickname) {
  var placeholder = "@" + nickname;
  document.getElementById('parent_comment_id').value = comment_id;
  jQuery("#comment_content").attr("placeholder", placeholder).focus();
};
// 提交评论
function add_comments(){
  var formData = jQuery('#comment_form').serialize();
  jQuery.ajax({
    url: "/add-comments/",
    type: 'POST',
    data: formData,
    success: function (data) {
      if (data.code == 0) {
        toastr["success"]("评论成功！");
        setTimeout(function(){window.location.reload();}, 1000);
      } else {
        toastr["warning"](data.msg_cn);
      }
    },
    error: function () {
      toastr["error"]("网络错误！");
    }
  });
}
// 获取评论
function get_comments(target){
  jQuery.ajax({
    url: "/get-comments/",
    type: 'GET',
    data: {
      "target": target
    },
    success: function (data) {
      if (data.code == 0) {
        // toastr["success"]("评论成功！");
        // setTimeout(function(){window.location.reload();}, 1000);
      } else {
        toastr["warning"](data.msg_cn);
      }
    },
    error: function () {
      toastr["error"]("网络错误！");
    }
  });
}
