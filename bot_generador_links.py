import tkinter as tk
from tkinter import ttk
import random
import time
import threading

class BotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot de Fila Virtual - Estilo Moderno")
        self.root.geometry("900x500")
        self.root.config(bg="#212121")

        # Variables
        self.links = []
        self.proxies = []
        self.task_counter = 1

        # Interface de usuario
        self.create_widgets()

    def create_widgets(self):
        # Enlace Base
        self.base_label = tk.Label(self.root, text="Enlace Base:", bg="#212121", fg="white")
        self.base_label.pack(pady=5)
        self.base_entry = tk.Entry(self.root, width=60, bg="#2E2E2E", fg="white", insertbackground="white")
        self.base_entry.pack(pady=5)

        # Proxies
        self.proxy_label = tk.Label(self.root, text="Proxies (separados por comas):", bg="#212121", fg="white")
        self.proxy_label.pack(pady=5)
        self.proxy_entry = tk.Entry(self.root, width=60, bg="#2E2E2E", fg="white", insertbackground="white")
        self.proxy_entry.pack(pady=5)

        # Cantidad de Enlaces
        self.amount_label = tk.Label(self.root, text="Cantidad de Enlaces:", bg="#212121", fg="white")
        self.amount_label.pack(pady=5)
        self.amount_entry = tk.Entry(self.root, width=10, bg="#2E2E2E", fg="white", insertbackground="white")
        self.amount_entry.pack(pady=5)

        # Botones
        self.run_button = tk.Button(self.root, text="Run", command=self.run_bot, bg="#28a745", fg="white")
        self.run_button.pack(pady=20)
        
        self.delete_button = tk.Button(self.root, text="Eliminar Todos", command=self.clear_table, bg="#dc3545", fg="white")
        self.delete_button.pack(pady=5)

        # Tabla
        self.table = ttk.Treeview(self.root, columns=("Task", "Store", "Proxy", "Estado", "Link", "Número de Fila"), show="headings")
        self.table.heading("Task", text="Task")
        self.table.heading("Store", text="Store")
        self.table.heading("Proxy", text="Proxy")
        self.table.heading("Estado", text="Estado")
        self.table.heading("Link", text="Link")
        self.table.heading("Número de Fila", text="Número de Fila")
        self.table.pack(pady=10)

    def generate_link(self, base_url, proxy, task_number, row_number):
        # Aquí generamos el enlace
        link = f"{base_url}&proxy={proxy}&task={task_number}"
        return link, row_number

    def run_bot(self):
        # Limpiar la tabla antes de comenzar
        self.clear_table()

        # Obtener datos del usuario
        base_url = self.base_entry.get()
        proxies = self.proxy_entry.get().split(",")
        amount = int(self.amount_entry.get())

        # Generar enlaces y asignar proxies
        row_number = 1
        for i in range(amount):
            proxy = random.choice(proxies)
            link, fila = self.generate_link(base_url, proxy, i + 1, row_number)
            self.links.append(link)
            self.proxies.append(proxy)
            self.insert_into_table(i + 1, base_url.split("?")[0], proxy, "Monitoreando", link, fila)
            row_number += 1

        # Actualizar estado
        self.update_state()

    def update_state(self):
        for item in self.table.get_children():
            task = self.table.item(item, "values")[0]
            row_number = int(self.table.item(item, "values")[5])
            # Esperamos que el número de fila llegue al 1, entonces mostramos "Completado"
            if row_number == 1:
                self.table.item(item, values=(task, "queue.puntoticket.com", self.proxies[task - 1], "Completado", self.links[task - 1], row_number))
            else:
                self.table.item(item, values=(task, "queue.puntoticket.com", self.proxies[task - 1], "Monitoreando", self.links[task - 1], row_number))

    def insert_into_table(self, task, store, proxy, estado, link, fila):
        self.table.insert("", "end", values=(task, store, proxy, estado, link, fila))

    def clear_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

# Crear la ventana principal de Tkinter
root = tk.Tk()
app = BotApp(root)
root.mainloop()
