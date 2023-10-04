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
    if(classNames){
        element.classList.add(...classNames);
    }
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
function postComments(postData){
    $.ajax({
        url: '/content/comment/post/',
        data: postData,
        method: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){

        }
    })
}

function initButtonWrapper(buttonWrapper){

}







function addButtonWrapper(element, userId){
    let buttonsWrapper = createElement('div', ['button-wrapper']);
    if (String(userId) === element.getAttribute('userid')){
              let commentsButtonResponse = createElement('button', ['btn', 'btn-secondary', 'btn-sm',
              'btn-comment-wrapper']);
              let commentButtonEdit = createElement('button', ['btn', 'btn-secondary', 'btn-sm',
                  'btn-comment-wrapper']);
              let commentButtonDelete = createElement('button', ['btn', 'btn-secondary', 'btn-sm',
                  'btn-comment-wrapper']);
              commentButtonDelete.textContent = 'Удалить';
              commentButtonEdit.textContent = 'Изменить';
              commentsButtonResponse.textContent = 'Ответить';
              commentsButtonResponse.id = 'buttonResponse';
              commentButtonEdit.id = 'buttonEdit';
              commentButtonDelete.id = 'buttonDelete';


              buttonsWrapper.append(commentsButtonResponse);
              buttonsWrapper.append(commentButtonDelete);
              buttonsWrapper.append(commentButtonEdit);
        }
        else{
            let commentsButtonResponse = createElement('button', ['btn', 'btn-secondary', 'btn-sm',
              'btn-comment-wrapper']);
            commentsButtonResponse.textContent = 'Ответить';
            buttonsWrapper.append(commentsButtonResponse);
        }
        element.appendChild(buttonsWrapper);

        return buttonsWrapper;
}

