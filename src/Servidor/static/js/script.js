function acceder() {
    var id = document.getElementById("id").value;
    var contrasena = document.getElementById("contrasena").value;
    var formularioInicioSesion = document.getElementById("formulario-inicio-sesion");
    var formularioAgregar = document.getElementById("formulario-agregar");

    // Mostrar el formulario de agregar usuario solo si el ID y la contraseña son "admin"
    if (id === "admin" && contrasena === "admin") {
        formularioInicioSesion.style.display = "none";
        formularioAgregar.style.display = "block";
    }
}

// Función para alternar la visibilidad del formulario de inicio de sesión
function toggleLoginForm() {
    var formulario = document.getElementById("formulario-inicio-sesion");
    formulario.style.display = (formulario.style.display === "none" || formulario.style.display === "") ? "block" : "none";
}

// Función para realizar el inicio de sesión
function login() {
    // Aquí puedes realizar la autenticación del usuario
    // Si la autenticación es exitosa, puedes guardar el estado del inicio de sesión en una cookie
    document.cookie = "logged_in=true; path=/";
    updateLoginStatus();
    // Mostrar el formulario de agregar después de iniciar sesión
    document.getElementById("formulario-agregar").style.display = "block";
}

// Función para realizar el cierre de sesión
function logout() {
    // Aquí puedes eliminar la cookie que indica el estado del inicio de sesión
    document.cookie = "logged_in=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    updateLoginStatus();
    // Ocultar el formulario de agregar después de cerrar sesión
    document.getElementById("formulario-agregar").style.display = "none";
}

// Función para actualizar el estado del inicio de sesión
function updateLoginStatus() {
    var loginButton = document.querySelector(".login-button");
    var loginStatus = document.getElementById("login-status");
    var logoutButton = document.getElementById("logout-button");

    var loggedIn = getCookie("logged_in");

    if (loggedIn) {
        loginButton.style.display = "none";
        loginStatus.innerText = "Bienvenido"; // Cambiar el texto según sea necesario
        logoutButton.style.display = "block";
    } else {
        loginButton.style.display = "block";
        loginStatus.innerText = "Iniciar Sesión";
        logoutButton.style.display = "none";
    }
}

// Función para obtener el valor de una cookie
function getCookie(name) {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }
    return "";
}

// Al cargar la página, actualiza el estado del inicio de sesión
updateLoginStatus();


// Función para inicializar la conexión SSE y manejar los eventos recibidos
function iniciarSSE() {
    const eventoSource = new EventSource('/actualizar_usuarios_conectados');
    eventoSource.onmessage = function(evento) {
        const datos = JSON.parse(evento.data);
        // Aquí actualizas las tablas con los nuevos datos recibidos
        // Por ejemplo:
        actualizarTablaUsuariosConectados(datos);
       // actualizarTablaUsuarios(datos);
    };
}

// Función para actualizar la tabla de usuarios conectados
function actualizarTablaUsuariosConectados(datos) {
    const tablaUsuariosConectados = document.getElementById("tabla-usuarios-conectados");
    // Limpiar la tabla antes de actualizar con los nuevos datos
    tablaUsuariosConectados.innerHTML = '';
    // Llenar la tabla con los nuevos datos
    datos.forEach(function(usuario) {
        const fila = document.createElement("tr");
        const celdaMAC = document.createElement("td");
        celdaMAC.textContent = usuario.MAC;
        fila.appendChild(celdaMAC);
        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = usuario.Nombre;
        fila.appendChild(celdaNombre);
        const celdaUbicacion = document.createElement("td");
        if(usuario.Ubicacion == "0x0026"){ 
            celdaUbicacion.textContent = "Xpeak 1"
        }else if(usuario.Ubicacion == "0x0027"){
            celdaUbicacion.textContent = "Xpeak 2"
        }else if(usuario.Ubicacion == "0x0028"){
            celdaUbicacion.textContent = "Xpeak 3"
        }
        //celdaUbicacion.textContent = usuario.Ubicacion;
       // if(celdaUbicacion == "0x0027"){ celdaUbicacion = "Xpeak 1"}
        fila.appendChild(celdaUbicacion);
        const celdaUbiUni= document.createElement("td");
        celdaUbiUni.textContent = usuario.Ubicacion;
        fila.appendChild(celdaUbiUni);
        const celdaRSSI = document.createElement("td");
        celdaRSSI.textContent = usuario.RSSI + " dBm";
        fila.appendChild(celdaRSSI);
        tablaUsuariosConectados.appendChild(fila);
    });
}

/*function actualizarTablaUsuarios(datos) {
    const tablaUsuariosSinUbicacion = document.getElementById("tabla-usuarios-registrados");
    // Limpiar la tabla antes de actualizar con los nuevos datos
    tablaUsuariosSinUbicacion.innerHTML = '';
    // Llenar la tabla con los nuevos datos
    datos.forEach(function(usuario) {
        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = usuario.Nombre;
        fila.appendChild(celdaNombre);
        tablaUsuariosSinUbicacion.appendChild(fila);
    });
}
*/
// Llamar a la función para iniciar la conexión SSE cuando la página se cargue
window.onload = iniciarSSE;

