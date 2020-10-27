import decorator
from abc import ABC, abstractmethod
from typing import List, get_type_hints

class Component(ABC):
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def add(self, component):
        pass

    def remove(self, component):
        pass

    def is_composite(self)->bool:
        return False

    def operation(self)->str:
        pass


class Leaf(Component):
    def operation(self) -> str:
        return "Leaf"

class Composite(Component):
    def __init__(self)->None:
        self._children: List[Component] = []
    
    def add(self, component)->None:
        self._children.append(component)
        component.parent = self

    def remove(self, component)->None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self)->bool:
        return True
    
    def operation(self)->str:
        results = []
        for child in self._children:
            results.append(child.operation())
        return f"Branch({'+'.join(results)})"

def client_code(component)->None:
    print('Result: ', component.operation())

if __name__ == '__main__':
    
    simple = Leaf()
    print('starting for simple code')
    client_code(simple)
    print('ending for simple code')

    tree = Composite()
    branch1 = Composite()
    branch2 = Composite()

    branch1.add(Leaf())
    branch1.add(Leaf())

    branch2.add(Leaf())

    tree.add(branch1)
    tree.add(branch2)

    client_code(tree)
    
