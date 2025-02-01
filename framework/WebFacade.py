import framework
from importlib import import_module
from stringcase import lowercase, pascalcase

class WebFacade(framework.WebDriver):
    """
    Facade for get all or specific method for used with webdriver. 
    Neither class is instanced.

    Attributes:
        _actions: Actions class
        _waits: Waits class
        _validate: Validate class
        _change: Change class
    """

    _actions:framework.Actions = None
    _waits:framework.Waits = None
    _validate:framework.Validate = None
    _change:framework.Change = None

    @classmethod
    def initialize_instaces(self):
        """ 
        Initialize and save instances of all classes defined in the framework module. 
        """
        for attribute_name in self.__dict__:
            class_module_name = pascalcase(attribute_name.replace("_", ""))
            if class_module_name in framework.__all__:
                module = import_module("framework.%s" %(class_module_name))
                instance = getattr(module, class_module_name)()
                setattr(self, attribute_name, instance)

    @classmethod
    def get_instance(self, class_name:str)->framework.Waits | framework.Actions | framework.Validate | framework.Change:
        """ 
        Get an instance of the specified class. 

        Note:
            This method doesn't change the attribute, only init and return.
        Parameters: 
            class_name (str):
            The name of the class to retrieve. 
        Returns: 
            instance: 
            An instance of the specified class.
        Raises: 
            AttributeError:
              If not found. 
        """
        attr_name = f"_{lowercase(class_name)}"
        if(attr_name in self.__dict__):
            return self.__initialize_class_instance(class_name)
        raise AttributeError(f"Class not exist {attr_name}")

    @classmethod
    def __initialize_class_instance(self, class_name:str):
        """ 
        Get an instance of the specified class.

        Note:
            This method is private, please not used.
        Parameters: 
            class_name (str):
            The name of the class to initialize. 
        Returns: 
            instance: 
            The initialized class instance.
        Raises:
            ImportError: 
            If the module is not found.
        """
        class_module_name = pascalcase(class_name)
        if class_module_name in framework.__all__:
            module = import_module("framework.%s" %(class_module_name))
            return getattr(module, class_module_name)()
        else:
            raise ImportError("Module %s not found in framework." %class_name)