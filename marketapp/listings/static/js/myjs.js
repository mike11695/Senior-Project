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

endpoint = "/listings/search-listings"

$(document).ready(function() {
  let scheduled_function = false

  let ajax_call = function (endpoint, request_parameters) {
      $.getJSON(endpoint, request_parameters)
          .done(response => {
              $('#listings-content').fadeTo('slow', 0).promise().then(() => {
                  $('#listings-content').html(response['html_from_view'])
                  $('#listings-content').fadeTo('fast', 1)
              })
          })
  }

  $("#user-input").on('keyup', function () {
    const request_parameters = {
        name: $('#user-input').val(),
        type: $('#listing-types').val(),
        tags: $('#tags option:selected').toArray().map(item => item.value).join(),
        searchRadius: $('#search-radius').val()
    }
    console.log(request_parameters)

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, 500, endpoint, request_parameters)
  })

  $('select[name="listing-types"]').change(function(){
    const request_parameters = {
        name: $('#user-input').val(),
        type: $('#listing-types').val(),
        tags: $('#tags option:selected').toArray().map(item => item.value).join(),
        searchRadius: $('#search-radius').val()
    }
    console.log(request_parameters)

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, 500, endpoint, request_parameters)
  })

  $('select[name="search-radius"]').change(function(){
    const request_parameters = {
        name: $('#user-input').val(),
        type: $('#listing-types').val(),
        tags: $('#tags option:selected').toArray().map(item => item.value).join(),
        searchRadius: $('#search-radius').val()
    }
    console.log(request_parameters)

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, 500, endpoint, request_parameters)
  })

  $('select[name="tags"]').change(function(){
    const request_parameters = {
        name: $('#user-input').val(),
        type: $('#listing-types').val(),
        tags: $('#tags option:selected').toArray().map(item => item.value).join(),
        searchRadius: $('#search-radius').val()
    }
    console.log(request_parameters)

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, 500, endpoint, request_parameters)
  })
})
