function favorite() {
    alert("Clicky click");
    var catid = $('.favorite-listing').attr("data-catid");
    var data = {'listing_id': catid}
    $.ajax(
    {
        type: "POST",
        url: "/listings/favorites/favorite-listing",
        data: data,
        success: function()
        {
            if (document.getElementById("fave-btn").classList.contains('fas')) {
              document.getElementById("fave-btn").classList.remove('fas');
              document.getElementById("fave-btn").classList.add('far');
            } else {
              document.getElementById("fave-btn").classList.remove('far');
              document.getElementById("fave-btn").classList.add('fas');
            }
        }
     })
});
