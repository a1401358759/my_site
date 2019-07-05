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
        var comment_list = data.comment_list;
        html = '<div style="margin-top:60px;">';
        if (comment_list.length > 0) {
          html += '已有 <b>' + data.total + '</b> 条评论';
          for (i = 0; i < comment_list.length; i++) {
            html += '<div class="col-12">'
                + '<hr>'
                + '<a id=' + '"' + comment_list[i].anchor + '"' + 'class="comments_anchor">'
                + '<img src=' + '"' + comment_list[i].avatar + '"' + 'style="border:1px solid #eee;border-radius:50%;padding: 5px;">'
                + '<span>'
                +   '<strong style="margin-right:5px; font-size:15px;">'
                +      '<a href=' + '"' + comment_list[i].website + '"' + 'target="_blank" style="color:#1abc9c;">' + comment_list[i].nickname + '</a>'
                if (comment_list[i].blogger) {
                +  '<span style="background-color:red;color:#FFF;font-size:smaller;padding:2px 5px;border-radius:5px;">博主</span>'
                }
                +    '</strong>'
                +  '<a style="color:#ccc" href="javascript:;">'
                +      + comment_list[i].created_time +
                +  '</a>'
                +  '</span>'
                + '</a>'
                + '<div class="pull-right" style="margin-top: 15px;">'
                +  '<a href="#comment_form" class="text-muted" onclick="set_parent_comment_id(' + comment_list[i].comment_id + ',' + comment_list[i].nickname + ')">'
                +    '回复'
                +  '</a>'
                + '</div>'
                + '<div class="clearfix"></div>'
                if (comment_list[i].reply_to) {
                +  '<blockquote>'
                +    '<p>引用自 <a href=' + '"#' + comment_list[i].parent_anchor + '"' + '>@' + comment_list[i].reply_to_user + '</a> 的评论</p>'
                +    '<div class="quote-content needEmojiParse">' + comment_list[i].parent_content + '</div>'
                +  '</blockquote>'
                }
                + '<div style="margin-top:15px;" class="needEmojiParse">' + comment_list[i].content + '</div>'
               + '</div>'
             + '<hr>'
          + '</div>'
          }
          $("#comment_list").append(html);
        }
      } else {
        toastr["warning"](data.msg_cn);
      }
    },
    error: function () {
      toastr["error"]("网络错误！");
    }
  });
}
