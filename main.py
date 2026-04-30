import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime
import os

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator - Генератор случайных задач")
        self.root.geometry("850x650")
        self.root.resizable(True, True)

        # Предопределённые задачи по категориям
        self.default_tasks = {
            "Учёба": [
                "📚 Прочитать статью по теме",
                "✍️ Сделать конспект урока",
                "💻 Пройти онлайн-курс (30 мин)",
                "📝 Решить 5 задач по математике",
                "🌐 Изучить 10 новых английских слов",
                "📖 Прочитать 20 страниц книги",
                "🎓 Посмотреть образовательное видео",
                "📊 Сделать домашнее задание"
            ],
            "Спорт": [
                "🏃 Сделать зарядку (15 мин)",
                "🧘 Йога-комплекс (20 мин)",
                "💪 Отжимания 3×10",
                "🚶 Прогулка на свежем воздухе",
                "🏊 Плавание (30 мин)",
                "🚴 Покататься на велосипеде",
                "🤸 Растяжка всего тела",
                "🏋️ Тренировка с весом тела"
            ],
            "Работа": [
                "💼 Проверить рабочие email",
                "📅 Составить план на день",
                "📊 Подготовить отчёт",
                "🤝 Связаться с коллегой",
                "💡 Записать 3 идеи для проекта",
                "⏰ Оптимизировать рабочий процесс",
                "📈 Изучить новые инструменты",
                "✅ Закончить начатую задачу"
            ]
        }

        # Загрузка задач и истории
        self.tasks = self.load_tasks()
        self.history = self.load_history()
        self.current_filter = "Все"

        # Создание GUI
        self.create_task_management_frame()
        self.create_generator_frame()
        self.create_filter_frame()
        self.create_history_frame()
        self.create_button_frame()

        # Обновление отображения
        self.update_task_display()
        self.update_history_display()

    def create_task_management_frame(self):
        """Создание рамки для управления задачами"""
        manage_frame = tk.LabelFrame(self.root, text="Управление задачами", padx=10, pady=10, font=("Arial", 10, "bold"))
        manage_frame.pack(fill="x", padx=10, pady=5)

        # Добавление новой задачи
        tk.Label(manage_frame, text="Новая задача:").grid(row=0, column=0, sticky="w", padx=5)
        self.new_task_entry = tk.Entry(manage_frame, width=40)
        self.new_task_entry.grid(row=0, column=1, padx=5, columnspan=2)

        tk.Label(manage_frame, text="Категория:").grid(row=0, column=3, sticky="w", padx=5)
        self.new_task_category = ttk.Combobox(manage_frame, values=["Учёба", "Спорт", "Работа"], width=12)
        self.new_task_category.set("Учёба")
        self.new_task_category.grid(row=0, column=4, padx=5)

        self.add_task_btn = tk.Button(manage_frame, text="➕ Добавить задачу", command=self.add_task, bg="#4CAF50", fg="white")
        self.add_task_btn.grid(row=0, column=5, padx=10)

        # Список существующих задач
        tk.Label(manage_frame, text="Существующие задачи:").grid(row=1, column=0, sticky="w", padx=5, pady=(10,0))
        
        # Рамка для списка задач с прокруткой
        list_frame = tk.Frame(manage_frame)
        list_frame.grid(row=2, column=0, columnspan=6, sticky="ew", pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tasks_listbox = tk.Listbox(list_frame, height=5, yscrollcommand=scrollbar.set, font=("Arial", 9))
        self.tasks_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.tasks_listbox.yview)
        
        # Кнопки управления задачами
        btn_frame = tk.Frame(manage_frame)
        btn_frame.grid(row=3, column=0, columnspan=6, pady=5)
        
        self.edit_task_btn = tk.Button(btn_frame, text="✏️ Редактировать", command=self.edit_task, bg="#FF9800", fg="white")
        self.edit_task_btn.pack(side="left", padx=5)
        
        self.delete_task_btn = tk.Button(btn_frame, text="🗑 Удалить задачу", command=self.delete_task, bg="#F44336", fg="white")
        self.delete_task_btn.pack(side="left", padx=5)

    def create_generator_frame(self):
        """Создание рамки для генерации задач"""
        generator_frame = tk.LabelFrame(self.root, text="Генератор задач", padx=10, pady=10, font=("Arial", 10, "bold"))
        generator_frame.pack(fill="x", padx=10, pady=5)

        self.generate_btn = tk.Button(generator_frame, text="🎲 Сгенерировать случайную задачу", command=self.generate_task,
                                      bg="#2196F3", fg="white", font=("Arial", 12, "bold"), height=2)
        self.generate_btn.pack(fill="x", pady=5)

        self.current_task_label = tk.Label(generator_frame, text="", font=("Arial", 14, "bold"), fg="#4CAF50", wraplength=800)
        self.current_task_label.pack(pady=10)

    def create_filter_frame(self):
        """Создание рамки для фильтрации"""
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация истории", padx=10, pady=10, font=("Arial", 10, "bold"))
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Фильтр по категории:").pack(side="left", padx=5)
        
        self.filter_var = tk.StringVar(value="Все")
        filter_options = ["Все", "Учёба", "Спорт", "Работа"]
        
        for option in filter_options:
            tk.Radiobutton(filter_frame, text=option, variable=self.filter_var, value=option,
                          command=self.apply_filter).pack(side="left", padx=10)

        self.filter_stats_label = tk.Label(filter_frame, text="", font=("Arial", 9, "italic"), fg="gray")
        self.filter_stats_label.pack(side="right", padx=10)

    def create_history_frame(self):
        """Создание рамки с историей задач"""
        history_frame = tk.LabelFrame(self.root, text="История сгенерированных задач", padx=10, pady=10, font=("Arial", 10, "bold"))
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Таблица истории
        columns = ("№", "Время", "Категория", "Задача")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.history_tree.heading(col, text=col)
        
        self.history_tree.column("№", width=50, anchor="center")
        self.history_tree.column("Время", width=150, anchor="center")
        self.history_tree.column("Категория", width=100, anchor="center")
        self.history_tree.column("Задача", width=500, anchor="w")

        # Скроллбары
        scroll_y = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        scroll_x = ttk.Scrollbar(history_frame, orient="horizontal", command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.history_tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        # Контекстное меню для истории
        self.history_menu = tk.Menu(self.root, tearoff=0)
        self.history_menu.add_command(label="🗑 Удалить запись", command=self.delete_history_entry)
        self.history_menu.add_command(label="🔄 Повторить задачу", command=self.repeat_task)
        self.history_tree.bind("<Button-3>", self.show_history_menu)

    def create_button_frame(self):
        """Создание рамки с кнопками управления"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        self.save_btn = tk.Button(button_frame, text="💾 Сохранить историю", command=self.save_history_to_file,
                                  bg="#9C27B0", fg="white", width=15)
        self.save_btn.pack(side="left", padx=5)

        self.load_btn = tk.Button(button_frame, text="📂 Загрузить историю", command=self.load_history_from_file,
                                  bg="#607D8B", fg="white", width=15)
        self.load_btn.pack(side="left", padx=5)

        self.clear_btn = tk.Button(button_frame, text="🗑 Очистить историю", command=self.clear_history,
                                   bg="#F44336", fg="white", width=15)
        self.clear_btn.pack(side="left", padx=5)

        self.reset_defaults_btn = tk.Button(button_frame, text="🔄 Сбросить задачи по умолчанию", command=self.reset_to_defaults,
                                            bg="#FF9800", fg="white", width=20)
        self.reset_defaults_btn.pack(side="left", padx=5)

        self.exit_btn = tk.Button(button_frame, text="🚪 Выйти", command=self.save_and_exit,
                                  bg="#555555", fg="white", width=10)
        self.exit_btn.pack(side="right", padx=5)

    def add_task(self):
        """Добавление новой задачи"""
        task_text = self.new_task_entry.get().strip()
        category = self.new_task_category.get()

        if not task_text:
            messagebox.showerror("Ошибка", "Текст задачи не может быть пустым!")
            return

        if category not in self.tasks:
            self.tasks[category] = []

        self.tasks[category].append(task_text)
        self.save_tasks()
        self.update_task_display()
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача добавлена в категорию '{category}'")

    def edit_task(self):
        """Редактирование выбранной задачи"""
        selection = self.tasks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
            return

        selected_text = self.tasks_listbox.get(selection[0])
        # Определяем категорию выбранной задачи
        category = None
        for cat, tasks in self.tasks.items():
            if selected_text in tasks:
                category = cat
                break

        if category:
            dialog = tk.Toplevel(self.root)
            dialog.title("Редактировать задачу")
            dialog.geometry("400x150")
            dialog.resizable(False, False)

            tk.Label(dialog, text="Редактировать задачу:").pack(pady=5)
            entry = tk.Entry(dialog, width=50)
            entry.insert(0, selected_text)
            entry.pack(pady=5)

            def save_edit():
                new_text = entry.get().strip()
                if new_text:
                    index = self.tasks[category].index(selected_text)
                    self.tasks[category][index] = new_text
                    self.save_tasks()
                    self.update_task_display()
                    dialog.destroy()
                    messagebox.showinfo("Успех", "Задача обновлена")
                else:
                    messagebox.showerror("Ошибка", "Текст не может быть пустым")

            tk.Button(dialog, text="Сохранить", command=save_edit, bg="#4CAF50", fg="white").pack(pady=10)

    def delete_task(self):
        """Удаление выбранной задачи"""
        selection = self.tasks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return

        selected_text = self.tasks_listbox.get(selection[0])
        
        # Находим категорию задачи
        for category, tasks in self.tasks.items():
            if selected_text in tasks:
                if messagebox.askyesno("Подтверждение", f"Удалить задачу:\n'{selected_text}'?"):
                    tasks.remove(selected_text)
                    # Удаляем категорию, если она стала пустой
                    if not tasks and category not in self.default_tasks:
                        del self.tasks[category]
                    self.save_tasks()
                    self.update_task_display()
                    messagebox.showinfo("Успех", "Задача удалена")
                break

    def generate_task(self):
        """Генерация случайной задачи"""
        # Собираем все задачи или только из выбранной категории
        if self.current_filter == "Все":
            all_tasks = []
            for category, tasks in self.tasks.items():
                for task in tasks:
                    all_tasks.append((category, task))
        else:
            all_tasks = [(self.current_filter, task) for task in self.tasks.get(self.current_filter, [])]

        if not all_tasks:
            messagebox.showwarning("Предупреждение", f"Нет задач в категории '{self.current_filter}'\nДобавьте задачи или смените фильтр")
            return

        # Выбираем случайную задачу
        category, task = random.choice(all_tasks)
        
        # Отображаем задачу
        self.current_task_label.config(text=f"✨ {task} ✨")
        
        # Сохраняем в историю
        history_entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "task": task
        }
        self.history.append(history_entry)
        self.save_history()
        self.update_history_display()

        # Анимация кнопки
        self.generate_btn.config(state="disabled")
        self.root.after(1000, lambda: self.generate_btn.config(state="normal"))

    def apply_filter(self):
        """Применение фильтра категории"""
        self.current_filter = self.filter_var.get()
        if self.current_filter == "Все":
            self.filter_stats_label.config(text="Показаны все категории")
        else:
            task_count = len(self.tasks.get(self.current_filter, []))
            self.filter_stats_label.config(text=f"Категория: {self.current_filter} (доступно задач: {task_count})")
        
        # Генерируем новую задачу в соответствии с фильтром (опционально)
        if self.history:
            self.update_history_display()

    def update_task_display(self):
        """Обновление отображения списка задач"""
        self.tasks_listbox.delete(0, tk.END)
        
        for category, tasks in sorted(self.tasks.items()):
            if tasks:
                self.tasks_listbox.insert(tk.END, f"--- {category} ---")
                for task in tasks:
                    self.tasks_listbox.insert(tk.END, f"  • {task}")

    def update_history_display(self):
        """Обновление отображения истории с учётом фильтра"""
        # Очистка таблицы
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Фильтрация истории
        if self.current_filter == "Все":
            filtered_history = self.history
        else:
            filtered_history = [h for h in self.history if h["category"] == self.current_filter]

        # Отображение записей (последние сверху)
        for entry in reversed(filtered_history[-50:]):  # Показываем последние 50
            self.history_tree.insert("", "end", values=(
                entry["id"],
                entry["timestamp"],
                entry["category"],
                entry["task"]
            ))

    def delete_history_entry(self):
        """Удаление выбранной записи из истории"""
        selected = self.history_tree.selection()
        if not selected:
            return

        item = self.history_tree.item(selected[0])
        task_id = int(item['values'][0])

        if messagebox.askyesno("Подтверждение", "Удалить эту запись из истории?"):
            self.history = [h for h in self.history if h["id"] != task_id]
            # Перенумерация ID
            for i, entry in enumerate(self.history, 1):
                entry["id"] = i
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("Успех", "Запись удалена из истории")

    def repeat_task(self):
        """Повтор задачи из истории"""
        selected = self.history_tree.selection()
        if not selected:
            return

        item = self.history_tree.item(selected[0])
        task_text = item['values'][3]
        category = item['values'][2]
        
        # Добавляем новую запись в историю
        history_entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "task": task_text
        }
        self.history.append(history_entry)
        self.save_history()
        self.update_history_display()
        self.current_task_label.config(text=f"🔄 Повтор: {task_text}")

    def show_history_menu(self, event):
        """Показать контекстное меню для истории"""
        item = self.history_tree.identify_row(event.y)
        if item:
            self.history_tree.selection_set(item)
            self.history_menu.post(event.x_root, event.y_root)

    def save_history_to_file(self):
        """Сохранение истории в JSON по запросу"""
        if self.save_history():
            messagebox.showinfo("Успех", "История сохранена в tasks_history.json")

    def load_history_from_file(self):
        """Загрузка истории из JSON по запросу"""
        if messagebox.askyesno("Подтверждение", "Загрузить историю из файла? Текущая история будет заменена."):
            loaded = self.load_history()
            if loaded:
                self.history = loaded
                self.update_history_display()
                messagebox.showinfo("Успех", f"Загружено {len(loaded)} записей")
            else:
                messagebox.showinfo("Информация", "Файл не найден или пуст")

    def clear_history(self):
        """Очистка всей истории"""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю задач? Это действие нельзя отменить!"):
            self.history = []
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("Успех", "История очищена")

    def reset_to_defaults(self):
        """Сброс к задачам по умолчанию"""
        if messagebox.askyesno("Подтверждение", "Сбросить все задачи к настройкам по умолчанию? Текущие задачи будут потеряны!"):
            self.tasks = self.default_tasks.copy()
            self.save_tasks()
            self.update_task_display()
            messagebox.showinfo("Успех", "Задачи сброшены к стандартному набору")

    def save_tasks(self):
        """Сохранение задач в JSON"""
        try:
            with open("tasks_data.json", "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить задачи: {str(e)}")
            return False

    def load_tasks(self):
        """Загрузка задач из JSON"""
        try:
            if os.path.exists("tasks_data.json"):
                with open("tasks_data.json", "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # Проверяем, что структура корректна
                    if isinstance(loaded, dict):
                        return loaded
        except Exception as e:
            print(f"Ошибка загрузки задач: {e}")
        return self.default_tasks.copy()

    def save_history(self):
        """Сохранение истории в JSON (автоматически)"""
        try:
            with open("tasks_history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")
            return False

    def load_history(self):
        """Загрузка истории из JSON"""
        try:
            if os.path.exists("tasks_history.json"):
                with open("tasks_history.json", "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
        return []

    def save_and_exit(self):
        """Сохранение и выход"""
        self.save_tasks()
        self.save_history()
        self.root.quit()

def main():
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()