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
