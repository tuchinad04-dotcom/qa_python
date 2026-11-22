
import pytest


class TestBooksCollector:

    # Проверяем добавление книг, ограничение длины названия и дубликаты
    @pytest.mark.parametrize('name, expected_books', [
        ('Гарри Поттер', {'Гарри Поттер': ''}),
        ('Война и мир', {'Война и мир': ''}),
        ('А' * 40, {'А' * 40: ''}),
        ('', {}),
        ('А' * 41, {})
    ])
    def test_add_new_book(self, collector, name, expected_books):
        collector.add_new_book(name)
        collector.add_new_book(name)

        assert collector.get_books_genre() == expected_books

    # Проверяем установку жанра книги
    @pytest.mark.parametrize('name, genre, expected_genre', [
        ('Гарри Поттер', 'Фантастика', 'Фантастика'),
        ('Гарри Поттер', 'Роман', ''),
        ('Несуществующая книга', 'Фантастика', '')
    ])
    def test_set_book_genre(self, collector, name, genre, expected_genre):
        collector.add_new_book('Гарри Поттер')

        collector.set_book_genre(name, genre)

        assert collector.books_genre['Гарри Поттер'] == expected_genre

    # Проверяем получение жанра книги
    @pytest.mark.parametrize('name, expected', [
        ('Гарри Поттер', 'Фантастика'),
        ('Несуществующая книга', None)
    ])
    def test_get_book_genre(self, collector, name, expected):
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')

        assert collector.get_book_genre(name) == expected

    # Проверяем получение книг с определённым жанром
    @pytest.mark.parametrize('genre, expected', [
        ('Фантастика', ['Гарри Поттер', 'Властелин колец']),
        ('Ужасы', ['Оно']),
        ('Роман', [])
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected):
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Властелин колец')
        collector.add_new_book('Оно')

        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        collector.set_book_genre('Властелин колец', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')

        assert collector.get_books_with_specific_genre(genre) == expected

    # Проверяем получение словаря книг и жанров
    def test_get_books_genre(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')

        assert collector.get_books_genre() == {
            'Гарри Поттер': 'Фантастика'
        }

    # Проверяем, что книги с возрастным рейтингом не попадают в список детских
    def test_get_books_for_children(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Оно')
        collector.add_new_book('Мадагаскар')

        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Мадагаскар', 'Мультфильмы')

        assert collector.get_books_for_children() == [
            'Гарри Поттер',
            'Мадагаскар'
        ]

    # Проверяем добавление книг в избранное и защиту от дубликатов
    @pytest.mark.parametrize('name, expected', [
        ('Гарри Поттер', ['Гарри Поттер']),
        ('Несуществующая книга', [])
    ])
    def test_add_book_in_favorites(self, collector, name, expected):
        collector.add_new_book('Гарри Поттер')

        collector.add_book_in_favorites(name)
        collector.add_book_in_favorites(name)

        assert collector.favorites == expected

    # Проверяем удаление книги из избранного
    @pytest.mark.parametrize('name, expected', [
        ('Гарри Поттер', []),
        ('Несуществующая книга', ['Гарри Поттер'])
    ])
    def test_delete_book_from_favorites(self, collector, name, expected):
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')

        collector.delete_book_from_favorites(name)

        assert collector.favorites == expected

    # Проверяем получение списка избранных книг
    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Властелин колец')

        collector.add_book_in_favorites('Гарри Поттер')
        collector.add_book_in_favorites('Властелин колец')

        assert collector.get_list_of_favorites_books() == [
            'Гарри Поттер',
            'Властелин колец'
        ]
