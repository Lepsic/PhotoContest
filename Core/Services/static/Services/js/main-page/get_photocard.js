import generatePages from './render.js';

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

let csrftoken = getCookie('csrftoken');
let sessionid = getCookie('sessionid');
const scriptElement = document.querySelector('script[src$="get_photocard.js"]');
const image_id = scriptElement.getAttribute('image-id');

console.log(image_id)
function get_photo(id){
    $.ajax({
    url: 'content/',
    data: {'image_id': id},
    method: 'POST',
    dataType: 'json',
    headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
    success: function (response){
        generatePages(response.data)
        console.log(response.data);
    }

})}

get_photo(image_id);