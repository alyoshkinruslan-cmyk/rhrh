"""Модуль работы с SQLite-БД для приложения ToDo."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent / "todo.db"


def get_connection() -> sqlite3.Connection:
    """Открывает подключение к SQLite с поддержкой row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Создаёт таблицу tasks при первом запуске."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                priority    TEXT    NOT NULL DEFAULT 'normal',
                done        INTEGER NOT NULL DEFAULT 0,
                created_at  TEXT    NOT NULL,
                done_at     TEXT
            )
            """
        )


def add_task(title: str, priority: str = "normal") -> int:
    """Добавляет задачу и возвращает её id."""
    title = title.strip()
    if not title:
        raise ValueError("Заголовок задачи не может быть пустым")
    if priority not in {"low", "normal", "high"}:
        raise ValueError(f"Недопустимый приоритет: {priority}")
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, priority, created_at) VALUES (?, ?, ?)",
            (title, priority, datetime.now().isoformat(timespec="seconds")),
        )
        return cursor.lastrowid


def list_tasks(
    show_done: bool = True, priority: Optional[str] = None
) -> list[sqlite3.Row]:
    """Возвращает список задач (с фильтрами)."""
    query = "SELECT * FROM tasks WHERE 1=1"
    params: list = []
    if not show_done:
        query += " AND done = 0"
    if priority and priority != "all":
        query += " AND priority = ?"
        params.append(priority)
    query += " ORDER BY done ASC, "
    query += "CASE priority WHEN 'high' THEN 0 WHEN 'normal' THEN 1 ELSE 2 END, "
    query += "id DESC"
    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def toggle_task(task_id: int) -> None:
    """Переключает статус выполнения задачи."""
    with get_connection() as conn:
        row = conn.execute("SELECT done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            raise KeyError(f"Задача {task_id} не найдена")
        new_done = 0 if row["done"] else 1
        done_at = datetime.now().isoformat(timespec="seconds") if new_done else None
        conn.execute(
            "UPDATE tasks SET done = ?, done_at = ? WHERE id = ?",
            (new_done, done_at, task_id),
        )


def update_task(
    task_id: int,
    title: Optional[str] = None,
    priority: Optional[str] = None,
) -> None:
    """Обновляет заголовок и/или приоритет задачи."""
    fields = []
    params: list = []
    if title is not None:
        title = title.strip()
        if not title:
            raise ValueError("Заголовок задачи не может быть пустым")
        fields.append("title = ?")
        params.append(title)
    if priority is not None:
        if priority not in {"low", "normal", "high"}:
            raise ValueError(f"Недопустимый приоритет: {priority}")
        fields.append("priority = ?")
        params.append(priority)
    if not fields:
        return
    params.append(task_id)
    with get_connection() as conn:
        conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", params)


def delete_task(task_id: int) -> None:
    """Удаляет задачу по id."""
    with get_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))


def clear_done() -> int:
    """Удаляет все выполненные задачи. Возвращает количество удалённых."""
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE done = 1")
        return cursor.rowcount


def stats() -> dict:
    """Возвращает агрегированную статистику по задачам."""
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        done = conn.execute("SELECT COUNT(*) FROM tasks WHERE done = 1").fetchone()[0]
        return {"total": total, "done": done, "active": total - done}
