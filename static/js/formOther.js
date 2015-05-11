$(function(){
	$(parent.document.getElementById("pageLoader")).hide();
	$('input').each(function(){
      if(!$(this).hasClass('form-control')) {
        $(this).addClass('form-control');
      }
    })
    $('select').each(function(){
      if(!$(this).hasClass('form-control')) {
        $(this).addClass('form-control');
      }
    })
})