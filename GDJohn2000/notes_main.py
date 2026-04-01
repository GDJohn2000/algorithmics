from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json

app = QApplication([])

notes = {

}
with open("notes_datas.json", "w", encoding="UTF-8") as file:
    json.dump(notes, file)

win_notes = QWidget()
win_notes.setWindowTitle("Notepod")
win_notes.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel("Lista de notas")

button_note_create = QPushButton('Crear nota')
button_note_del = QPushButton('Borrar nota')
button_note_save = QPushButton('Guardar nota')

list_tags_label = QLabel("Lista de etiquetas")
list_tags = QListWidget()
field_tag = QLineEdit("")
field_tag.setPlaceholderText("Ingresar etiqueta...")
button_tag_add = QPushButton("Agregar etiqueta")
button_tag_del = QPushButton("Eliminar etiqueta")
button_tag_search = QPushButton("Buscar nota por etiqueta")

field_text = QTextEdit()

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()

col_1.addWidget(field_text)

col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

col_2.addLayout(row_1)
col_2.addWidget(button_note_save)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_2 = QVBoxLayout()
row_2.addWidget(button_tag_add)
row_2.addWidget(button_tag_del)

col_2.addLayout(row_2)
col_2.addWidget(button_tag_search)

layout_notes.addLayout(col_1, stretch= 2)
layout_notes.addLayout(col_2, stretch= 1)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes[key]["tags"])

def create_note():
    note_name, ok = QInputDialog.getText(win_notes, "Crear nota", "Nombre de nota:")
    if ok and note_name != "" :
        notes[note_name] = {"text":"", "tags":[]}
        list_notes.addItem(note_name)
        #list_tags.addItems(notes[note_name]["tags"])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w",) as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("La nota para eliminar no esta seleccionada")


list_notes.clicked.connect(show_note)
button_note_create.clicked.connect(create_note)
button_note_del.clicked.connect(del_note)

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["tags"]:
            notes[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_datas.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("No hay nota seleccionada para agregar etiqueta")
button_tag_add.clicked.connect(add_tag)

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["tags"])
        with open("notes_datas.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("No hay etiqueta seleccionada para eliminar")
button_tag_del.clicked.connect(del_tag)

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Buscar nota por etiqueta" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["tags"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Restablecer busqueda")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Restablecer busqueda":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Buscar nota por etiqueta")
    else:
        pass
button_tag_search.clicked.connect(search_tag)

with open("notes_datas.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)


win_notes.setLayout(layout_notes)
win_notes.show()
app.exec_()