class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def __init__(self):
        self.root = None

    def _height(self, node):
        return 0 if node is None else node.height

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rebalance(self, node):
        self._update_height(node)
        balance = self._balance_factor(node)
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node
        return self._rebalance(node)

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)
        return self._rebalance(node)

    def search(self, value):
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            if value < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def inorder(self):
        result = []

        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node.value)
                visit(node.right)

        visit(self.root)
        return result

    def visualize(self):
        lines = []

        def visit(node, depth, label):
            if node is None:
                lines.append(f"{'    ' * depth}{label}: ∅")
                return
            lines.append(
                f"{'    ' * depth}{label}: {node.value} "
                f"[h={node.height}, b={self._balance_factor(node)}]"
            )
            if node.left is not None or node.right is not None:
                visit(node.left, depth + 1, "L")
                visit(node.right, depth + 1, "R")

        visit(self.root, 0, "root")
        return "\n".join(lines)


# Объяснение решения
# AVL — сбалансированное бинарное дерево поиска целых чисел.
# Все ключи слева строго меньше ключа узла, справа — строго больше.
# Повторная вставка ничего не меняет; удаление отсутствующего ключа тоже.
# insert и delete возвращают None. search возвращает True или False.
# inorder возвращает новый отсортированный список, visualize — строковую
# схему: L/R — левый/правый ребёнок, ∅ — пустое поддерево, h — высота,
# b — баланс. Схема и обход не изменяют дерево. Поля узлов открыты для
# разбора примеров; ручное изменение ссылок или высот нарушает гарантии AVL.
#
# Высота пустого поддерева равна 0, листа — 1. В каждом узле храним height,
# поэтому баланс b = height(left) - height(right) вычисляется за O(1).
# У AVL для каждого узла b принадлежит {-1, 0, 1}.
# Вставка сначала спускается как в обычном BST и создаёт лист.
# На обратном пути обновляем высоты и вызываем _rebalance:
#
# Условие                   | Случай | Повороты
# --------------------------|--------|------------------------------------
# b > 1, b(left) >= 0        | LL     | вправо вокруг узла
# b > 1, b(left) < 0         | LR     | влево вокруг left, вправо вокруг узла
# b < -1, b(right) <= 0      | RR     | влево вокруг узла
# b < -1, b(right) > 0       | RL     | вправо вокруг right, влево вокруг узла
#
# Удаление: лист заменяем на None, узел с одним ребёнком — на ребёнка.
# При двух детях берём минимальный ключ правого поддерева (successor),
# записываем его в удаляемый узел и удаляем прежний узел successor справа.
# Затем балансируем ВСЕ узлы обратного пути, включая корень: после удаления
# высота может уменьшаться несколько раз. Баланс тяжёлого ребёнка может
# равняться 0; тогда нужен одиночный поворот, как указано в таблице.
# Каждый рекурсивный метод возвращает новый корень своего поддерева,
# поэтому родитель и self.root сохраняют правильные ссылки после поворота.
# Поиск только сравнивает ключи и движется по одной ветви без рекурсии.
#
# Почему все работает правильно
# Вставка идёт в единственное поддерево, допускающее ключ по правилам BST.
# При удалении successor больше всех ключей слева и не больше остальных
# справа. После удаления его старого узла строгий порядок восстанавливается.
# Правый поворот сохраняет порядок A < x < B < y < C:
#
#          y                  x
#         / \                / \
#        x   C      ->      A   y
#       / \                    / \
#      A   B                  B   C
#
# Левый поворот симметричен. Важный шаг: среднее поддерево B переносится,
# а не теряется. Высоты обновляются сначала у прежнего, затем у нового корня.
# На обратном пути дети уже являются AVL. Изменение высоты ребёнка не больше
# единицы, поэтому нарушенный баланс равен 2 или -2. Указанные одиночные
# и двойные повороты возвращают |b| <= 1, сохраняя BST. По индукции после
# завершения операции всё дерево снова AVL. Поиск может отбросить вторую
# ветвь благодаря строгому порядку, значит, не пропустит существующий ключ.
#
# Оценка сложности
# n — число ключей, h — высота. Для минимального числа узлов высоты h:
# M(h) = 1 + M(h-1) + M(h-2), M(0)=0, M(1)=1. Рост экспоненциальный,
# следовательно, h = O(log(n + 1)). Сравнения целых считаем O(1).
# insert, delete, search: O(log(n + 1)) времени (при n=0 — O(1)).
# Поворот и обновление высоты: O(1). Удаление с поиском successor проходит
# лишь O(h) узлов; балансировка на каждом уровне тоже стоит O(1).
# insert/delete: O(log(n + 1)) дополнительной памяти стека; search: O(1).
# Дерево целиком занимает O(n); создание пустого AVL — O(1).
# Построение из n ключей: O(n log(n + 1)) времени, O(n) памяти.
# inorder: O(n) времени, O(h) стека плюс O(n) памяти результата.
# visualize: O(S) времени и памяти, где S — длина схемы, включая отступы.
# При коротких записях ключей S = O(n * log(n + 1)); пустая схема — O(1).
# Для больших чисел дополнительно учитывается стоимость сравнения и печати.
#
# Визуализация работы алгоритма
# Последовательно вставляем [30, 10, 20, 40, 50, 25].
# Шаги 1–2: корень 30; после insert(10) у него левый ребёнок 10.
# Шаг 3: insert(20) идёт 30 -> 10 -> вправо. Получаем случай LR:
#
#       30              30              20
#      /               /               /  \
#     10      ->      20      ->      10    30
#       \            /
#        20         10
#          левый у 10       правый у 30
#
# Шаг 4: insert(40) добавляет правого ребёнка к 30; корень 20, b=-1.
# Шаг 5: insert(50) нарушает баланс 30 (RR). Левый поворот у 30:
#
#       20                 20
#      /  \               /  \
#     10   30     ->     10    40
#            \               /  \
#             40            30   50
#               \
#                50
#
# Шаг 6: insert(25) идёт 20 -> 40 -> 30 -> влево. Корень 20 получает
# b=-2, а его правый ребёнок 40 — b=1. Это RL:
#
#       20                 20                   30
#      /  \               /  \                /    \
#     10   40     ->     10    30      ->      20     40
#         /  \               /  \           /  \      \
#        30   50            25   40        10   25      50
#       /                          \
#      25                           50
#          правый у 40          левый у 20
#
# Теперь delete(30): у корня два ребёнка, successor = 40. Копируем 40
# в корень, затем старый узел 40 справа заменяем его ребёнком 50:
#
#          40
#         /  \
#        20   50       h(root)=3, b(root)=1; повороты не нужны.
#       /  \
#      10   25
#
# Затем delete(50): у корня b=2, у левого ребёнка b=0. Правый поворот:
#
#          40                  20
#         /                   /  \
#        20        ->        10   40
#       /  \                     /
#      10   25                  25
#
# В итоге search(25): 20 -> вправо к 40 -> влево к 25 -> True.
# search(35): 20 -> 40 -> 25 -> вправо к None -> False.
# inorder() возвращает [10, 20, 25, 40]. В visualize() последняя схема:
# root: 20 [h=3, b=-1]
#     L: 10 [h=1, b=0]
#     R: 40 [h=2, b=1]
#         L: 25 [h=1, b=0]
#         R: ∅
#
# Запуск из homework_5: python3 -m AVL.avl
# Тесты: python3 -m pytest -q AVL/test_avl.py


if __name__ == "__main__":
    tree = AVL()
    for value in [30, 10, 20, 40, 50, 25]:
        tree.insert(value)
        print(f"\ninsert({value}):\n{tree.visualize()}")
    for value in [30, 50]:
        tree.delete(value)
        print(f"\ndelete({value}):\n{tree.visualize()}")
    print("\nsearch(25):", tree.search(25))
    print("search(35):", tree.search(35))
    print("inorder:", tree.inorder())
