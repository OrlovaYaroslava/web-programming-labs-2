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
                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitle.innerText = films[i].title == films[i].title_ru ? '' : films[i].title;
                tdTitleRus.innerText = films[i].title_ru;
                tdYear.innerText = films[i].year;

                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                let deleteButton = document.createElement('button');
                deleteButton.innerText = 'Удалить';
                deleteButton.onclick = function() {
                    deleteFilm(i, films[i].title_ru);
                };

                tdActions.append(editButton);
                tdActions.append(deleteButton);

                tr.append(tdTitle);
                tr.append(tdTitleRus);
                tr.append(tdYear);
                tr.append(tdActions);

                tbody.append(tr);
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }

    fetch(`/lab7/rest-api/films/${id + 1}`, {
        method: 'DELETE'
    })
    .then(function() {
        fillFilmList();
    })
    .catch(error => console.error('Ошибка:', error));
}

document.getElementById('add-film-button').addEventListener('click', function() {
    // Логика для добавления нового фильма
    alert('Добавление нового фильма');
});