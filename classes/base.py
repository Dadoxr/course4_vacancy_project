from abc import ABC, abstractmethod


class BaseAPIClass(ABC):
    
    @abstractmethod
    def make_request():
        pass

    @abstractmethod
    def get_data():
        pass



class BaseJSONClass(ABC):
    
    @abstractmethod
    def add_vacancy():
        pass


    @abstractmethod
    def delete_vacancy():
        pass


