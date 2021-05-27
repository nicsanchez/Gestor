from django.shortcuts import render,redirect
from .models import Usuario
from .models import Noticia
from create.models import coordinadores,Integrante,Participante2,Rol,Semillero,Atributos,categoriaAdyacente,categoriaPrincipal,produccion
from conv.models import Proyectos
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Avg, Max, Min
import os
from subprocess import call

#Controlador encargado de la vista de inicio
def home(request):
    noticias = Noticia.objects.all().order_by('-created')
    layers = Noticia.objects.all().order_by('-created')[:4]

    """ if request.method == "POST":
        title = request.POST['title']
        image = request.POST['image']
        description = request.POST['description']
        content = request.POST['content']

        insert = Noticia(title=title, image=image, description=description, content=content)
        insert.save()
    """

    return render(request, "core/home.html", {'noticias':noticias,'layers':layers})

#Controlador encargado de loguearse en el aplicativo
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            if(request.user.groups.filter(name='Coordinador').exists()):
                coordinador=coordinadores.objects.get(user=request.user)
                integrante=Integrante.objects.get(id=coordinador.Integrante.id)
                rol=Rol.objects.get(name="Coordinador de semillero")
                participante=Participante2.objects.filter(id_integrante=integrante.id,rol=rol)
                if(participante.count()>1):
                    return redirect('/choose')
                else:
                    return redirect('/integrante')
            else:
                return redirect('/proyectos')        
        else:
            return render(request, "core/login.html",{'mensaje':'Usuario y/o contraseña invalidos'})
    return render(request, "core/login.html")

#Controlador encargado de registrar usuarios en el aplicativo
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        name = request.POST['name']
        lastname = request.POST['lastname']
        email = request.POST['email']
        grupo = request.POST['group']
        if " " in username:
            return render(request, "core/sign-up.html", {'mensaje':'El nombre de usuario no puede contener espacios.'})
        elif rpassword == password:
            user = User.objects.create_user(username, email, password)
            group = Group.objects.all().filter(name=grupo)
            user.first_name = name
            user.last_name = lastname
            user.groups.set(group)
            user.save()
            return render(request, "core/sign-up.html")
        else:
            return render(request, "core/sign-up.html", {'mensaje':'Las contraseñas no coinciden.'})
    return render(request, "core/sign-up.html")

#Controlador encargado de generar noticias
def add_news(request):
    if request.method == "POST":
        image = request.FILES['image']
        banner = request.FILES['banner']
        title = request.POST['title']
        description = request.POST['description']
        content = request.POST['content']
        insert = Noticia(title=title, description=description, content=content, image=image, banner=banner)
        insert.save()

    return render(request, "core/add_news.html")

#Controlador encargado de listar noticias
def news(request, id_item=None):
    item = Noticia.objects.get(id=id_item)
    return render(request, "core/news.html",{'item':item,})

#Controlador encargado de la elección de semillero a gestionar por un coordinador que tiene mas de un semillero a cargo
def choose(request):
    coordinador=coordinadores.objects.get(user=request.user)
    integrante=Integrante.objects.get(id=coordinador.Integrante.id)
    rol=Rol.objects.get(name="Coordinador de semillero")
    semilleros=Participante2.objects.filter(id_integrante=integrante.id,rol=rol)
    if request.method=="POST":
        semillero=request.POST["id_semillero"]
        insert=coordinadores.objects.get(user=request.user)
        insert.id_semillero=semillero
        insert.save(update_fields=['id_semillero'])
        return redirect("/integrante")

    return render(request,"core/choose.html",{'semilleros':semilleros})

#Controlador encargado de listar los semilleros en la vista Nuestros Semilleros
def semilleros(request):
    semilleros = Semillero.objects.all()
    return render(request, "core/semilleros.html",{'semilleros':semilleros})

