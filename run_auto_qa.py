"""
Ejecución de programación para gestion de calidad en código fuente

1 - Fiximports: separado y ordenado de importado de librerias, funciones, etc
2 - PyCodeStyle: verificación de especificaciones PEP8
3 - ImportChecker: verificacion de uso de elementos importados
"""
import os
import subprocess
import sys

def main():
    print("\n")
    print("Fixing imports (fiximports)")
    for root, dirs, files in os.walk(os.getcwd()):
        if root != os.getcwd():
            for f in files:
                if len(f.split('.')) > 1 and 'py' == f.split('.')[1]:
                    arch = "{}".format(os.path.join(root, f))
                    if "migrations" not in arch:
                        subprocess.call(
                            ['fiximports', arch], stdout=sys.stdout)
    print("\n")
    print("Codestyle Checking (pycodestyle)")
    for root, dirs, files in os.walk(os.getcwd()):
        if root != os.getcwd():
            for f in files:
                if len(f.split('.')) > 1 and 'py' == f.split('.')[1]:
                    arch = "{}".format(os.path.join(root, f))
                    if "migrations" not in arch:
                        subprocess.call(
                            ['pycodestyle', arch], stdout=sys.stdout)
    print("\n")
    print("Import checking (importchecker)")
    for root, dirs, files in os.walk(os.getcwd()):
        if root != os.getcwd():
            for f in files:
                if len(f.split('.')) > 1 and 'py' == f.split('.')[1]:
                    arch = "{}".format(os.path.join(root, f))
                    if "migrations" not in arch:
                        subprocess.call(
                            ['importchecker', arch], stdout=sys.stdout)

if __name__ == "__main__":
    main()
