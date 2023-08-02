// Функция для создания элемента с заданным тегом и классами


function createElement(tag, classNames) {
    const element = document.createElement(tag);
    element.classList.add(...classNames);
    return element;
}

// Функция для обработки лайка фотографии
function likePhoto(photoId) {
    // Отправка запроса на сервер для обработки лайка фотографии с идентификатором photoId
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
        image.src = photo.image;
        image.alt = 'Фотография';
        card.appendChild(image);

        const cardBody = createElement('div', ['card-body']);
        card.appendChild(cardBody);

        const title = createElement('h5', ['card-title']);
        title.innerHTML = photo.title + "<br>Дата публикации: " + photo.data_created;
        cardBody.appendChild(title);

        const description = createElement('p', ['card-text']);
        description.textContent = photo.description;
        cardBody.appendChild(description);


        const buttonsWrapper = createElement('div', ['d-flex', 'justify-content-between']);
        cardBody.appendChild(buttonsWrapper);

        const likeButton = createElement('button', ['btn', 'btn-primary']);
        likeButton.textContent = 'Лайк ' + photo.count_likes ;
        likeButton.addEventListener('click', () => likePhoto(photo.id));
        buttonsWrapper.appendChild(likeButton);

        const commentsButton = createElement('button', ['btn', 'btn-secondary']);
        commentsButton.textContent = 'Показать комментарии: ' +'('+ photo.count_comments + ')';
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
        title: 'Фотография 2',
        description: 'Описание фотографии 2',
        count_likes: '25',
        count_comments: '16',
        data_created: '02.08.2023'
    }
];

// Генерация страницы с фотографиями
generatePage(photosData);