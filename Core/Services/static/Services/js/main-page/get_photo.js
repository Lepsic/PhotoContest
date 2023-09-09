import generatePages from './render.js';


let csrftoken = getCookie('csrftoken');
let sessionid = getCookie('sessionid');
let container = document.querySelector('.container');
let searchButton = document.getElementById('searchButton');
let searchInput = document.getElementById('searchInput');

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

function get_photo_sorted(sort_data){
    $.ajax({
    url: '/content/photo/',
    data: {'sort_type': sort_data},
    method: 'POST',
    dataType: 'json',
    headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
    success: function (response){
        generatePages(response.data)
        console.log(response.data);
    }

});
}


$(document).ready(function (){
    get_photo_sorted('create_data')
})


$('.btn-group-justified').on('change', '.btn-check', function (event) {
    let radioValue = $('input[name="radioBtn"]:checked').val();
    console.log(radioValue);
    container.innerHTML="";
    get_photo_sorted(radioValue)
});


searchButton.addEventListener('click',function (event) {
    event.preventDefault();
    console.log(searchInput.value);
    $.ajax({
        url: '/content/photo/search/',
        dataType: 'json',
        method: 'POST',
        data: {'searchData': searchInput.value},
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){
            container.innerHTML="";
            generatePages(response.data)
        }
    })
    searchInput.value = '';
})