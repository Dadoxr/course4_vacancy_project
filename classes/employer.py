class Employer:

    employers_list = []
    
    def __init__(self, id: str, name: str, link: str, description: str) -> None:
        self.id = int(id)
        self.name = str(name) or "Нет названия"
        self.link = str(link) or "Нет ссылки"
        self.description = str(description) or "Нет описания"
        self.employers_list.append(self)
    
    def __repr__(self) -> str:
        return '%s(id=%s, name=%s, link=%s, description=%s)' % (
            self.__class__.__name__, self.id, self.name, self.link, self.description
        )