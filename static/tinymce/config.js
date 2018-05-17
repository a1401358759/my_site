tinyMCE.init({
    selector: 'textarea',
    theme : "modern",
    height: 450,
    plugins: [
      "advlist autolink autosave link image lists charmap print preview hr anchor pagebreak spellchecker",
      "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
      "table contextmenu directionality emoticons template textcolor paste fullpage save codesample"
    ],
    toolbar_items_size: 'small',
    toolbar1: " save undo redo | cut copy paste | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | styleselect formatselect fontselect fontsizeselect",
    toolbar2: " searchreplace | bullist numlist | outdent indent blockquote | link unlink anchor image media code | inserttime preview | forecolor backcolor | codesample",
    toolbar3: "table | hr removeformat | subscript superscript | charmap emoticons | print fullscreen | ltr rtl | spellchecker | visualchars visualblocks nonbreaking template pagebreak restoredraft",
    language:'zh_CN'
});
