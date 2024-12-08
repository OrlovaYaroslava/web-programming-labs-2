document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});

function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitleRus.innerText = films[i].title_ru;
                tdTitle.innerHTML = films[i].title ? `<i>(${films[i].title})</i>` : '';
                tdYear.innerText = films[i].year;

                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                editButton.onclick = function() {
                    editFilm(i + 1); // Учитываем ID с смещением 1
                };
                let deleteButton = document.createElement('button');
                deleteButton.innerText = 'Удалить';
                deleteButton.onclick = function() {
                    deleteFilm(i + 1, films[i].title_ru); // Учитываем ID с смещением 1
                };

                tdActions.append(editButton);
                tdActions.append(deleteButton);

                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdActions);

                tbody.append(tr);
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

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
    })
    .catch(error => {
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerText = error.message;
        errorMessage.style.display = 'block';
    });
}

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
    })
    .catch(error => {
        console.error('Ошибка:', error.message);
        alert(`Ошибка: ${error.message}`);
    });
}

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

function showModal() {
    document.getElementById('add-film-modal').style.display = 'block'; // Показываем модальное окно
    document.getElementById('error-message').innerText = ''; // Очищаем сообщение об ошибке
}

function hideModal() {
    document.getElementById('add-film-modal').style.display = 'none';
    document.getElementById('error-message').style.display = 'none'; // Скрываем ошибки при закрытии
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal(); // Показываем модальное окно
}
