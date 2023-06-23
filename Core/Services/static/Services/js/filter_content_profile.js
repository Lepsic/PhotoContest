function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');


$(document).ready(function () {
    let vbtn = $('#vbtn-radio0');
    vbtn.prop('checked', true);

    let radioValue = vbtn.val();
    $.ajax({
        url: '/account/profile/filterUserPhoto/',
        data: {'filter_type': radioValue},
        method: 'post',
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken},
        success: function (response) {
            let data = response.data;
            let tablePhoto = $('#table-photo tbody');
            tablePhoto.empty();
            for (let i = 0; i < data.length; i++) {
                let row = $('<tr>');
                row.append($('<td>').text(data[i].name));
                let imgCell = $('<td>');
                let img = $('<img src="" alt="Иди правь че сидишь?">');
                img.attr('src', 'data:image/png;base64,' + data[i].media);
                imgCell.append(img);
                row.append(imgCell);
                row.append($('<td>').text(data[i].description));
                row.append($('<td>').text(data[i].create_data));
                tablePhoto.append(row);
            }
        }
    });

    $('.btn-group-justified').on('click', '.btn', function (event) {
        let radioValue = $(this).val();
        $.ajax({
            url: '/account/profile/filterUserPhoto/',
            data: {'filter_type': radioValue},
            method: 'post',
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
            success: function (response) {
                let data = response.data;
                let tablePhoto = $('#table-photo tbody');
                tablePhoto.empty();
                for (let i = 0; i < data.length; i++) {
                    let row = $('<tr>');
                    row.append($('<td>').text(data[i].name));
                    let imgCell = $('<td>');
                    let img = $('<img src="" alt="Иди правь че сидишь?">');
                    img.attr('src', 'data:image/png;base64,' + data[i].media);
                    imgCell.append(img);
                    row.append(imgCell);
                    row.append($('<td>').text(data[i].description));
                    row.append($('<td>').text(data[i].create_data));
                    tablePhoto.append(row);
                }
            }
        });
    });
});