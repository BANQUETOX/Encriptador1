
import pickle
import datetime
import string
import random
import glob
import os


def main_menu() -> int:
    print("-------------------------------------------")
    print("              Menu principal            ")
    print("               PassManager            \n")
    print("* Crear nuevo archivo de contraseñas (1)")
    print("* Leer archivo de contraseñas (2)")
    print("* Eliminar archivo de contraseñas (3) ")
    print("* Salir (4)")
    option = int(input("\n- "))
    while option not in [1, 2, 3, 4]:
        print("Seleccion invalida")
        option = int(input("\n- "))
    print("-------------------------------------------")
    return (option)


def save_new_pasword_archive():
    passwords_archive = {}
    save_other = "s"
    filename = input("* Escriba un nombre para su archivo de contraseñas: ")
    while save_other == "s":
        label = input("* Cual el el sitio web: ")
        raw_password = input("- Escriba su contraseña: ")
        print("* Para crear su clave se necesita un dia, mes y año")
        year = int(input("- Seleccione un año "))
        while year < 0:
            print("* Seleccion invalida")
            year = input("- Seleccione un año ")
        month = int(input("- Seleccione un mes "))
        while month < 0 or month > 12:
            print("* Seleccion invalida")
            month = input("- Seleccione un mes ")
        day = int(input("- Seleccione un dia "))
        while day < 0 or day > 31:
            print("*Seleccion invalida")
            day = input("- Seleccione un dia ")
        date_key = datetime.datetime(year, month, day)
        encrypted_password = encrypt_password(raw_password, date_key)
        passwords_archive[label] = encrypted_password
        save_other = input("- Desea guardar otra contraseña? (s/n)").lower
    with open(filename + ".pickle", 'wb') as handle:
        pickle.dump(passwords_archive, handle,
                    protocol=pickle.HIGHEST_PROTOCOL)
    print("* Archivo de contraseñas guardado!!!")
    print("* Recuerde guardar sus claves en un lugar seguro")


def read_pasword_archive():
    print("       Menu de lectura de archivos            ")
    print("               PassManager            \n")
    print("* Escriba el nombre de su archivo de contraseñas\n")
    current_path = os.getcwd()
    for file in glob.glob(f"{current_path}\*.pickle"):
        print("*", end=" ")
        file_name = os.path.basename(file)
        print(file_name)
    file_name_selected = input("- ")
    with open(file_name_selected, 'rb') as handle:
        unpickled_file = pickle.load(handle)
    print("* Escriba el nombre del sitio que desea desencriptar")
    for key, _ in unpickled_file.items():
        print("*", end=" ")
        print(key)
    selected_key = input("- ")
    print("* Para desencriptar su contraseña debe insetar su clave")
    year = int(input("- Escriba el año "))
    while year < 0:
        print("* Seleccion invalida")
        year = input("- Escriba el año ")
    month = int(input("- Escriba el mes "))
    while month < 0 or month > 12:
        print("* Seleccion invalida")
        month = input("- Escriba el mes ")
    day = int(input("- Escriba el dia "))
    while day < 0 or day > 31:
        print("*Seleccion invalida")
        day = input("- Escriba el dia ")
    date_key = datetime.datetime(year, month, day)
    password = decrypt_password(unpickled_file[selected_key], date_key)
    print("* Su contraseña es:", password)


def delete_archive():
    print("       Menu de eliminacion de archivos            ")
    print("               PassManager            \n")
    print("* Escriba el nombre el archivo que desea eliminar")
    print("* ADVERTENCIA: Todas las contraseñas seran permanentemente eliminadas!")
    current_path = os.getcwd()
    for file in glob.glob(f"{current_path}\*.pickle"):
        print("*", end=" ")
        file_name = os.path.basename(file)
        print(file_name)
    file_name_selected = input("- ")
    os.remove(file_name_selected)
    print("Archivo eliminado!")


def encrypt_password(raw_password: str, date_key: datetime.datetime) -> str:
    day = date_key.day
    month = date_key.month
    year = date_key.year
    sum_date_numbers = (year + month + day)
    new_key = (sum_date_numbers * year) + \
        (sum_date_numbers * month) * (sum_date_numbers * day)
    new_raw_password = raw_password + str(new_key)
    while len(new_raw_password) < 128:
        new_raw_password = new_raw_password + random.choice(characters_list)

    encrypted_password = ""
    for i, char in enumerate(new_raw_password):
        character_position = characters_list.index(char)
        encrypted_password += characters_list[(character_position + (new_key + day + ((i + year) * (i + month)))) %
                                              len(characters_list)]

    return encrypted_password


def decrypt_password(encrypted_password: str, date_key: datetime.datetime) -> str:
    day = date_key.day
    month = date_key.month
    year = date_key.year
    sum_date_numbers = (year + month + day)
    new_key = (sum_date_numbers * year) + \
        (sum_date_numbers * month) * (sum_date_numbers * day)

    decrypted_password = ""
    for i, char in enumerate(encrypted_password):
        character_position = characters_list.index(char)
        decrypted_password += characters_list[(character_position - (new_key + day + ((i + year) * (i + month)))) %
                                              len(characters_list)]

    decrypted_password = decrypted_password.split(str(new_key))[0]
    return decrypted_password


characters_list = string.ascii_letters + string.digits + string.punctuation
while True:
    option_menu = main_menu()
    if option_menu == 1:
        save_new_pasword_archive()
    elif option_menu == 2:
        read_pasword_archive()
    elif option_menu == 3:
        delete_archive()
    elif option_menu == 4:
        exit()
