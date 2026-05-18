"""ToDo-приложение на Flet с SQLite-хранилищем.

Запуск:
    python lab8/main.py
"""

import flet as ft

import db

PRIORITY_LABELS = {"high": "Высокий", "normal": "Обычный", "low": "Низкий"}
PRIORITY_COLORS = {
    "high": ft.Colors.RED_400,
    "normal": ft.Colors.BLUE_400,
    "low": ft.Colors.GREY_500,
}


def main(page: ft.Page) -> None:
    page.title = "ToDo — Лабораторная №8"
    page.window_width = 720
    page.window_height = 720
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    db.init_db()

    title_field = ft.TextField(
        label="Что нужно сделать?",
        expand=True,
        on_submit=lambda e: on_add(e),
        autofocus=True,
    )
    priority_field = ft.Dropdown(
        label="Приоритет",
        width=160,
        value="normal",
        options=[
            ft.dropdown.Option("high", "Высокий"),
            ft.dropdown.Option("normal", "Обычный"),
            ft.dropdown.Option("low", "Низкий"),
        ],
    )

    filter_priority = ft.Dropdown(
        label="Фильтр",
        width=160,
        value="all",
        options=[
            ft.dropdown.Option("all", "Все"),
            ft.dropdown.Option("high", "Высокий"),
            ft.dropdown.Option("normal", "Обычный"),
            ft.dropdown.Option("low", "Низкий"),
        ],
        on_change=lambda e: refresh(),
    )
    show_done_switch = ft.Switch(
        label="Показывать выполненные",
        value=True,
        on_change=lambda e: refresh(),
    )

    stats_text = ft.Text("", size=13, color=ft.Colors.GREY_700)
    tasks_column = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)

    snack = ft.SnackBar(content=ft.Text(""), open=False)
    page.overlay.append(snack)

    def show_snack(message: str) -> None:
        snack.content = ft.Text(message)
        snack.open = True
        page.update()

    def build_task_row(row) -> ft.Control:
        task_id = row["id"]
        is_done = bool(row["done"])

        checkbox = ft.Checkbox(
            value=is_done,
            on_change=lambda e, tid=task_id: on_toggle(tid),
        )
        title = ft.Text(
            row["title"],
            size=15,
            expand=True,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.GREY_500 if is_done else ft.Colors.BLACK,
            italic=is_done,
        )
        priority_badge = ft.Container(
            content=ft.Text(
                PRIORITY_LABELS[row["priority"]],
                size=11,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=PRIORITY_COLORS[row["priority"]],
            padding=ft.padding.symmetric(horizontal=8, vertical=3),
            border_radius=10,
        )
        edit_btn = ft.IconButton(
            icon=ft.Icons.EDIT_OUTLINED,
            tooltip="Редактировать",
            icon_size=18,
            on_click=lambda e, r=row: open_edit_dialog(r),
        )
        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            tooltip="Удалить",
            icon_size=18,
            icon_color=ft.Colors.RED_400,
            on_click=lambda e, tid=task_id: on_delete(tid),
        )

        return ft.Container(
            content=ft.Row(
                [checkbox, title, priority_badge, edit_btn, delete_btn],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.GREY_100 if is_done else ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
        )

    def refresh() -> None:
        tasks = db.list_tasks(
            show_done=show_done_switch.value,
            priority=filter_priority.value,
        )
        tasks_column.controls = (
            [build_task_row(t) for t in tasks]
            if tasks
            else [
                ft.Container(
                    content=ft.Text(
                        "Пока ничего нет. Добавьте первую задачу.",
                        color=ft.Colors.GREY_500,
                        italic=True,
                    ),
                    padding=20,
                    alignment=ft.alignment.center,
                )
            ]
        )
        s = db.stats()
        stats_text.value = (
            f"Всего: {s['total']}    •    Активных: {s['active']}    •    Выполнено: {s['done']}"
        )
        page.update()

    def on_add(_event) -> None:
        try:
            db.add_task(title_field.value or "", priority_field.value)
        except ValueError as exc:
            show_snack(str(exc))
            return
        title_field.value = ""
        title_field.focus()
        refresh()

    def on_toggle(task_id: int) -> None:
        db.toggle_task(task_id)
        refresh()

    def on_delete(task_id: int) -> None:
        db.delete_task(task_id)
        show_snack("Задача удалена")
        refresh()

    def on_clear_done(_event) -> None:
        removed = db.clear_done()
        show_snack(f"Удалено выполненных: {removed}")
        refresh()

    def open_edit_dialog(row) -> None:
        edit_title = ft.TextField(label="Заголовок", value=row["title"], autofocus=True)
        edit_priority = ft.Dropdown(
            label="Приоритет",
            value=row["priority"],
            options=[
                ft.dropdown.Option("high", "Высокий"),
                ft.dropdown.Option("normal", "Обычный"),
                ft.dropdown.Option("low", "Низкий"),
            ],
        )

        def close_dialog(_e=None) -> None:
            dialog.open = False
            page.update()

        def save(_e) -> None:
            try:
                db.update_task(row["id"], edit_title.value, edit_priority.value)
            except ValueError as exc:
                show_snack(str(exc))
                return
            close_dialog()
            refresh()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Задача #{row['id']}"),
            content=ft.Column([edit_title, edit_priority], tight=True, width=320),
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog),
                ft.ElevatedButton("Сохранить", on_click=save),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    add_row = ft.Row(
        [
            title_field,
            priority_field,
            ft.ElevatedButton(
                "Добавить",
                icon=ft.Icons.ADD,
                on_click=on_add,
                height=50,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    filter_row = ft.Row(
        [
            filter_priority,
            show_done_switch,
            ft.Container(expand=True),
            ft.OutlinedButton(
                "Очистить выполненные",
                icon=ft.Icons.CLEANING_SERVICES_OUTLINED,
                on_click=on_clear_done,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Система учёта задач (ToDo)",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Лабораторная №8 • Flet + SQLite",
                    size=12,
                    color=ft.Colors.GREY_600,
                ),
                ft.Divider(),
                add_row,
                filter_row,
                ft.Divider(),
                stats_text,
                tasks_column,
            ],
            expand=True,
        )
    )

    refresh()


if __name__ == "__main__":
    ft.app(target=main)
