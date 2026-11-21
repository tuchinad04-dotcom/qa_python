import pytest
from main import BooksCollector


class TestBooksCollector:

    # Проверяем добавление книги, ограничения названия и отсутствие дубликатов
    @pytest.mark.parametrize('name, expected', [
        ('Гарри Поттер', True),
        ('Война и мир', True),
        ('А' * 40, True),
        ('', False),
        ('А' * 41, False)
    ])
    def test_add_new_book(self, name, expected):
        collector = BooksCollector()

        collector.add_new_book(name)

        if expected:
            collector.set_book_genre(name, 'Фантастика')
            collector.add_new_book(name)
            assert collector.get_books_genre() == {
                name: 'Фантастика'
            }
        else:
            assert collector.get_books_genre() == {}

    # Проверяем установку жанра книги
    @pytest.mark.parametrize('name, genre, expected', [
        ('Гарри Поттер', 'Фантастика', 'Фантастика'),
        ('Гарри Поттер', 'Роман', ''),
        ('Несуществующая книга', 'Фантастика', '')
    ])
    def test_set_book_genre(self, name, genre, expected):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')

        collector.set_book_genre(name, genre)

        assert collector.books_genre == {
            'Гарри Поттер': expected
        }

    # Проверяем получение жанра книги
    @pytest.mark.parametrize('name, expected', [
        ('Гарри Поттер', 'Фантастика'),
        ('Несуществующая книга', None)
    ])
    def test_get_book_genre(self, name, expected):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')

        assert collector.get_book_genre(name) == expected

    # Проверяем получение книг с определённым жанром
    @pytest.mark.parametrize('genre, expected', [
        ('Фантастика', ['Гарри Поттер', 'Властелин колец']),
        ('Ужасы', ['Оно']),
        ('Роман', [])
    ])
    def test_get_books_with_specific_genre(self, genre, expected):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Властелин колец')
        collector.add_new_book('Оно')

        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        collector.set_book_genre('Властелин колец', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')

        assert collector.get_books_with_specific_genre(genre) == expected

    # Проверяем получение словаря книг и жанров
    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')

        assert collector.get_books_genre() == {
            'Гарри Поттер': 'Фантастика'
        }

    # Проверяем, что книги с возрастным рейтингом не попадают в список детских
    def test_get_books_for_children(self):
        collector = BooksCollector()
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

    # Проверяем добавление книги в избранное и защиту от дубликатов
    @pytest.mark.parametrize('name, expected', [
        ('Гарри Поттер', ['Гарри Поттер']),
        ('Несуществующая книга', [])
    ])
    def test_add_book_in_favorites(self, name, expected):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')

        collector.add_book_in_favorites(name)
        collector.add_book_in_favorites(name)

        assert collector.favorites == expected

    # Проверяем удаление книги из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')

        collector.delete_book_from_favorites('Гарри Поттер')

        assert collector.favorites == []

    # Проверяем получение списка избранных книг
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Властелин колец')

        collector.add_book_in_favorites('Гарри Поттер')
        collector.add_book_in_favorites('Властелин колец')

        assert collector.get_list_of_favorites_books() == [
            'Гарри Поттер',
            'Властелин колец'
        ]
