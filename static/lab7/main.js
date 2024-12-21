document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});

// Функция для заполнения списка фильмов на странице
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';  // Очистка таблицы

            let fragment = document.createDocumentFragment();  // Создание фрагмента для оптимизации DOM

            films.forEach(film => {
                let tr = document.createElement('tr');
                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitleRus.innerText = film.title_ru;
                tdTitle.innerHTML = film.title ? `<i>(${film.title})</i>` : ''; // Проверка наличия оригинального названия
                tdYear.innerText = film.year;

                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                editButton.onclick = function() {
                    editFilm(film.id); // Используем настоящий ID
                };
                let deleteButton = document.createElement('button');
                deleteButton.innerText = 'Удалить';
                deleteButton.onclick = function() {
                    deleteFilm(film.id, film.title_ru); // Используем настоящий ID
                };

                tdActions.append(editButton);
                tdActions.append(deleteButton);

                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdActions);

                fragment.append(tr);  // Добавление строки в фрагмент
            });

            tbody.append(fragment);  // Добавление фрагмента в DOM
        })
        .catch(error => console.error('Ошибка при загрузке фильмов:', error));
}

// Функция для отправки данных фильма (добавление или редактирование)
function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: parseInt(document.getElementById('year').value, 10),
        description: document.getElementById('description').value
    };

    const url = id ? `/lab7/rest-api/films/${id}` : '/lab7/rest-api/films/';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(error => {
                throw new Error(error.error || error.description);
            });
        }
        return response.json();
    })
    .then(data => {
        fillFilmList();
        hideModal();
        showErrorMessage('Фильм успешно добавлен/отредактирован!', 'success');
    })
    .catch(error => {
        showErrorMessage(error.message, 'error');
    });
}

// Функция для отображения сообщений об ошибках или успехе
function showErrorMessage(message, type) {
    const errorMessage = document.getElementById('error-message');
    errorMessage.innerText = message;
    errorMessage.style.display = 'block';
    errorMessage.style.color = type === 'error' ? 'red' : 'green';
    
    // Скрыть сообщение через 5 секунд
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

// Функция для удаления фильма
function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }

    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(error => {
                throw new Error(error.error || "Ошибка при удалении фильма.");
            });
        }
        fillFilmList();
        showErrorMessage(`Фильм "${title}" успешно удалён!`, 'success');
    })
    .catch(error => {
        console.error('Ошибка:', error.message);
        alert(`Ошибка: ${error.message}`);
    });
}

// Функция для редактирования фильма
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.error || "Ошибка при получении данных фильма.");
                });
            }
            return response.json();
        })
        .then(film => {
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title || '';
            document.getElementById('title-ru').value = film.title_ru || '';
            document.getElementById('year').value = film.year || '';
            document.getElementById('description').value = film.description || '';
            showModal();
        })
        .catch(error => {
            console.error('Ошибка:', error.message);
            alert(`Ошибка: ${error.message}`);
        });
}

// Показывает модальное окно для добавления или редактирования фильма
function showModal() {
    document.getElementById('add-film-modal').style.display = 'block';
    document.getElementById('error-message').innerText = ''; // Очищаем сообщение об ошибке
}

// Скрывает модальное окно
function hideModal() {
    document.getElementById('add-film-modal').style.display = 'none';
    document.getElementById('error-message').style.display = 'none'; // Скрываем ошибки при закрытии
}

// Функция для открытия модального окна с пустыми полями (для добавления нового фильма)
function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal(); // Показываем модальное окно
}
