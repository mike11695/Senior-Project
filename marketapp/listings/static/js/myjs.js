function select_all()  {
     $('input[type=checkbox]').prop('checked', true);
     document.getElementById('select-btn').setAttribute('onclick','deselect_all()')
     $('#select-btn').text('Deselect All')
}

function deselect_all()  {
     $('input[type=checkbox]').prop('checked', false);
     document.getElementById('select-btn').setAttribute('onclick','select_all()')
     $('#select-btn').text('Select All')
}

function favorite(id) {
    var catid = $('#listing' + id).attr("data-catid");
    var data = {'listing_id': catid}
    $.ajax(
    {
        type: "POST",
        url: "/listings/favorites/favorite-listing",
        data: data,
        success: function()
        {
            if (document.getElementById("fave-btn" + id).classList.contains('fas')) {
              document.getElementById("fave-btn" + id).classList.remove('fas');
              document.getElementById("fave-btn" + id).classList.add('far');
            } else {
              document.getElementById("fave-btn" + id).classList.remove('far');
              document.getElementById("fave-btn" + id).classList.add('fas');
            }
        }
     })
}
