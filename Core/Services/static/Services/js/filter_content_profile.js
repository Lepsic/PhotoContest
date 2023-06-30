let csrftoken = getCookie('csrftoken');
let sessionid = getCookie('sessionid');


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


let tablePhoto = $('#table-photo tbody');
function ShowApproved(response){
            let data = response.data;
            tablePhoto.empty();
            for (let i = 0; i < data.length; i++) {
                let buttonCellRemove = $('<td>');
                let buttonRemove = $('<button class="btn btn-outline-dark">').text('Удалить');
                let buttonCellChange = $('<td>');
                let buttonChange = $('<button class="btn btn-outline-dark">').text('Изменить');
                buttonCellRemove.append(buttonRemove)
                buttonCellChange.append(buttonChange)
                let row = $('<tr>');
                row.append($('<td>').text(data[i].name));
                let imgCell = $('<td>');
                let img = $('<img src="" alt="Иди правь че сидишь?">');
                img.attr('src', 'data:image/png;base64,' + data[i].media);
                imgCell.append(img);
                row.append(imgCell);
                row.append($('<td>').text(data[i].description));
                row.append($('<td>').text(data[i].created_data));
                row.append(buttonCellRemove)
                row.append(buttonCellChange)


                buttonRemove.click(function () {
                    fetch('delete', {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken,
                            'X-SessionId': sessionid
                        },
                        body: JSON.stringify({id: data[i].id})
                    })
                    .then(function(response) {
                        if (response.ok) {
                            console.log('Работает')
                            $(document).ready(function () {
                                let radioValue = $('input[name="vbtn-radio"]:checked').val();
                                console.log(radioValue)
                                $.ajax({
                                    url: '/account/profile/filterUserPhoto/',
                                    data: {'filter_value': radioValue},
                                    method: 'post',
                                    dataType: 'json',
                                    headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                                    success: function (response){
                                        ShowApproved(response)
                                    }
                                });
                            });
                          return true;
                        } else {
                          throw new Error('Ошибка запроса: ' + response.status);
                        }
                      })
                      .then(function(result) {
                        console.log(result);
                      })
                      .catch(function(error) {
                        console.error(error);
                      });

                });


                tablePhoto.append(row);}





            }






function Request(response, radioValue) {
  let data = response.data;
  tablePhoto.empty();
  for (let i = 0; i < data.length; i++) {
    let row = $('<tr>');
    row.append($('<td class="text-center">').text(data[i].name));
    let imgCell = $('<td class="text-center">');
    let img = $('<img src="" alt="Иди правь че сидишь?" class="text-center">');
    img.attr('src', 'data:image/png;base64,' + data[i].media);
    imgCell.append(img);
    row.append(imgCell);
    row.append($('<td class="text-center">').text(data[i].description));
    row.append($('<td class="text-center">').text(data[i].created_data));
    tablePhoto.append(row);
  }
}



$(document).ready(function () {
    let radioValue = $('input[name="vbtn-radio"]:checked').val();
    $.ajax({
        url: '/account/profile/filterUserPhoto/',
        data: {'filter_value': radioValue},
        method: 'post',
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){
            Request(response, radioValue)
        }
    });
});


    $('.btn-group-justified').on('change', '.btn-check', function (event) {
        let radioValue = $('input[name="vbtn-radio"]:checked').val();
        console.log(radioValue);
    $.ajax({
        url: '/account/profile/filterUserPhoto/',
        data: {'filter_value': radioValue},
        method: 'post',
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){
            if(radioValue == 1){
                ShowApproved(response)
            }
            else{
                Request(response)
            }

        }
    });
})
