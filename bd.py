import sqlite3
from datetime import datetime

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Criação das tabelas
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    full_name TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES Users(id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS UserGroups (
    user_id INTEGER,
    group_id INTEGER,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE CASCADE
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS GroupPermissions (
    group_id INTEGER,
    permission_id INTEGER,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, permission_id),
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES Permissions(id) ON DELETE CASCADE
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS OperationLogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    group_id INTEGER,
    operation TEXT,
    details TEXT,
    operation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE SET NULL,
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE SET NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    group_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES Locations(id) ON DELETE SET NULL,
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE SET NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location_id INTEGER,
    parent_object_id INTEGER,
    group_id INTEGER,
    FOREIGN KEY (location_id) REFERENCES Locations(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_object_id) REFERENCES Objects(id) ON DELETE SET NULL,
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE SET NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_id INTEGER,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (object_id) REFERENCES Objects(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES Groups(id) ON DELETE SET NULL
)''')

# Inserção de dados de exemplo
cursor.execute('''INSERT INTO Users (username, full_name, email) 
                  VALUES ('usuario1', 'Usuário 1', 'usuario1@exemplo.com')''')
user_id = cursor.lastrowid

cursor.execute('''INSERT INTO Groups (name, created_by) 
                  VALUES ('Gerência', ?)''', (user_id,))
group_id = cursor.lastrowid

cursor.execute('''INSERT INTO UserGroups (user_id, group_id) 
                  VALUES (?, ?)''', (user_id, group_id))

cursor.execute('''INSERT INTO Permissions (name, description) 
                  VALUES ('Gerenciar Objetos', 'Permite adicionar, editar e remover objetos em locais associados')''')
permission_id = cursor.lastrowid

cursor.execute('''INSERT INTO GroupPermissions (group_id, permission_id) 
                  VALUES (?, ?)''', (group_id, permission_id))

cursor.execute('''INSERT INTO Locations (name, group_id) 
                  VALUES ('Almoxarifado', ?)''', (group_id,))
location_id = cursor.lastrowid

cursor.execute('''INSERT INTO Objects (name, location_id, group_id) 
                  VALUES ('Refrigerador de Vacinas', ?, ?)''', (location_id, group_id))
object_id = cursor.lastrowid

cursor.execute('''INSERT INTO Attributes (object_id, name, value, group_id) 
                  VALUES (?, 'Temperatura', '2°C', ?)''', (object_id, group_id))

cursor.execute('''INSERT INTO OperationLogs (user_id, group_id, operation, details) 
                  VALUES (?, ?, 'Criação de Objeto', 'Usuário 1 criou o objeto Refrigerador de Vacinas no Almoxarifado')''', 
                  (user_id, group_id))

# Commit das operações
conn.commit()

# Consultas de teste
print("Usuarios:")
for row in cursor.execute('''SELECT * FROM Users'''):
    print(row)

print("\nGrupos:")
for row in cursor.execute('''SELECT * FROM Groups'''):
    print(row)

print("\nLocais:")
for row in cursor.execute('''SELECT * FROM Locations'''):
    print(row)

print("\nObjetos:")
for row in cursor.execute('''SELECT * FROM Objects'''):
    print(row)

print("\nAtributos:")
for row in cursor.execute('''SELECT * FROM Attributes'''):
    print(row)

print("\nLogs de Operações:")
for row in cursor.execute('''SELECT * FROM OperationLogs'''):
    print(row)

# Fechamento da conexão
conn.close()