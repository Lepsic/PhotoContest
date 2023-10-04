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
function createElement(tag, classNames) {
    const element = document.createElement(tag);
    if(classNames){
        element.classList.add(...classNames);
    }
    return element;
}

let csrftoken = getCookie('csrftoken');
let sessionid = getCookie('sessionid');

const baseURL = window.location.origin + '/';
console.log(baseURL);
const bodyContainer = document.getElementById('body')
const searchButton = document.getElementById('searchButton');
const searchInput = document.getElementById('searchInput');



function getStackRejected(){
     $.ajax({
         url: baseURL + 'moderation/rejects/',
         dataType: 'json',
         method: 'get',
         headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
         success: function (response) {
             bodyContainer.innerHTML = '';
             let table = document.createElement("table");
             table.classList.add("table");
             let thead = document.createElement('thead');
             let headerRow = document.createElement('tr');
             headerRow.innerHTML = '<th>Название</th><th>Описание</th><th>Фото</th>';
             thead.appendChild(headerRow);
             table.appendChild(thead);
             bodyContainer.appendChild(table);
             let data = response.data;
             let tbody = document.createElement('tbody');
             for (let i = 0; i < data.length; i++) {
                 let row = document.createElement('tr');
                 let namePhoto = document.createElement('td');
                 namePhoto.textContent = data[i].name;
                 let descriptionPhoto = document.createElement('td');
                 descriptionPhoto.textContent = data[i].description;
                 let photoImgCell = document.createElement('td');
                 let img = $('<img src="" alt="Photo" class="text-center" >');
                 img.attr('src', 'data:image/png;base64,' + data[i].media);
                 photoImgCell.append(img[0]);
                 let cancelRejectButton = $('<button class="btn btn-danger">').text('Отправить на модерацию');
                 cancelRejectButton.click(function (){
                     $.ajax({
                         url: baseURL + 'moderation/rejects/cancel/',
                         dataType: 'JSON',
                         method: 'post',
                         data: {'id': data[i].id},
                         headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                         success: function (response){
                             getStackRejected();
                         }
                     })
                 })
                 row.append(namePhoto);
                 row.append(descriptionPhoto);
                 row.append(photoImgCell);
                 row.append(cancelRejectButton[0]);
                 tbody.append(row);
             }
             table.append(tbody);
         }
     })}



function getStackPublication(){
    $.ajax({
        url: baseURL + 'moderation/publications/',
        dataType: 'json',
        method: 'get',
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){
            bodyContainer.innerHTML = '';
            let table = document.createElement("table");
            table.classList.add("table");
            let thead = document.createElement('thead');
            let headerRow = document.createElement('tr');
            headerRow.innerHTML = '<th>Название</th><th>Описание</th><th>Фото</th>';
            thead.appendChild(headerRow);
            table.appendChild(thead);
            bodyContainer.appendChild(table);
            let data = response.data;
            let tbody = document.createElement('tbody');
            for (let i = 0; i<data.length; i++){
                let row = document.createElement('tr');
                let namePhoto = document.createElement('td');
                namePhoto.textContent = data[i].name;
                let descriptionPhoto = document.createElement('td');
                descriptionPhoto.textContent = data[i].description;
                let photoImgCell = document.createElement('td');
                let img = $('<img src="" alt="Photo" class="text-center" >');
                img.attr('src', 'data:image/png;base64,' + data[i].media);
                photoImgCell.append(img[0]);
                let approvedButton = $('<button class="btn btn-danger">').text('Опубликовать фото');
                let rejectedButton = $('<button class="btn btn-danger">').text('Отклонить фото');
                row.append(namePhoto);
                row.append(descriptionPhoto);
                row.append(photoImgCell);
                row.append(approvedButton[0]);
                row.append(rejectedButton[0]);
                tbody.append(row);
                approvedButton.click(function (){
                    $.ajax({
                        url: baseURL + 'moderation/publications/publish/',
                        method: 'post',
                        dataType: 'json',
                        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                        data: {'id': data[i].id},
                        success: function (response) {
                            getStackPublication();
                        }
                    })
                })
                rejectedButton.click(function (){
                    $.ajax({
                        url: baseURL + 'moderation/publications/publish/reject/',
                        method: 'post',
                        dataType: 'json',
                        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                        data: {'id': data[i].id},
                        success: function (response) {
                            getStackPublication();
                        }
                    })
                })


            }
            table.appendChild(tbody);
        }
    })
}

function getStackChange(){
    $.ajax({
        url: baseURL + 'moderation/changes/',
        dataType: 'json',
        method: 'get',
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){
            bodyContainer.innerHTML = '';
            let table = document.createElement("table");
            table.classList.add("table");
            let thead = document.createElement('thead');
            let headerRow = document.createElement('tr');
            headerRow.innerHTML = '<th>Название</th><th>Описание</th><th>Исходное Фото</th> <th>Обновленное Фото</th>';
            thead.appendChild(headerRow);
            table.appendChild(thead);
            bodyContainer.appendChild(table);
            let data = response.data;
            let tbody = document.createElement('tbody');
            for (let i = 0; i<data.length; i++){
                let row = document.createElement('tr');
                let namePhoto = document.createElement('td');
                namePhoto.textContent = data[i].name;
                let descriptionPhoto = document.createElement('td');
                descriptionPhoto.textContent = data[i].description;
                let photoImgSourceCell = document.createElement('td');
                let imgSource = $('<img src="" alt="Photo" class="text-center" >');
                imgSource.attr('src', 'data:image/png;base64,' + data[i].media);
                photoImgSourceCell.append(imgSource[0]);
                let photoImgUpdateCell = document.createElement('td');
                let imgUpdate = $('<img src="" alt="Photo" class="text-center" >');
                imgUpdate.attr('src', 'data:image/png;base64,' + data[i].source_media);
                photoImgUpdateCell.append(imgUpdate[0]);
                let approvedButton = $('<button class="btn btn-danger">').text('Опубликовать изменения');
                let rejectedButton = $('<button class="btn btn-danger">').text('Отклонить изменения');
                row.append(namePhoto);
                row.append(descriptionPhoto);
                row.append(photoImgUpdateCell);
                row.append(photoImgSourceCell);
                row.append(approvedButton[0]);
                row.append(rejectedButton[0]);
                tbody.append(row);
                approvedButton.click(function (){
                    $.ajax({
                        url: baseURL + 'moderation/changes/approve/',
                        dataType: 'json',
                        method: 'POST',
                        data: {'id': data[i].id},
                        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                        success: function (){
                            getStackChange();
                        }
                    })
                })
                rejectedButton.click(function(){
                    $.ajax({
                        url: baseURL + 'moderation/changes/cancel/',
                        dataType: 'json',
                        method: 'POST',
                        data: {'id': data[i].id},
                        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                        success: function (){
                            getStackChange();
                        }
                    })
                })

    }
            table.append(tbody);
        }
        })
            }




 $('.btn-group-justified').on('change', '.btn-check', function (event){
     let radioValue = $('input[name="radioBtn"]:checked').val();
     if(radioValue === 'PublicStack'){
         getStackPublication();
     }
     else if(radioValue === 'ChangeStack'){
         getStackChange();
     }
     else if(radioValue === 'RejectStack'){
         getStackRejected();
     }
 })

$(document).ready(function () {
      getStackPublication()
    })

searchButton.addEventListener('click', function (event){
    event.preventDefault();
    $.ajax({
        url: baseURL + 'moderation/notification/',
        method: 'POST',
        dataType: 'JSON',
        data: {'text': searchInput.value},
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){
            searchInput.value = '';
        }
    })
})