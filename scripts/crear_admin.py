"""
Genera el INSERT SQL para crear un usuario del panel de administración,
con la contraseña ya hasheada (nunca se guarda en texto plano).

Uso:
    python scripts/crear_admin.py

Te va a pedir usuario y contraseña, y te imprime el SQL listo para
pegar y correr en MySQL Workbench.
"""
import os
import sys
import getpass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt


def main():
    usuario = input("Usuario para el panel admin: ").strip()
    password = getpass.getpass("Contraseña: ")
    password2 = getpass.getpass("Repite la contraseña: ")

    if password != password2:
        print("Las contraseñas no coinciden. Intenta de nuevo.")
        return

    if len(password) < 8:
        print("Usa una contraseña de al menos 8 caracteres.")
        return

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    print("\nCopia y corre esto en MySQL Workbench:\n")
    print("USE vidplex;")
    print(
        "INSERT INTO admin_usuarios (usuario, password_hash) VALUES "
        f"('{usuario}', '{hashed}');"
    )
    print()


if __name__ == '__main__':
    main()
