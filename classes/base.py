from abc import ABC, abstractmethod


class BaseAPIClass(ABC):
    
    @abstractmethod
    def make_request():
        pass



class BaseSaveClass(ABC):
    
    @abstractmethod
    def add():
        pass


    @abstractmethod
    def delete():
        pass


