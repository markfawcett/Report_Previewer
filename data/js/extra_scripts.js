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
    //select element, copy text then remove
    tempContainer.select();
    document.execCommand('copy');
    tempContainer.remove();
  });
  $('.contents-heading').each(function(){
    var report_location = window.location.href.replace(/\#.*/g, '');
    var list_items='<li>'+'<a href="' + report_location+'#'+this.id + '">&#8212; '+this.innerText+'</a>'+'</li>';
    $('#contents-links').append(list_items);
  });
});