function createActionButtonWrapper(buttonWrapper, photoId, parent_comment_id = null){

    buttonWrapper.addEventListener('click', function (event){

                    if(event.target.classList.contains('btn')){
                        if(event.target.id === 'buttonResponse'){
                            let commentsFormResponse = createElement('form');
                            let inputResponse = createElement('input', ['form-control']);
                            inputResponse.type = 'text';
                            inputResponse.placeholder = 'Ответ';
                            inputResponse.name = 'Ответ';
                            let submitButtonResponse = createElement('button',
                                ['btn','btn-primary', 'btn-sm', 'btn-submit-wrapper']);
                            submitButtonResponse.type = 'submit';
                            submitButtonResponse.textContent = 'Ответить';
                            commentsFormResponse.append(inputResponse);
                            commentsFormResponse.append(submitButtonResponse);
                            let parentElement = buttonWrapper.parentNode;
                            parentElement.append(commentsFormResponse);
                            submitButtonResponse.addEventListener('click', function (event){
                                event.preventDefault();
                                let postDataResponse = {
                                    content: inputResponse.value,
                                    parent_id_comment: true,
                                    image_id: photoId,
                                    parent_id: buttonWrapper.parentNode.id
                                }
                                if(buttonWrapper.parentNode.className.includes("child-comment")){
                                    postDataResponse = {
                                        content: inputResponse.value,
                                        parent_id_comment: true,
                                        image_id: photoId,
                                        parent_id: buttonWrapper.parentNode.getAttribute('parent_comment_id')

                                    }

                                }


                                $.ajax({
                                    url: '/content/comment/post/',
                                    data: postDataResponse,
                                    method: 'POST',
                                    dataType: 'json',
                                    headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                                    success: function (responsePost){
                                        let childCommentsBlock = createElement('div', ['child-comments']);
                                        let commentBlock = buttonWrapper.parentNode.parentNode;
                                        childCommentsBlock.id = "child-comments" + responsePost.comment_parent_id;
                                        commentBlock.appendChild(childCommentsBlock);
                                        childCommentsBlock.setAttribute("parent_comment_id",
                                        postDataResponse.parent_id)

                                        $.ajax({
                                     url: '/profile/user/data/get/',
                                     dataType: 'json',
                                     method: 'GET',
                                     headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                                     success: function (response){
                                        let childCommentElement = createElement('div', ['child-comment']);
                                        childCommentElement.setAttribute('userid', response.id);
                                        childCommentElement.setAttribute('parent_comment_id',
                                            responsePost.comment_parent_id);
                                        childCommentElement.id = responsePost.comment_id;

                                        childCommentElement.innerHTML = '<span class="username">' +
                                            response.username  + '</span>: ' +
                                        postDataResponse.content;
                                        childCommentsBlock.appendChild(childCommentElement);
                                        let createdButtonWrapper = addButtonWrapper(childCommentElement, response.id);
                                        createActionButtonWrapper(createdButtonWrapper, photoId);
                                        parentElement.removeChild(commentsFormResponse);

                                 }
                                 })

                                    }
                                })
                                  })
                        }else if(event.target.id === 'buttonDelete'){
                            let parentElement = buttonWrapper.parentNode
                            let deleteData = {
                                comment_id: parentElement.id
                            }
                            $.ajax({
                                url: 'content/comment/delete/',
                                dataType: 'json',
                                data: deleteData,
                                method: 'POST',
                                headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                                success: function (response){
                                    console.log('Delete complited');
                                    parentElement.parentNode.removeChild(parentElement);
                                },
                                error: function (status, error){
                                    console.log('Вылет с Error');
                                    console.log(status);
                                }
                                }
                            )
                        }else if(event.target.id === "buttonEdit"){
                            let parentElement = buttonWrapper.parentNode;
                            let requestData = {
                                comment_id: parentElement.id
                            }
                            $.ajax({
                                url: '/content/comment/text/',
                                dataType: 'json',
                                method: 'POST',
                                data: requestData,
                                headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                                success: function(response){
                                    let commentElement = buttonWrapper.parentNode
                                    let commentChangeForm = createElement('form');
                                    let inputChange = createElement('input', ['form-control']);
                                    inputChange.type = 'text';
                                    inputChange.placeholder = 'Введите комментарий';
                                    inputChange.name = 'Комментарий';
                                    inputChange.value = response.commentContent;
                                    let submitButton = createElement('button',
                                        ['btn','btn-primary', 'btn-sm', 'btn-submit-wrapper']);
                                    submitButton.type = 'submit';
                                    submitButton.textContent = 'Применить изменения';
                                    commentChangeForm.appendChild(inputChange);
                                    commentChangeForm.appendChild(submitButton);
                                    commentElement.appendChild(commentChangeForm);
                                    submitButton.addEventListener('click', function (event){
                                        event.preventDefault();
                                        $.ajax({
                                            url: '/content/comment/edit/',
                                            dataType: 'json',
                                            method: 'POST',
                                            data: {'comment_id': parentElement.id, 'editText': inputChange.value},
                                            headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                                            success: function(response){
                                                parentElement.innerHTML = '<span class="username">' +
                                                    response.username + '</span>: ' + inputChange.value;
                                                parentElement.appendChild(buttonWrapper);
                                            }
                                        })

                            })
                                }

                            })

                        }

                    }
                })
}

