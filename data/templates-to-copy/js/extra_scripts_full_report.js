$(window).bind("load", function() {
  $('#copyURL').click(function(event){
    event.preventDefault();
    $(this).text(' Copied');
    setTimeout(function(){
      $('#copyURL').html('<i class="fas fa-link"></i> Copy URL');
    }, 1500);
    var tempContainer = $('<textarea></textarea>');
    tempContainer.val(window.location.href.replace(/\#.*/gi, ''));
    tempContainer.attr('readonly', true);
    tempContainer.css({
     'position': 'fixed',
     'bottom': '0',
     'top': '0'
    })
    $('body').append(tempContainer);
    tempContainer.select();
    document.execCommand('copy');
    tempContainer.remove();
  });
  
  $("sup").on("click", function(t) {
      t.preventDefault();
      var supReg = new RegExp(/(\d+$)/,'gi'),
          supID = $(this).attr("id"),
          matches = supReg.exec(supID),
          a = $("#ftn" + matches[1]).offset().top;
      $("html, body").animate({
          scrollTop: a - "55"
      }, "medium")
  });
  $(".FootnoteText").on("click", function(t) {
      t.preventDefault();
      var refReg = new RegExp(/(\d+$)/,'gi'),	
	        refID = $(this).attr("id"),
	        matches = refReg.exec(refID),
          a = $("#_ftnref" + matches[1]).offset().top;
      $("html, body").animate({
          scrollTop: a - "100"
      }, "medium")
  });
  $('.contents-heading').each(function(){
    var report_location = window.location.href.replace(/\#.*/g, '');
    var list_items='<li>'+'<a href="' + report_location+'#'+this.id + '">&#8212; '+this.innerText+'</a>'+'</li>';
    $('#contents-links').append(list_items);
  });
});