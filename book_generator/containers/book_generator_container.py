from dependency_injector import containers, providers


class BookGeneratorContainer(containers.DeclarativeContainer):
    book_service = providers.Singleton("services.book_service.BookService")


book_generator_container = BookGeneratorContainer()
