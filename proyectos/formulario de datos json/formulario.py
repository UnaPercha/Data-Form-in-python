import json # librería pra trabajar con archivos json
import tkinter as tk # librería pra trabajar con interfaces gráficas
import re # librería de expresiones regulares



#Clase en la que se creará todo el programa
class DataFormApp:
    def __init__(self):
        #-----------Root-------------------
        self.root = tk.Tk()
        self.root.title("Data form")
        
        #-----------Frame-------------------
        self.frame = tk.Frame(self.root, width=800, height=600)
        self.frame.pack(fill = "both" , expand=True)
        
        #----------variables json------------
        self.usersjson = {'users': []}
        self.users_list = []
        
        # Inicializar el menú
        self.Initialize_start_menu() 

    # Esta funcion se encarga de inicializar el menú
    def Initialize_start_menu(self):
        # Botón que te lleva al menú sing in
        singin_button = tk.Button(self.frame, text = "Sing in")
        singin_button.config(width=15, height=15, command=lambda: self.Singin_menu())
        singin_button.grid(column=0, row=0)
        # Botón que te lleva al menú log in
        login_button = tk.Button(self.frame, text = "Log in")
        login_button.config(width=15, height=15, command=lambda: self.Login_menu())
        login_button.grid(column=1, row=0)

    # Botón para poder ver de nuevo el menú de log in y sing in
    def Return_to_start(self):
        # bucle que itera los frames hijos del frame principal(los widgets)
        for widget in self.frame.winfo_children():
            # se encarga de destruir los widgets
            widget.destroy()
        # inicializa el menú de nuevo
        self.Initialize_start_menu()

    # Función que se encarga de obtener en formato lectura el documento json
    def Get_documentation(self, option):
        #si el botón apretado ha sido sing in hará lo siguiente
        if option == 'singin':
            # intentará
            try:
                # abrir el documento.json en formato lectura como d
                with open('documentation.json', 'r', encoding="utf-8") as d:
                    # y lo guardará en la variable self.usersjson
                    self.usersjson = json.load(d)
            # si no puede abrir el documento porque el json no ha sido creado
            except FileNotFoundError:
                # guardará en self.usersjson un diccionario con una lista dentro
                self.users = {'users': []}
        # en cambio, si ha elegido log in
        else:
            # abrirá el documento.json como d
            with open('documentation.json', 'r', encoding="utf-8") as d:
                #y guardará la información en self.users_list
                self.users_list = json.load(d)['users']

    # Esta funcion se encarga de quitar todo el texto innecessario para que no se sobre ponga otro texto por encima
    def Destroy_unnecessary_text(self):
        # Bucle que itera los frames hijos(widgets)
        for widget in self.frame.winfo_children():
            # y si los widgets pertenecen a la clase tk.Label y contienen "Congratulations", "Incorrect password or username", "There are unfilled fileds"
            if isinstance(widget, tk.Label) and widget.cget("text") in ["Congratulations", "Incorrect password or username","There are unfilled fields"]:
                # los quitará
                widget.destroy()

        # Este método se encarga de enviar los datos a el archivo json
    def Upload_to_json(self, name_value, lastname_value, age_value, username_value, email_value, password_value):
        # Llama al método self.Get_documentation() y le indica que trabaje como singin
        self.Get_documentation('singin')
        # Destruye el texto innecesario
        self.Destroy_unnecessary_text()
        # Le manda la información necesaria al método self.Create_user_entrys() para que cree un nuevo usuario
        self.Create_user_entrys(name_value, lastname_value, age_value, username_value, email_value, password_value)
        
        # Se la manda a self.Confirmation() para que imprima el mensaje correspondiente
        if self.Check_email(email_value):
            self.Confirmation('confirmation')

            # Por último abre el archivo json en formato de escritura como d
            with open('documentation.json', 'w', encoding="utf-8") as d:
                # y vuelca la información de la lista documentation en el archivo json con un indentado de 4 para que sea legible
                json.dump(self.usersjson, d, indent=4)
        else:
            self.Confirmation('invalid email')

    # Esta función se encarga de guardar en una variable el diccionario de el nuevo usuario
    def Create_user_entrys(self, name_value, lastname_value, age_value, username_value, email_value, password_value):
        # intentará
        try:
            # guardar los datos del usuario dentro de un diccionario en una variable
            new_user = {
                    'name': name_value,
                    'lastname': lastname_value,
                    'age': int(age_value),
                    'username': username_value,
                    'email': email_value,
                    'password': password_value
                }
            # y agregará dicha variable a la lista self.usersjson
            self.usersjson['users'].append(new_user)
        # Si alguno de los datos pasados no son válidos como una edad en números
        except ValueError:
            # Llama a el método self.Confirmation() para imprimir el mensaje correspondiente
            self.Confirmation('data error')

    # Este método se encarga de crear los mensajes correspondientes para cada caso
    def Confirmation(self, message, username=None):
        # Si el caso es confirmation
        if message == 'confirmation':
            # Creará el siguiente Label
            confirmation = tk.Label(self.frame, text="You have singed up correctly")
            confirmation.grid(row=8,columnspan=3, pady= 10, padx= 10)
        # Si el caso es congratulations
        elif message == 'congratulations':
            # Creará el siguiente Label
            congratulations = tk.Label(self.frame, text=f"Congratulations, {username} loged in correctly!")
            congratulations.grid(row=4, columnspan=2)
        # Si el caso es wrong pass
        elif message == 'wrong pass':
            # Creará el siguiente Label
            wrong_password = tk.Label(self.frame, text="Incorrect password or username, please try again")
            wrong_password.grid(row=4, columnspan=2)
        # Si el caso es invalid email
        elif message == 'invalid email':
            # Creará el siguiente Label
            invalid_email = tk.Label(self.frame, text="This email is invalid")
            invalid_email.grid(row=4, column=2, pady= 10, padx= 10)
        # Si el caso es data_error
        else:
            # Creará el siguiente Label
            data_error = tk.Label(self.frame, text="There are unfilled fields")
            data_error.grid(row=8,columnspan=3, pady= 10, padx= 10)

    # Método que se encarga de decir si el email es válido
    def Check_email(self, email):
        # Crea una variable con la expresión regular necesaria para comprobar si es un email
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        # Devuelve True si ha confirmado que el email es válido
        return re.match(expresion_regular, email) is not None

    # Método que comprueba los datos ingresados para reconocer al usuario
    def Check_login(self, username_value, password_value):
        # Llama a Get_documentation() a que actue como login
        self.Get_documentation('login')
        
        # Elimina el texto innecesario en caso de que lo haya
        self.Destroy_unnecessary_text()
        
        # Crea una variable login_succesful y le da el valor de Flase
        login_succesful = False
        # Crea otra variable login_username y le da una cadena vacía
        login_username = ""
        # Este bucle itera la lista que ha recogido self.Get_documentation()
        for i in self.users_list:
            # Si el nombre de usuario y la contraseña recogidas son iguales a las ingresadas
            if (i['username'] == username_value and i["password"] == password_value):
                # Establece login_succesful a True
                login_succesful = True
                # login_username le guarda el nombre de usuario
                login_username = i['username']
                # y rompe el bucle 
                break
        # Si login_succesful es True
        if login_succesful:
            # le pasa al método self.Confirmation() que imprima el mensaje congratulations con el nombre guardado en login_username
            self.Confirmation('congratulations', username=login_username)
        else:
            # en cambio si es False llamará al método self.Confirmation() que imprima el mensaje de worng pass
            self.Confirmation('wrong pass')

    # Esta funcion se encarga de mostrar la contraseña
    def Show_password(self, square_pass, show_activate):
        # Si el botón por el que se pasa la variable está encendido
        if show_activate.get() == True:
            # Mostrará la contraseña
            square_pass.configure(show='')
        # Si no
        else:
            # Pues no
            square_pass.config(show="•")

    # Esta funcion se encarga de imprimir el menú se Sing in
    def Singin_menu(self):
        # Destruye el frame anterior
        self.frame.destroy()
        # Crea uno nuevo
        self.frame = tk.Frame(self.root, width=800, height=600)
        self.frame.pack(fill="both", expand=True)
        
        # Crea un texto nombre
        name_label = tk.Label(self.frame, text="Name:")
        name_label.grid(row=0, column=0, sticky=("e"), pady= 10, padx= 10)

        # y su respectivo cuadro de texto
        square_name = tk.Entry(self.frame)
        square_name.grid(row=0, column=1, pady= 10, padx= 10)

        # Crea un cuadro de apellido
        lastname_label = tk.Label(self.frame, text="Lastname:")
        lastname_label.grid(row=1, column=0, sticky=("e"), pady= 10, padx= 10)

        # y su respectivo cuadro de texto
        square_lastname = tk.Entry(self.frame)
        square_lastname.grid(row=1, column=1, pady= 10, padx= 10)
        
        # Crea un texto de edad
        age_label = tk.Label(self.frame, text="Age:")
        age_label.grid(row=2, column=0, sticky=("e"), pady= 10, padx= 10)

        # y su respectivo cuadro de texto
        square_age = tk.Entry(self.frame)
        square_age.grid(row=2, column=1, pady= 10, padx= 10)

        # Crea un texto de username
        name_username = tk.Label(self.frame, text="Username:")
        name_username.grid(row=3, column=0, sticky=("e"), pady= 10, padx= 10)

        # y su respectivo cuadro de texto
        square_username = tk.Entry(self.frame)
        square_username.grid(row=3, column=1, pady= 10, padx= 10)

        # Crea un texto de email
        email_label = tk.Label(self.frame, text="Email:")
        email_label.grid(row=4, column=0, sticky=("e"), pady= 10, padx= 10)

        # y su respectivo cuadro de texto
        square_email = tk.Entry(self.frame)
        square_email.grid(row=4, column=1, pady= 10, padx= 10)

        # Crea un texto de contraseña
        pass_label = tk.Label(self.frame, text="Password:")
        pass_label.grid(row=5, column=0, sticky=("e"), pady= 10, padx= 10)

        # y su respectivo cuadro de texto
        square_pass = tk.Entry(self.frame, show="•")
        square_pass.grid(row=5, column=1, pady= 10, padx= 10)

        # Crea una variable booleana 
        show_activate = tk.BooleanVar()

        # Crea el botón para poder ver la contraseña y le pasa la variable booleana que se pondrá True cuando se clicke
        show_pass = tk.Checkbutton(self.frame, text="Show Password", variable=show_activate)
        show_pass.grid(row=5, column=2, pady= 10, padx= 10)
        # y se le establece el método correspondiente
        show_pass.config(command=lambda: self.Show_password(square_pass, show_activate))

        # Crea un botón para poder ver de nuevo el menú de seleccion y se le pasa el método self.Return_to_start
        return_button = tk.Button(self.frame, text="Return", command= self.Return_to_start)
        return_button.grid(row=7,columnspan=3, pady= 10, padx= 10)

        # Crea un botón de finalizar
        finish_button = tk.Button(self.frame, text="Finalized")
        finish_button.grid(row=6, columnspan=3, pady= 10, padx= 10)
        # Y le pasa el método self.Upload_to_json(con los cuadros de texto)
        finish_button.config(command=lambda: self.Upload_to_json
                                                            (
                                                            square_name.get(),
                                                            square_lastname.get(),
                                                            square_age.get(),
                                                            square_username.get(),
                                                            square_email.get(),
                                                            square_pass.get()
                                                            )
                            )

    # Este método se encarga de crear el menú de log in
    def Login_menu(self):
        # Quita el menú anterior
        self.frame.destroy()
        # Crea un nuevo frame
        self.frame = tk.Frame(self.root, width=800, height=600)
        self.frame.pack(fill="both", expand=True)

        # Crea un texto nombre
        name_username = tk.Label(self.frame, text="Username:")
        name_username.grid(row=0, column=0, sticky=("e"), pady= 10, padx= 10)

        # y su respectivo cuadro de texto
        square_username = tk.Entry(self.frame)
        square_username.grid(row=0, column=1, pady= 10, padx= 10)

        # Crea un texto contraseña
        pass_label = tk.Label(self.frame, text="Password:")
        pass_label.grid(row=1, column=0, sticky=("e"), pady= 10, padx= 10)

        # y su respectivo cuadro de texto
        square_pass = tk.Entry(self.frame)
        square_pass.grid(row=1, column=1, pady= 10, padx= 10)
        square_pass.config(show="•")
        
        # Crea una variable booleana 
        show_activate = tk.BooleanVar()

        # Crea el botón para poder ver la contraseña y le pasa la variable booleana que se pondrá True cuando se clicke
        show_pass = tk.Checkbutton(self.frame, text="Show Password", variable=show_activate)
        show_pass.grid(row=1, column=2, pady= 10, padx= 10)
        # y se le establece el método correspondiente
        show_pass.config(command=lambda: self.Show_password(square_pass, show_activate))

        # Crea un botón para poder ver de nuevo el menú de seleccion y se le pasa el método self.Return_to_start
        return_button = tk.Button(self.frame, text="Return", command=self.Return_to_start)
        return_button.grid(row=3, columnspan=3, pady= 10, padx= 10)

        # Crea un botón de finalizar y le pasa la función self.Check_login con los parametros square_username y square_pass
        finish_button = tk.Button(self.frame, text="Finalized", command=lambda: self.Check_login(square_username.get(), square_pass.get()))
        finish_button.grid(row=2, columnspan=3, pady= 10, padx= 10)

    # Función que ejecuta el programa
    def Run(self):
        self.root.mainloop()


# Comprueba si el programa se está ejecutando desde el programa y no como módulo
if __name__ == '__main__':
    # Instancia un objeto de la clase DataFormApp()
    app = DataFormApp()
    # y llama la función Run()
    app.Run()