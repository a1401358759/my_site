tinyMCE.init({
  selector: 'textarea',
  theme : "modern",
  height: 450,
  plugins: [
    "advlist autolink autosave link imageupload lists charmap print preview hr anchor pagebreak",
    "searchreplace wordcount code fullscreen insertdatetime media nonbreaking",
    "table contextmenu directionality emoticons textcolor paste fullpage save codesample"
  ],
  toolbar_items_size: 'small',
  toolbar1: " save undo redo | cut copy paste | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | styleselect formatselect fontselect fontsizeselect",
  toolbar2: " searchreplace | bullist numlist | outdent indent | link unlink anchor imageupload media code | inserttime preview | forecolor backcolor | codesample",
  toolbar3: "table | hr removeformat | subscript superscript | charmap emoticons | print fullscreen | nonbreaking pagebreak restoredraft",
  language:'zh_CN',
  imageupload_url: '/upload/',
});
