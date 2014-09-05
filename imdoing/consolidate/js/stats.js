var ajaxForm = $("#ajaxForm")
  , ajaxDiv = $("#ajaxDiv");

ajaxForm.change(function(){
  ajaxDiv.fadeOut(200, function(){
    ajaxForm.submit();
  });
});

setInterval(function(){
  ajaxForm.submit();
}, 10000);

ajaxForm.submit();