function showComments(photoId, userId) {
    let commentsWrapper = document.getElementById('comments-' + photoId);
    let commentsBlock = createElement('div',['comments', 'wrapper']);
    commentsWrapper.appendChild(commentsBlock);
    commentsBlock.innerHTML = '';
    let commentsData;
    $.ajax({
        url: '/content/comment/get/',
        dataType: 'json',
        data: {'photoId': photoId},
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
        success: function (response){
            commentsData = response.data;
            let baseComments = commentsData.filter(comment => !comment.child_comment);
            let childComments = commentsData.filter(comment => comment.child_comment);
            /*Создание формы для создания комментария*/
            let commentsForm = createElement('form');
            let input = createElement('input', ['form-control']);
            input.type = 'text';
            input.name = 'Комменатрий';
            input.placeholder = 'Написать комментарий';


            let submitButton = createElement('button', ['btn','btn-primary', 'btn-sm', 'btn-submit-wrapper']);
            submitButton.type='submit';
            submitButton.textContent = 'Отправить';

            commentsForm.append(input);
            commentsForm.append(submitButton);



            baseComments.forEach(comment => {
                let commentElement = createElement('div', ['comment']);
                commentElement.id = comment.id;
                commentElement.setAttribute('userId', comment.user_id);
                commentElement.innerHTML = '<span class="username">' + comment.username + '</span>: ' + comment.content;
                commentsBlock.appendChild(commentElement);

                let childCommentsBlock = createElement('div', ['child-comments']);
                childCommentsBlock.id = "child-comments" + comment.id;
                commentsBlock.appendChild(childCommentsBlock);

                let childCommentsForParent = childComments.filter(childComment =>
                    childComment.parent_id === comment.id);
                let childCommentsForParentRender = childCommentsForParent.slice(0,2);
                childCommentsForParentRender.forEach(childComment => {
                    let childCommentElement = createElement('div', ['child-comment']);
                    childCommentElement.id = childComment.id;
                    childCommentElement.setAttribute('parent_comment_id', comment.id);
                    childCommentElement.innerHTML = '<span class="username">' + childComment.username + '</span>: ' +
                        childComment.content;
                    childCommentElement.setAttribute('userId', childComment.user_id);
                    let childButtonWrapper = addButtonWrapper(childCommentElement, userId, photoId);
                    createActionButtonWrapper(childButtonWrapper, photoId)
                    childCommentsBlock.appendChild(childCommentElement);
                });
                if (childCommentsForParent.length > 2) {
                    let showMoreButton = createElement('button', ['btn', 'btn-link']);
                    showMoreButton.textContent = 'Показать еще ' +
                        (childCommentsForParent.length-2) + ' комментариев';
                    showMoreButton.addEventListener('click', () => showAllChildComments(childComments,
                        childCommentsBlock, userId, photoId));
                    childCommentsBlock.appendChild(showMoreButton);
                }
                let buttonWrapper = addButtonWrapper(commentElement, userId, photoId);
                createActionButtonWrapper(buttonWrapper, photoId);

                })


            commentsWrapper.appendChild(commentsForm);
            submitButton.addEventListener('click', function (event){
                event.preventDefault();
                let inputData = {
                    image_id: photoId,
                    parent_id_comment: false,
                    content: input.value
                }
                if(inputData.content === ""){
                    input.placeholder = 'Комментарий не может быть пустым';
                    return 0;
                }

                $.ajax({
                    url: '/content/comment/post/',
                    data: inputData,
                    method: 'POST',
                    dataType: 'json',
                    headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                    success: function (responsePost){
                        let commentElement = createElement('div', ['comment']);
                        $.ajax({
                                url: '/profile/user/data/get/',
                                dataType: 'json',
                                method: 'GET',
                                headers: {'X-CSRFToken': csrftoken, 'X-SessionId': sessionid},
                                success: function (response){
                                    commentElement.id = responsePost.comment_id;
                                    commentElement.setAttribute('userId', response.id)
                                    commentElement.innerHTML = '<span class="username">' + response.username + '</span>: '
                                        + inputData.content;
                                    commentsBlock.appendChild(commentElement);
                                    let buttonWrapper = addButtonWrapper(commentElement, response.id, photoId);
                                    createActionButtonWrapper(buttonWrapper, photoId);

                                    }
                                }
                    )
                    }
                })



            })
            commentsWrapper.style.display = 'block';
}

        })
    }



function showAllChildComments(childComments, childCommentsBlock, userId, photoId) {
    childCommentsBlock.innerHTML = '';
    childComments.forEach(comment =>{
        let childCommentElement = createElement('div', ['child-comment'])
        childCommentElement.setAttribute('userId', comment.user_id);
        childCommentElement.setAttribute('id', comment.id);
        childCommentElement.innerHTML = '<span class="username">' + comment.username + '</span>: ' + comment.content;
        childCommentsBlock.appendChild(childCommentElement);
        let buttonWrapper = addButtonWrapper(childCommentElement, userId);
        createActionButtonWrapper(buttonWrapper, photoId);

    })
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
        //commentsButton.addEventListener('click', () => showComments(photo.id));
        commentsButton.addEventListener('click', function (){
            $.ajax({
                url: 'profile/user/data/get/',
                dataType: 'json',
                method: 'GET',
                success: function (response){
                    showComments(photo.id, response.id);
                }

            })
        })
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

const commentsData = [
    {
        id :1,
        username: 'user',
        content: 'Some Text',
        count_child_comments: 0,
        child_comment: false, //существуют ли дочерние комментарии если они существуют, то данные о первых двух
    }

    ]




export default generatePage;