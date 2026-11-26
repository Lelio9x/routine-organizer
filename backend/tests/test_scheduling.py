import random
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.text import normalize_answer
from app.routine.binary_tree import BinaryTree
from app.routine.scheduling import compute_free_slots, find_conflict, format_minutes


@dataclass
class Item:
    start_minutes: int
    duration: int = 30
    title: str = "t"


def check_avl(node):
    """Valida ordenação, alturas e fator de balanceamento; devolve a altura."""
    if node is None:
        return 0
    left_h = check_avl(node.left)
    right_h = check_avl(node.right)
    if node.left is not None:
        assert node.left.time_key < node.time_key
    if node.right is not None:
        assert node.right.time_key > node.time_key
    assert abs(left_h - right_h) <= 1, "árvore desbalanceada"
    assert node.height == 1 + max(left_h, right_h), "altura desatualizada"
    return node.height


def build(items):
    tree = BinaryTree()
    for item in items:
        assert tree.insert(item.start_minutes, item)
    return tree


class BinaryTreeTests(unittest.TestCase):
    def test_in_order_is_sorted(self):
        keys = random.Random(1).sample(range(1440), 200)
        tree = build([Item(k) for k in keys])
        self.assertEqual([i.start_minutes for i in tree.in_order()], sorted(keys))

    def test_duplicate_key_rejected(self):
        tree = build([Item(480)])
        self.assertFalse(tree.insert(480, Item(480)))
        self.assertEqual(len(tree), 1)

    def test_sequential_insert_stays_balanced(self):
        # Na ABB simples isso viraria uma lista de altura 1000.
        tree = BinaryTree()
        for k in range(1000):
            tree.insert(k, k)
        check_avl(tree.root)
        self.assertLessEqual(tree.height(), 12)

    def test_deep_sequence_does_not_hit_recursion_limit(self):
        tree = BinaryTree()
        for k in range(5000):
            tree.insert(k, k)
        self.assertEqual(len(tree.in_order()), 5000)

    def test_remove_three_classic_cases(self):
        tree = build([Item(k) for k in (50, 30, 70, 20, 40, 60, 80)])
        self.assertTrue(tree.remove(20))   # folha
        self.assertTrue(tree.remove(30))   # um filho
        self.assertTrue(tree.remove(50))   # dois filhos (raiz)
        self.assertFalse(tree.remove(999))
        self.assertEqual([i.start_minutes for i in tree.in_order()], [40, 60, 70, 80])
        check_avl(tree.root)

    def test_predecessor_successor(self):
        tree = build([Item(k) for k in (100, 200, 300)])
        self.assertIsNone(tree.predecessor(100))
        self.assertEqual(tree.predecessor(250).start_minutes, 200)
        self.assertEqual(tree.predecessor(200).start_minutes, 100)
        self.assertEqual(tree.successor(150).start_minutes, 200)
        self.assertEqual(tree.successor(200).start_minutes, 300)
        self.assertIsNone(tree.successor(300))

    def test_randomized_against_reference_model(self):
        rng = random.Random(42)
        tree, model = BinaryTree(), {}
        for _ in range(6000):
            key = rng.randrange(0, 400)
            if rng.random() < 0.55:
                inserted = tree.insert(key, key)
                self.assertEqual(inserted, key not in model)
                model.setdefault(key, key)
            else:
                removed = tree.remove(key)
                self.assertEqual(removed, key in model)
                model.pop(key, None)

            if rng.random() < 0.1:
                check_avl(tree.root)
                self.assertEqual(len(tree), len(model))
                self.assertEqual(tree.in_order(), sorted(model))
                probe = rng.randrange(-5, 410)
                smaller = [k for k in model if k < probe]
                bigger = [k for k in model if k > probe]
                self.assertEqual(tree.predecessor(probe), max(smaller) if smaller else None)
                self.assertEqual(tree.successor(probe), min(bigger) if bigger else None)
                self.assertEqual(tree.search(probe), model.get(probe))


class ConflictTests(unittest.TestCase):
    def setUp(self):
        # 08:00-09:00, 10:00-10:30
        self.tree = build([Item(480, 60, "A"), Item(600, 30, "B")])

    def test_same_start(self):
        self.assertEqual(find_conflict(self.tree, 480, 5).title, "A")

    def test_overlaps_previous_task(self):
        self.assertEqual(find_conflict(self.tree, 510, 10).title, "A")

    def test_overlaps_next_task(self):
        self.assertEqual(find_conflict(self.tree, 570, 40).title, "B")

    def test_back_to_back_is_allowed(self):
        self.assertIsNone(find_conflict(self.tree, 540, 60))   # termina às 10:00
        self.assertIsNone(find_conflict(self.tree, 630, 30))   # começa às 10:30

    def test_free_gap_and_empty_tree(self):
        self.assertIsNone(find_conflict(self.tree, 700, 30))
        self.assertIsNone(find_conflict(BinaryTree(), 0, 1440))

    def test_matches_brute_force(self):
        rng = random.Random(7)
        items, tree = [], BinaryTree()
        for _ in range(400):
            start, dur = rng.randrange(0, 1400), rng.randrange(5, 90)
            if start + dur > 1440:
                continue
            brute = any(start < i.start_minutes + i.duration and i.start_minutes < start + dur for i in items)
            conflict = find_conflict(tree, start, dur)
            self.assertEqual(conflict is not None, brute, (start, dur))
            if conflict is None:
                item = Item(start, dur)
                items.append(item)
                tree.insert(start, item)


class FreeSlotTests(unittest.TestCase):
    def test_gaps_between_tasks(self):
        tasks = build([Item(480, 15), Item(495, 30), Item(570, 30), Item(1320, 30)]).in_order()
        self.assertEqual(
            compute_free_slots(tasks),
            [
                {"start_minutes": 525, "end_minutes": 570, "duration": 45},
                {"start_minutes": 600, "end_minutes": 1320, "duration": 720},
            ],
        )

    def test_no_slots_for_zero_one_or_adjacent_tasks(self):
        self.assertEqual(compute_free_slots([]), [])
        self.assertEqual(compute_free_slots([Item(480)]), [])
        self.assertEqual(compute_free_slots([Item(480, 30), Item(510, 30)]), [])

    def test_overlapping_legacy_data_does_not_invent_free_time(self):
        tasks = [Item(0, 100), Item(10, 10), Item(50, 10), Item(120, 10)]
        self.assertEqual(
            compute_free_slots(tasks),
            [{"start_minutes": 100, "end_minutes": 120, "duration": 20}],
        )


class TextTests(unittest.TestCase):
    def test_normalize_answer(self):
        self.assertEqual(normalize_answer("  Árvore   Binária "), "arvore binaria")
        self.assertEqual(normalize_answer("SETEMBRO"), "setembro")
        self.assertEqual(normalize_answer("4"), "4")

    def test_format_minutes(self):
        self.assertEqual(format_minutes(510), "08:30")
        self.assertEqual(format_minutes(0), "00:00")


if __name__ == "__main__":
    unittest.main()
