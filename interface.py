from data import AppData


class AppInterface:
    def getData(self) -> AppData:
        raise NotImplementedError()
