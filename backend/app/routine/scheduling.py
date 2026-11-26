"""Regras de agenda que dependem só da árvore (sem banco, sem FastAPI)."""
from typing import Any, Optional

from app.routine.binary_tree import BinaryTree

MINUTES_IN_DAY = 1440


def format_minutes(total: int) -> str:
    return f"{total // 60:02d}:{total % 60:02d}"


def find_conflict(tree: BinaryTree, start_minutes: int, duration: int) -> Optional[Any]:
    """Devolve a tarefa que se sobrepõe a [start, start + duration), ou None.

    Como as tarefas já agendadas não se sobrepõem entre si, basta olhar
    três nós: o que começa no mesmo horário, o vizinho anterior (que pode
    terminar depois do início da nova tarefa) e o vizinho seguinte (que pode
    começar antes do fim da nova tarefa).
    """
    same_start = tree.search(start_minutes)
    if same_start is not None:
        return same_start

    before = tree.predecessor(start_minutes)
    if before is not None and before.start_minutes + before.duration > start_minutes:
        return before

    after = tree.successor(start_minutes)
    if after is not None and after.start_minutes < start_minutes + duration:
        return after

    return None


def compute_free_slots(ordered_tasks: list[Any]) -> list[dict[str, int]]:
    """Intervalos livres entre o fim de uma atividade e o início da próxima.

    Recebe as tarefas já em ordem cronológica (percurso in-order da árvore).
    """
    slots: list[dict[str, int]] = []
    latest_end: Optional[int] = None

    for task in ordered_tasks:
        if latest_end is not None and task.start_minutes > latest_end:
            slots.append(
                {
                    "start_minutes": latest_end,
                    "end_minutes": task.start_minutes,
                    "duration": task.start_minutes - latest_end,
                }
            )
        task_end = task.start_minutes + task.duration
        latest_end = task_end if latest_end is None else max(latest_end, task_end)

    return slots
