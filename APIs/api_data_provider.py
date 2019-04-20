import abc


class API_data_provider(abc.ABC):
    @abc.abstractmethod
    def get_API_Data_json(isbn: str) -> str:
        """
        This method should be implemented by the subclass
        """