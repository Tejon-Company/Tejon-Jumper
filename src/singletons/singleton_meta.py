class SingletonMeta(type):
    """
    Metaclase para implementar el patrón Singleton. Esta metaclase
    asegura que una clase que la utilice solo pueda tener una única
    instancia.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
