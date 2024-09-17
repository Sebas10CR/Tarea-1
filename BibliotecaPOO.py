"""
Creadores:
Sebastian Vega Castillo
Josue Espinoza Castillo
Christian Zepeda Ruiz
Eduardo Cascante Conejo

Prof. Estrellita Jenkins
Grupo #3 Los Arquitectos del Objeto
Biblioteca POO
Curso: INFO-103
"""
#Se importa el modulo csv lo cual nos permite almacenar datos en hojas de calculo
import csv
# Definimos la clase Libro para almacenar la información de cada libro
class Libro:
     # Inicializamos las propiedades del libro con la información proporcionada
    def __init__(self, titulo, autor, cantidad, isbn, genero, editorial, fecha_publicacion):
        self.titulo = titulo
        self.autor = autor
        self.cantidad = cantidad
        self.isbn = isbn
        self.genero = genero
        self.editorial = editorial
        self.fecha_publicacion = fecha_publicacion
        
# Definimos una clase Biblioteca para gestionar los libros y préstamos
class Biblioteca:
    def __init__(self):
        # Creamos una lista vacía para guardar libros y un diccionario para los préstamos
        self.libros = []
        self.prestamos = {}

    def agregar_libro(self, titulo, autor, cantidad, isbn, genero, editorial, fecha_publicacion):
        libro = Libro(titulo, autor, cantidad, isbn, genero, editorial, fecha_publicacion)
        self.libros.append(libro)
        print(f"Libro '{titulo}' agregado exitosamente.")
   # Crea un nuevo libro y lo agrega a la lista de libros
    def consultar_libros(self):
        if not self.libros:
            #Se muestra los libros disponibles en la biblioteca
            #En caso de no haber, se muestra el siguiente mensaje
            print("No hay libros en la biblioteca.")
        else:
            for libro in self.libros:
                print(f"Título: {libro.titulo}, Autor: {libro.autor}, Cantidad: {libro.cantidad}")

    def prestar_libro(self, titulo, usuario):
         # Busca el libro y lo presta al usuario si hay disponibilidad
        for libro in self.libros:
            if libro.titulo == titulo and libro.cantidad > 0:
                libro.cantidad -= 1
                if usuario in self.prestamos:
                    self.prestamos[usuario].append(libro.titulo)
                else:
                    self.prestamos[usuario] = [libro.titulo]
                print(f"Libro '{titulo}' prestado a {usuario}.")
                return
        print(f"No se puede prestar el libro '{titulo}'.")

    def devolver_libro(self, titulo, usuario):
         #En caso de que el usuario decida devolver un libro se solicitan los datos y de coincidir se actualiza en la base de datos
        if usuario in self.prestamos and titulo in self.prestamos[usuario]:
            for libro in self.libros:
                if libro.titulo == titulo:
                    libro.cantidad += 1
                    self.prestamos[usuario].remove(titulo)
                    print(f"Libro '{titulo}' devuelto por {usuario}.")
                    return 
                #En caso de que el usuario no haya pedido ese libro se muestar el siguiente mensaje
                print(f"{usuario} no tiene el libro '{titulo}' prestado.")

    def generar_informe(self, tipo):
        # Generamos un informe en formato de texto o CSV
        if tipo == 'texto':
            with open('informe_biblioteca.txt', 'w') as file:
                file.write(self.resumen_informe())
        elif tipo == 'csv':
            with open('informe_biblioteca.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                # Escribe los encabezados del informe
                writer.writerow(['Título', 'Autor', 'ISBN', 'Género', 'Editorial', 'Fecha de Publicación', 'Cantidad'])
                # Escribe los datos de cada libro
                for libro in self.libros:
                    writer.writerow([libro.titulo, libro.autor, libro.isbn, libro.genero, libro.editorial, libro.fecha_publicacion, libro.cantidad])
                writer.writerow([])
                writer.writerow(['Libros Prestados'])
                # Escribe los libros prestados y quién los tiene
                for usuario, libros in self.prestamos.items():
                    writer.writerow([f'Usuario: {usuario}'])
                    for titulo in libros:
                        writer.writerow([f'- {titulo}'])
        print(f"Informe generado en formato {tipo}.")

    def resumen_informe(self):
        # Crea un resumen del estado de la biblioteca
        resumen = "Estado Actual de la Biblioteca:\n"
        resumen += f"Cantidad total de libros: {len(self.libros)}\n"
        
        # Detalles de todos los libros
        resumen += "Detalles de todos los libros:\n"
        for libro in self.libros:
            resumen += f"Título: {libro.titulo}, Autor: {libro.autor}, ISBN: {libro.isbn}, Género: {libro.genero}, Editorial: {libro.editorial}, Fecha de Publicación: {libro.fecha_publicacion}, Cantidad: {libro.cantidad}\n"
        
        resumen += "\nLibros con mayor stock:\n"
        # Muestra los primeros 5 libros con más cantidad disponible
        for libro in sorted(self.libros, key=lambda x: x.cantidad, reverse=True)[:5]:
            resumen += f"{libro.titulo} - Cantidad disponible: {libro.cantidad}\n"
        
        resumen += "\nLibros registrados con poco stock:\n"
        # Muestra los libros con menos de 5 unidades disponibles
        for libro in self.libros:
            if libro.cantidad < 5:
                resumen += f"{libro.titulo} - Cantidad disponible: {libro.cantidad}\n"
        
        resumen += "\nLibros Prestados:\n"
        # Muestra los libros que están prestados y quién los tiene
        for usuario, libros in self.prestamos.items():
            resumen += f"Usuario: {usuario}\n"
            for titulo in libros:
                resumen += f"- {titulo}\n"
        
        return resumen


def mostrar_menu():
    # Muestra las opciones disponibles en el menú
    print("\n--- Menú Biblioteca ---")
    print("1. Agregar libro")
    print("2. Consultar libros")
    print("3. Prestar libro")
    print("4. Devolver libro")
    print("5. Generar informe")
    print("6. Salir")

def main():
    biblioteca = Biblioteca()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
             # Solicita la información del libro y lo agrega a la biblioteca
            titulo = input("\nTítulo del libro: ").lower()
            autor = input("Autor del libro: ").lower()
            cantidad = int(input("Cantidad disponible: "))
            isbn = input("ISBN: ")
            genero = input("Género: ")
            editorial = input("Editorial: ")
            fecha_publicacion = input("Fecha de Publicación: ")
            biblioteca.agregar_libro(titulo, autor, cantidad, isbn, genero, editorial, fecha_publicacion)
        elif opcion == "2":
            # Muestra la lista de libros en la biblioteca
            biblioteca.consultar_libros()
        elif opcion == "3":
            # Presta un libro al usuario
            titulo = input("Título del libro a prestar: ").lower()
            usuario = input("Nombre del usuario: ").lower()
            biblioteca.prestar_libro(titulo, usuario)
        elif opcion == "4":
            # Devuelve un libro prestado por el usuario
            titulo = input("Título del libro a devolver: ").lower()
            usuario = input("Nombre del usuario: ").lower()
            biblioteca.devolver_libro(titulo, usuario)
        elif opcion == "5":
             # Genera un informe en el formato elegido
            tipo = input("Tipo de informe (texto/csv): ").lower()
            biblioteca.generar_informe(tipo)
        elif opcion == "6":
            # Sale del programa
            print("Saliendo del sistema.")
            break
        else:
            # Maneja opciones no válidas
            print("Opción no válida, por favor intenta nuevamente.")

# Verifica si este archivo se está ejecutando directamente
if __name__ == "__main__":
    # Si es así llama a la función principal que inicia el sistema de la biblioteca
    main()