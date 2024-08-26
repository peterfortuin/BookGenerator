from dependency_injector import containers, providers

from services.book_service import BookService


class BookGeneratorContainer(containers.DeclarativeContainer):
    book_service = providers.Singleton(BookService)


book_generator_container = BookGeneratorContainer()
