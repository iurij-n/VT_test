'''
Класс TreeStore для работы со структурами данных вида:
items = [
        {'id': 1, 'parentId': 0},
        {'id': 2, 'parentId': 0},
        {'id': 3, 'parentId': 1},
        {'id': 4, 'parentId': 1},
        {'id': 5, 'parentId': 2},
        {'id': 6, 'parentId': 4},
        {'id': 7, 'parentId': 5}
    ]

Методы класса:
get_all(self) - Возвращает изначальный массив элементов.

get_item(self, id) - Принимает id элемента и возвращает объект
    элемента c 'id' = id.

get_children(self, id) - Принимает id элемента и возвращает массив элементов,
    являющихся дочерними для того элемента, чей id получен в аргументе. Если у
    элемента нет дочерних, то возвращается пустой список.

get_all_parents(self, id) - Принимает id элемента и возвращает массив из
    цепочки родительских элементов, начиная от самого элемента, чей id был
    передан в аргументе и до корневого элемента, т.е. должен получиться путь
    элемента наверх дерева через цепочку родителей к корню дерева. Список
    родительских элементов - parents_list, составляется с помощью рекурсивно
    вызываемой функции get_self_parent().

get_structure(self) - Преобразует массив 'плоских' объектов в массив
    объектов с вложенными дочерними элементами.
'''
from copy import deepcopy


class TreeStore:
    def __init__(self, items: list) -> None:
        '''
        В конструкторе переданный список элементов обходится в цикле.
        При этом элементы списка хэшируются в словарь hashed_items. В качестве
        ключа используется значение ключа 'id' элемента, а значением становится
        словарь с двумя ключами:
           'item' - сам элемент;
           'childs' - список потомков элемента.
        После этого к элементу можно обращаться напрямую по id и методы класса
        реализуются без поиска элементов в массиве.
        '''
        self.items = items
        self.hashed_items = {}
        self.childs = {}

        for item in self.items:
            self.hashed_items[item['id']] = {}
            self.hashed_items[item['id']]['item'] = item
            self.hashed_items[item['id']]['childs'] = []
            if item['parentId'] != 0:
                self.hashed_items[item['parentId']]['childs'].append(
                    item['id'])

    def get_all(self) -> list:
        '''
        Возвращает изначальный массив элементов.
        '''
        return self.items

    def get_item(self, id: int) -> dict:
        '''
        Принимает id элемента и возвращает объект элемента c 'id' = id.
        '''
        return self.hashed_items[id]['item']

    def get_children(self, id: int) -> list:
        '''
        Принимает id элемента и возвращает массив элементов, являющихся
        дочерними для того элемента, чей id получен в аргументе.
        Если у элемента нет дочерних, то возвращается пустой список.
        '''
        return [self.hashed_items[id]['item'] for id in
                self.hashed_items[id]['childs']]

    def get_all_parents(self, id: int) -> list:
        '''
        Принимает id элемента и возвращает массив из цепочки родительских
        элементов, начиная от самого элемента, чей id был передан в аргументе
        и до корневого элемента, т.е. должен получиться путь элемента наверх
        дерева через цепочку родителей к корню дерева.
        Список родительских элементов - parents_list, составляется с помощью
        рекурсивно вызываемой функции get_self_parent().
        '''
        parents_list = []

        def get_self_parent(self, id, parents_list):
            if self.hashed_items[id]['item']['parentId'] == 0:
                return
            parents_list.append(self.hashed_items[
                    self.hashed_items[id]['item']['parentId']]['item'])
            get_self_parent(self,
                            self.hashed_items[id]['item']['parentId'],
                            parents_list)

        get_self_parent(self, id, parents_list)

        return parents_list

    def get_structure(self) -> list:
        '''
        Преобразует массив 'плоских' объектов в массив
        объектов с вложенными дочерними элементами.
        '''
        temp_data = deepcopy(self.get_all())

        for item in temp_data[::-1]:
            if self.get_children(item['id']) != []:
                if item.get('children') is None:
                    item['children'] = self.get_children(item['id'])

        return [item for item in temp_data
                if item.get('children') is not None]


if __name__ == '__main__':
    items = [
        {'id': 1, 'parentId': 0},
        {'id': 2, 'parentId': 0},
        {'id': 3, 'parentId': 1},
        {'id': 4, 'parentId': 1},
        {'id': 5, 'parentId': 2},
        {'id': 6, 'parentId': 4},
        {'id': 7, 'parentId': 5}
    ]

    print(TreeStore(items).get_structure())
