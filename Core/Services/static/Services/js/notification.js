const notificationContainer = document.getElementById('notificationContainer');
const notificationContent = document.getElementById('notificationContent');
let socket = new WebSocket("ws://127.0.0.1:8000/ws/Notification/");
// Функция для добавления уведомления в контейнер
function addNotification(message) {
    let notification = document.createElement('div');
    notification.classList.add('notification');
    notification.textContent = message;
    console.log(message);
    notificationContent.appendChild(notification);
    return notification
}

socket.onmessage = function(event) {
    let message = JSON.parse(event.data).notification;
    let notification = addNotification(message);
    setTimeout(function (){
        notification.parentNode.removeChild(notification);
    }, 2000);
};

