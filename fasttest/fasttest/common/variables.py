import copy

class Variables(object):

    def __getattr__(self, name: str) -> object:
        try:
            value = self.__getattribute__(name)
            return value
        except:
            return None
    
    def __getitem__(self, name: str) -> object:
        try:
            value = self.__getattribute__(name)
            return value
        except:
            return None

    def __setattr__(self, key: str, value: object) -> None:
        object.__setattr__(self, key, value)

    def __setitem__(self, key: str, value: object) -> None:
        object.__setattr__(self, key, value)

    
    def __deepcopy__(self, memo):
        cls = self.__class__
        new_obj = cls.__new__(cls)
        memo[id(self)] = new_obj
        for k in self.__dict__.keys():
            setattr(new_obj, k, copy.deepcopy(self[k]))
        return new_obj