#Controlador encargado de generar las estadisticas
def estadisticas(request):
    semilleros = Semillero.objects.all()
    if request.method == "POST":
        caso = request.POST["query"]
        opcion = request.POST['opcion']
        #Numero de estudiantes de un semillero
        if caso == "0":  
            #Todos los semilleros
            cadenaSemilleros = ""
            cadenaPre = ""
            cadenaPos = ""
            if(opcion == "0"):
                semilleros = Semillero.objects.all()
                rol = Rol.objects.get(name="Estudiante Udea")
                for semillero in semilleros:
                    #Todos los estudiantes que pertenecen al semillero
                    participantes = Participante2.objects.filter(id_semillero=semillero,rol=rol)
                    cantidadPre = 0
                    cantidadPos = 0
                    #Conteo de Estudiantes de pregrado
                    if(len(participantes) > 0):
                        cadenaSemilleros += semillero.name + "&"
                        for participante in participantes:
                            informacion = Atributos.objects.get(id_participante=participante)
                            if(informacion.id_programa.tipo == "Pregrado"):
                                cantidadPre += 1
                            else:
                                cantidadPos += 1        
                        
                        cadenaPre += str(cantidadPre) + ","
                        cadenaPos += str(cantidadPos) + ","
                
                cadenaSemilleros = cadenaSemilleros[:-1]
                cadenaPre = cadenaPre[:-1]
                cadenaPos = cadenaPos[:-1]
                #Total de estudiantes de pregrado UdeA sin duplicados
                #estudiantes = Atributos.objects.filter(id_programa__tipo="Pregrado").order_by("id_estudiante").values("id_estudiante").distinct()
                #cantidad = str(len(estudiantes))
                retorno=os.getcwd()
                os.chdir("./pdf_files/estadisticas/estudiantes")
                generateStudentsReport(cadenaSemilleros,cadenaPre,cadenaPos)
                delete_pdf_files("ReporteEstudiantes")
                os.chdir(retorno)
            
            #Listado de Semilleros
            elif(opcion == "1"):
                contador = int(request.POST['contador'])
                for i in range(1,contador+1):
                    try:   
                        añadido = request.POST['SemilleroAñadido'+str(i)]
                        semillero = Semillero.objects.get(id=int(añadido))
                        rol = Rol.objects.get(name="Estudiante Udea")
                        #Todos los estudiantes que pertenecen al semillero
                        participantes = Participante2.objects.filter(id_semillero=semillero,rol=rol)
                        cantidad = 0
                        #Conteo de Estudiantes de pregrado
                        for participante in participantes:
                            informacion = Atributos.objects.get(id_participante=participante)
                            if(informacion.id_programa.tipo == "Pregrado"):
                                cantidad+=1
                        print("Hay un total de "+str(cantidad)+" estudiantes de pregrado UdeA registrados en el semillero "+semillero.name+".") 
                    except:    
                        pass
        #Numero de estudiantes de Posgrado UdeA                
        #elif caso == "1":
            #Todos los semilleros
        #    if(opcion == "0"):
        #        semilleros = Semillero.objects.all()
        #        rol = Rol.objects.get(name="Estudiante Udea")
        #        for semillero in semilleros:
                    #Todos los estudiantes que pertenecen al semillero
        #            participantes = Participante2.objects.filter(id_semillero=semillero,rol=rol)
        #            cantidad = 0
                    #Conteo de Estudiantes de posgrado
        #            for participante in participantes:
        #                informacion = Atributos.objects.get(id_participante=participante)
        #                if(informacion.id_programa.tipo == "Postgrado"):
        #                    cantidad+=1
        #            print("Hay un total de "+str(cantidad)+" estudiantes de posgrado UdeA registrados en el semillero "+semillero.name+".") 
                #Total de estudiantes de posgrado UdeA sin duplicados
        #        estudiantes = Atributos.objects.filter(id_programa__tipo="Postgrado").order_by("id_estudiante").values("id_estudiante").distinct()
        #        cantidad = str(len(estudiantes))
        #        print("Hay un total de "+cantidad+" estudiantes de posgrado UdeA registrados en la aplicación.") 
            
            #Listado de Semilleros
        #    elif(opcion == "1"):
        #        contador = int(request.POST['contador'])
        #        for i in range(1,contador+1):
        #            try:   
        #                añadido = request.POST['SemilleroAñadido'+str(i)]
        #                semillero = Semillero.objects.get(id=int(añadido))
        #                rol = Rol.objects.get(name="Estudiante Udea")
                        #Todos los estudiantes que pertenecen al semillero
        #                participantes = Participante2.objects.filter(id_semillero=semillero,rol=rol)
        #                cantidad = 0
                        #Conteo de Estudiantes de posgrado
        #                for participante in participantes:
        #                    informacion = Atributos.objects.get(id_participante=participante)
        #                    if(informacion.id_programa.tipo == "Postgrado"):
        #                        cantidad+=1
        #                print("Hay un total de "+str(cantidad)+" estudiantes de posgrado UdeA registrados en el semillero "+semillero.name+".") 
        #            except:    
        #                pass
        #Numero de integrantes de un semillero    
        elif caso == "2":
            #Todos los semilleros
            if(opcion == "0"):
                semilleros = Semillero.objects.all()
                for semillero in semilleros:
                    #Todos los integrantes que pertenecen al semillero
                    integrantes = Participante2.objects.filter(id_semillero=semillero)
                    cantidad = str(len(integrantes))
                    print("Hay un total de "+cantidad+" integrantes registrados al semillero: "+semillero.name+" en la aplicación.") 
            
            #Listado de Semilleros
            elif(opcion == "1"):
                contador = int(request.POST['contador'])
                for i in range(1,contador+1):
                    try:   
                        añadido = request.POST['SemilleroAñadido'+str(i)]
                        semillero = Semillero.objects.get(id=int(añadido))
                        integrantes = Participante2.objects.filter(id_semillero=semillero)
                        cantidad = str(len(integrantes))
                        print("Hay un total de "+cantidad+" integrantes registrados al semillero: "+semillero.name+" en la aplicación.") 
                    except:    
                        pass
        #Numero de articulos de investigacion publicados
        elif caso == "3":
            categoriaArticulo = categoriaAdyacente.objects.get(nombre="Artículos de Investigación publicados en revista indexada, ISI o Scopus")
            #Todos los semilleros
            if(opcion == "0"):
                semilleros = Semillero.objects.all()
                for semillero in semilleros:                
                    producciones = produccion.objects.filter(categoria=categoriaArticulo,semillero=semillero)
                    cantidad=len(producciones)
                    print("Hay un total de "+cantidad+" articulos de investigacion publicados por el semillero: "+semillero.name+" en la aplicación.")
        
            #Listado de Semilleros
            elif(opcion == "1"):
                contador = int(request.POST['contador'])
                for i in range(1,contador+1):
                    añadido = request.POST['SemilleroAñadido'+str(i)]
                    semillero = Semillero.objects.get(id=int(añadido))
                    producciones = produccion.objects.filter(categoria=categoriaArticulo,semillero=semillero)
                    cantidad=len(producciones)
                    print("Hay un total de "+cantidad+" articulos de investigacion publicados por el semillero: "+semillero.name+" en la aplicación.")

        #Numero de capitulos de libros publicados
        elif caso == "4":
            categoriaCapitulo = categoriaAdyacente.objects.get(nombre="Capítulos de libro")
            #Todos los semilleros
            if(opcion == "0"):
                semilleros = Semillero.objects.all()
                for semillero in semilleros:
                    producciones = produccion.objects.filter(categoria=categoriaCapitulo,semillero=semillero)
                    cantidad=len(producciones)
                    print("Hay un total de "+ str(cantidad) +" capítulos de libros publicados por el semillero: "+semillero.name+" en la aplicación.")
        
            #Listado de Semilleros
            elif(opcion == "1"):
                contador = int(request.POST['contador'])
                for i in range(1,contador+1):
                    añadido = request.POST['SemilleroAñadido'+str(i)]
                    semillero = Semillero.objects.get(id=int(añadido))
                    producciones = produccion.objects.filter(categoria=categoriaCapitulo,semillero=semillero)
                    cantidad=len(producciones)
                    print("Hay un total de "+str(cantidad)+" capítulos de libros publicados por el semillero: "+semillero.name+" en la aplicación.")
        
        #Numero de libros de investigación publicados
        elif caso == "5":
            categoriaLibro = categoriaAdyacente.objects.get(nombre="Libros")
            #Todos los semilleros
            if(opcion == "0"):
                semilleros = Semillero.objects.all()
                for semillero in semilleros:
                    producciones = produccion.objects.filter(categoria=categoriaLibro,semillero=semillero)
                    cantidad=len(producciones)
                    print("Hay un total de "+str(cantidad)+" capítulos de libros publicados por el semillero: "+semillero.name+" en la aplicación.")
        
            #Listado de Semilleros
            elif(opcion == "1"):
                contador = int(request.POST['contador'])
                for i in range(1,contador+1):
                    añadido = request.POST['SemilleroAñadido'+str(i)]
                    semillero = Semillero.objects.get(id=int(añadido))
                    producciones = produccion.objects.filter(categoria=categoriaLibro,semillero=semillero)
                    cantidad=len(producciones)
                    print("Hay un total de "+str(cantidad)+" capítulos de libros publicados por el semillero: "+semillero.name+" en la aplicación.") 

        #return render(request, "core/estadisticas.html",{'semilleros':semilleros,'mensaje':mensaje})
        
    return render(request, "core/estadisticas.html",{'semilleros':semilleros})

#Funcion encargada de eliminar los archivos generados por latex en la generacion de pdfs
def delete_pdf_files(name):
    os.remove(name+".aux")
    os.remove(name+".log")
    os.remove(name+".pdf")
    os.remove("vars.tex")

#Funcion encargada de generar el reporte de estudiantes
def generateStudentsReport(semilleros,pregrado,postgrado):
    template="plantilla_vars.tex"
    with open(template,'r') as f:
        archivo=f.read()
    archivo=archivo.replace('semilleros-list',semilleros)
    archivo=archivo.replace('pregrado-students-list',pregrado)
    archivo=archivo.replace('postgrado-students-list',postgrado)

    with open ("vars.tex",'w') as h:
        h.write(archivo)
    d=os.getcwd()
    call("xelatex -jobname=ReporteEstudiantes "+d+"/plantilla.tex",shell=1)    