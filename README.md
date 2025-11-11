
##  Objetivos
Implementar un sistema funcional de autenticación con conexión a dos bases de datos.  
Aplicar el uso de contraseñas cifradas con bcrypt.  
Registrar todas las actividades de inicio y acciones de usuario.  
Manejar roles de acceso (usuario y administrador).  
Documentar el diseño, resultados y conclusiones.



## Arquitectura y diseño


Módulo | Descripción 

`config_conexiones.py` - Maneja las conexiones a MySQL y MongoDB. 
`seguridad_utils.py` - Realiza el hashing y validaciones de contraseñas. 
`gestion_usuarios.py` - Contiene las funciones de registro, login, edición y logs. 
`sistema_autenticacion.py` - Controla el flujo del sistema y los menús. 

Además, se incluyen los archivos:
`sql_sistema_examen.sql`  creación de la base de datos MySQL.  
`mongo_setup.txt` creación de colecciones en MongoDB.  
`requirements.txt`  librerías necesarias.  



##  Bases de datos

### MySQL
Base de datos: **sistema_examen**  
Tabla: **usuarios**  
Contiene campos para `username`, `email`, `password_hash`, `rol`, `activo`, `fecha_registro`.

### MongoDB Atlas
Base de datos: **examen_autenticacion**  
Colecciones:
`usuarios`: espejo de los usuarios registrados.  
`logs_login`: guarda todos los eventos del sistema (login, registro, cambios, etc.).



## Funcionalidades desarrolladas

1. **Registro de usuario:**  
Inserta los datos en MySQL y en MongoDB con contraseña cifrada.  

2. **Inicio de sesión:**  
Verifica credenciales y registra cada intento (exitoso o fallido) en MongoDB.  

3. **Recuperación de contraseña:**  
Asigna una contraseña temporal “1234” en caso de olvido.  

4. **Edición de perfil:**  
Permite cambiar correo o contraseña actual.  

5. **Logs de actividad:**  
Muestra el historial de acciones del usuario conectado.  

6. **Rol administrador:**  
Permite listar todos los usuarios existentes en la base MySQL.



## Pruebas realizadas

Prueba - Resultado 

Registro de usuario válido - Usuario guardado en MySQL y MongoDB. 
Inicio de sesión correcto - Acceso concedido, log “login_exitoso”. 
Inicio de sesión incorrecto - Mensaje de error y log “login_fallido”. 
Recuperar contraseña - Clave temporal generada y guardada. 
Editar perfil - Cambios aplicados en la base de datos. 



##  Capturas de evidencia
Las capturas que muestran los resultados del sistema se encuentran en la carpeta `/evidencias`:
MySQL con tabla `usuarios`.  
MongoDB con logs registrados.  
Consola del programa mostrando las operaciones principales.



##  Decisiones de diseño
Se usó una arquitectura modular con 4 archivos para mantener el código ordenado.  
MySQL se usa para datos estructurados, y MongoDB para registros dinámicos.  
Se implementó `bcrypt` para evitar contraseñas planas.  
Se agregaron validaciones básicas en todos los formularios.  
Se simplificó el código para mantenerlo entendible y funcional.




