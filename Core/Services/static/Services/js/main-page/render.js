// Функция для создания элемента с заданным тегом и классами
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

function createElement(tag, classNames) {
    const element = document.createElement(tag);
    element.classList.add(...classNames);
    return element;
}


// Функция для обработки лайка фотографии
function likePhoto(photoId) {
    // Отправка запроса на сервер для обработки лайка фотографии с идентификатором photoId
    let count;

    $.ajax({
        url: '/content/like/',
        data: {'photo_id': photoId},
        method: 'POST',
        dataType: 'JSON',
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){
            count = response.count_likes
            let likeButton = document.getElementById('likeButton'+photoId);
            if(likeButton.className === 'btn btn-primary'){
                likeButton.className = 'btn btn-danger';
                likeButton.textContent = 'Лайк ' + count
                }
            else{
                likeButton.className = 'btn btn-primary';
                likeButton.textContent = 'Лайк ' + count
                }

        }
    })




}

// Функция для загрузки и отображения комментариев для фотографии
function showComments(photoId) {
    // Отправка запроса на сервер для получения комментариев для фотографии с идентификатором photoId
    // После получения ответа от сервера, создание элементов комментариев и их добавление в соответствующий блок
}

// Функция для генерации страницы с фотографиями
function generatePage(photos) {
    const container = document.querySelector('.container');


    // Создание заголовка
    const heading = createElement('h1', ['mt-5']);
    heading.textContent = 'Конкурс фотографий';
    container.appendChild(heading);

    // Создание карточек фотографий
    photos.forEach(photo => {
        const card = createElement('div', ['card', 'mb-3']);
        container.appendChild(card);

        const image = createElement('img', ['card-img-top']);
        image.src = 'data:image/png;base64,' + photo.media;
        image.alt = 'Фотография';
        card.appendChild(image);

        const cardBody = createElement('div', ['card-body']);
        card.appendChild(cardBody);

        const title = createElement('h5', ['card-title']);
        title.innerHTML = photo.name + "<br>Дата публикации: " + photo.created_data;
        cardBody.appendChild(title);

        const description = createElement('p', ['card-text']);
        description.textContent = photo.description;
        cardBody.appendChild(description);


        const buttonsWrapper = createElement('div', ['d-flex', 'justify-content-between']);
        cardBody.appendChild(buttonsWrapper);


        if(photo.like_exist === "False"){
            let likeButton = createElement('button', ['btn', 'btn-primary']);
            likeButton.textContent = 'Лайк ' + photo.like_count ;
            likeButton.addEventListener('click', () => likePhoto(photo.id));
            likeButton.setAttribute('id', 'likeButton' + photo.id);
            buttonsWrapper.appendChild(likeButton);
        }
        else{
            let likeButton = createElement('button', ['btn', 'btn-danger']);
            likeButton.textContent = 'Лайк ' + photo.like_count ;
            likeButton.addEventListener('click', () => likePhoto(photo.id));
            likeButton.setAttribute('id', 'likeButton' + photo.id);
            buttonsWrapper.appendChild(likeButton);
        }


        const commentsButton = createElement('button', ['btn', 'btn-secondary']);
        commentsButton.textContent = 'Показать комментарии: ' +'('+ photo.comment_count + ')';
        commentsButton.addEventListener('click', () => showComments(photo.id));
        buttonsWrapper.appendChild(commentsButton);

        const commentsBlock = createElement('div', []);
        commentsBlock.id = 'comments-'+photo.id;
        commentsBlock.style.display = 'none';
        cardBody.appendChild(commentsBlock);

        image.addEventListener('mouseenter', () => {
            description.style.display = 'block';
        });

        image.addEventListener('mouseleave', () => {
            description.style.display = 'none';
        });

    });
}

// Пример данных о фотографиях

/*

const photosData = [
    {
        id: 1,
        image: 'path/to/image1.jpg',
        title: 'Фотография 1',
        description: 'Описание фотографии 1',
        count_likes: '11',
        count_comments: '8',
        data_created: '02.08.2023'
    },
    {
        id: 2,
        image: 'path/to/image2.jpg',
        name: 'Фотография 2',
        description: 'Описание фотографии 2',
        like_count: '25',
        comment_count: '16',
        created_data: '02.08.2023'
    },
    {
        name: "сыбака",
        media: "iVBORw0KGgoAAAANSUhEUgAA…qxKKHHdAAAAAElFTkSuQmCC",
        created_data: "2023-08-02",
        description: "",
        id: 1,
        user:1,
        like_exist: 'False',
        like_count: 0,
        comment_count:0
    }
];

Генерация страницы с фотографиями
generatePage(photosData);
*/

export default generatePage;