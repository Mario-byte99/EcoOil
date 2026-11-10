import streamlit as st
from supabase import create_client, Client

# --------------------------
# 🔑 CONFIGURACIÓN DE SUPABASE
# --------------------------
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------
# 👤 ADMINISTRADORES
# --------------------------
ADMIN_CORREOS = {
    "chalquenomario18@gmail.com": "3312",
    "josedejesuspalenciaramirez2@gmail.com": "2006",
    "asc720613@gmail.com": "1234",
    "tatisaguilarmtz@gmail.com": "4567"
}

# --------------------------
# ✅ INICIALIZAR VARIABLES DE SESIÓN
# --------------------------
if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "inicio"

# --------------------------
# 🔐 FUNCIONES DE AUTENTICACIÓN
# --------------------------
def registrar_usuario(correo, contrasena, nombre_usuario=""):
    try:
        respuesta = supabase.table("usuarios").select("*").eq("correo", correo).execute()
        if respuesta.data:
            return False, "⚠️ Este correo ya está registrado"
        
        datos = {
            "correo": correo,
            "contrasena": contrasena,
            "nombre_usuario": nombre_usuario
        }
        supabase.table("usuarios").insert(datos).execute()
        return True, "✅ Registro exitoso. Ahora puedes iniciar sesión"
    except Exception as e:
        return False, f"❌ Error al registrar: {str(e)}"


def iniciar_sesion_usuario(correo, contrasena):
    try:
        respuesta = supabase.table("usuarios").select("*").eq("correo", correo).execute()
        
        if not respuesta.data:
            return None, "❌ Correo no encontrado"
        
        usuario = respuesta.data[0]
        
        if usuario.get("contrasena") == contrasena:
            return usuario, f"✅ Bienvenido, {usuario['nombre_usuario']}!"
        else:
            return None, "❌ Contraseña incorrecta"
            
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


def actualizar_datos_usuario(correo_actual, nuevos_datos):
    try:
        supabase.table("usuarios").update(nuevos_datos).eq("correo", correo_actual).execute()
        return True, "✅ Datos actualizados correctamente"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def guardar_solicitud_recoleccion(datos):
    try:
        supabase.table("historial_recoleccion").insert(datos).execute()
        return True, "✅ Solicitud enviada correctamente"
    except Exception as e:
        return False, f"❌ Error al guardar: {str(e)}"

# --------------------------
# 📱 BARRA LATERAL Y MENÚ
# --------------------------
if st.session_state.usuario:
    correo_usuario = st.session_state.usuario.get("correo", "")
    if correo_usuario in ADMIN_CORREOS:
        menu = st.sidebar.radio("Navegación", [
            "🏠 Inicio",
            "🏢 Datos de la Empresa",
            "⚙️ Administración",
            "🚪 Cerrar Sesión"
        ])
    else:
        menu = st.sidebar.radio("Navegación", [
            "🏠 Inicio",
            "🏢 Datos de la Empresa",
            "✏️ Mis Datos",
            "📦 Mis Solicitudes",
            "📦 Nueva Solicitud",
            "🚪 Cerrar Sesión"
        ])
else:
    menu = st.sidebar.radio("Navegación", [
        "🏠 Inicio",
        "🔑 Iniciar Sesión",
        "📝 Registrarse",
        "🏢 Datos de la Empresa"
    ])

# --------------------------
# 📄 PÁGINAS DE LA APLICACIÓN
# --------------------------

# 🏠 INICIO
if menu == "🏠 Inicio":
    st.title("🌱 Eco-Oil — Recolección de Aceite")
    st.subheader("Cuida el planeta, recicla tu aceite usado")
    
    st.markdown("""
    ### 🟢 Bienvenido a Eco-Oil
    
    Somos una empresa comprometida con el medio ambiente. 
    Recolectamos tu aceite usado y le damos un tratamiento adecuado.
    
    ✅ Contamina menos
    ✅ Cuida el agua y el suelo
    ✅ Recibe un servicio gratuito
    
    > 🔑 Inicia sesión o regístrate para solicitar tu recolección
    """)

# 🔑 INICIAR SESIÓN
elif menu == "🔑 Iniciar Sesión":
    st.title("🔑 Iniciar Sesión")
    
    correo = st.text_input("📧 Correo electrónico")
    contrasena = st.text_input("🔒 Contraseña", type="password")
    
    if st.button("Ingresar"):
        if correo and contrasena:
            usuario, mensaje = iniciar_sesion_usuario(correo, contrasena)
            if usuario:
                st.session_state.usuario = usuario
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)
        else:
            st.warning("⚠️ Completa todos los campos")

# 📝 REGISTRARSE
elif menu == "📝 Registrarse":
    st.title("📝 Crear Cuenta")
    
    nombre = st.text_input("👤 Nombre completo")
    correo = st.text_input("📧 Correo electrónico")
    contrasena = st.text_input("🔒 Contraseña", type="password")
    confirmar = st.text_input("🔒 Confirmar contraseña", type="password")
    
    if st.button("Registrarse"):
        if nombre and correo and contrasena and confirmar:
            if contrasena != confirmar:
                st.error("❌ Las contraseñas no coinciden")
            else:
                ok, mensaje = registrar_usuario(correo, contrasena, nombre)
                if ok:
                    st.success(mensaje)
                    st.info("Ahora ve a 'Iniciar Sesión'")
                else:
                    st.error(mensaje)
        else:
            st.warning("⚠️ Completa todos los campos")

# 🏢 DATOS DE LA EMPRESA
elif menu == "🏢 Datos de la Empresa":
    st.title("🏢 Eco-Oil — Recolección de Aceite")
    
    st.markdown("""
    ### 🌍 Quiénes Somos
    
    **Eco-Oil** es una empresa dedicada a la recolección y tratamiento de aceites usados.
    Contribuimos al cuidado del medio ambiente evitando que aceites contaminantes lleguen a nuestros ríos y suelos.
    
    📍 **Ubicación:** San Luis Potosí, S.L.P.
    📞 **Teléfono:** (444) 123-4567
    📧 **Correo:** cristiancomepolla12@gmail.com
    
    ### 👥 Nuestro Equipo
    - **Mario Chalqueño** — Coordinador de Logística
    - **José de Jesús Palencia** — Jefe de Operaciones
    - **Aracely Sánchez** — Atención a Clientes
    - **Cristian** — Administración
    
    ### 📋 ¿Qué hacemos?
    Recolectamos aceite y lubricante usado de automoviles de forma segura,
    lo procesamos y le damos un destino ecológico.
    """)

# ✏️ MIS DATOS
elif menu == "✏️ Mis Datos":
    if not st.session_state.usuario:
        st.warning("⚠️ Inicia sesión primero")
    else:
        st.title("✏️ Mis Datos")
        
        usuario = st.session_state.usuario
        nombre_actual = usuario.get("nombre_usuario", "")
        correo_actual = usuario.get("correo", "")
        
        nuevo_nombre = st.text_input("👤 Nombre de usuario", value=nombre_actual)
        nuevo_correo = st.text_input("📧 Correo electrónico", value=correo_actual, disabled=True)
        nueva_contrasena = st.text_input("🔒 Nueva contraseña (dejar vacío para no cambiar)", type="password")
        
        if st.button("Guardar Cambios"):
            actualizar = {"nombre_usuario": nuevo_nombre}
            if nueva_contrasena:
                actualizar["contrasena"] = nueva_contrasena
            
            ok, msg = actualizar_datos_usuario(correo_actual, actualizar)
            if ok:
                st.success(msg)
                # Actualizar datos en sesión
                st.session_state.usuario["nombre_usuario"] = nuevo_nombre
            else:
                st.error(msg)

# 📦 NUEVA SOLICITUD DE RECOLECCIÓN
elif menu == "📦 Nueva Solicitud":
    if not st.session_state.usuario:
        st.warning("⚠️ Inicia sesión primero")
    else:
        st.title("📦 Solicitar Recolección")
        
        st.info("Llena los datos para que pasemos a recoger tu aceite")
        
        nombre_taller = st.text_input("🏢 Nombre del Taller / Negocio")
        ubicacion = st.text_area("📍 Dirección completa")
        referencia = st.text_area("🗺️ Referencias para llegar")
        tipo_aceite = st.selectbox("🛢️ Tipo de Aceite", ["Aceite de cocina", "Aceite lubricante", "Otro"])
        litros = st.number_input("Cantidad aproximada en litros", min_value=1, step=1)
        tambos = st.number_input("Cantidad de tambos/envases", min_value=1, step=1)
        fecha = st.date_input("📅 Fecha preferida")
        horario = st.selectbox("⏰ Horario preferido", ["Mañana (9:00-12:00)", "Tarde (12:00-15:00)", "Por la tarde (15:00-18:00)"])
        
        if st.button("✅ Enviar Solicitud"):
            datos = {
                "correo_usuario": st.session_state.usuario["correo"],
                "nombre_usuario": st.session_state.usuario["nombre_usuario"],
                "nombre_taller": nombre_taller,
                "ubicacion": ubicacion,
                "referencia": referencia,
                "tipo_aceite": tipo_aceite,
                "litros": litros,
                "tambos": tambos,
                "fecha": str(fecha),
                "horario": horario,
                "estado": "Pendiente"
            }
            
            ok, msg = guardar_solicitud_recoleccion(datos)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

# 📦 MIS SOLICITUDES
elif menu == "📦 Mis Solicitudes":
    if not st.session_state.usuario:
        st.warning("⚠️ Inicia sesión primero")
    else:
        st.title("📦 Mis Solicitudes")
        
        try:
            correo = st.session_state.usuario["correo"]
            respuesta = supabase.table("historial_recoleccion").select("*").eq("correo_usuario", correo).execute()
            
            if respuesta.data:
                for solicitud in respuesta.data:
                    st.subheader(f"📅 {solicitud.get('fecha', 'Sin fecha')}")
                    st.write(f"**Lugar:** {solicitud.get('nombre_taller', '')}")
                    st.write(f"**Ubicacion:** {solicitud.get('ubicacion', '')}")
                    st.write(f"**Aceite:** {solicitud.get('tipo_aceite', '')} — {solicitud.get('litros', 0)} litros")
                    st.write(f"**Estado:** {solicitud.get('estado', 'Pendiente')}")
                    st.divider()
            else:
                st.info("📋 No tienes solicitudes registradas aún")
        except Exception as e:
            st.error(f"Error al cargar solicitudes: {str(e)}")

# ⚙️ ADMINISTRACIÓN
elif menu == "⚙️ Administración":
    correo_usuario = st.session_state.usuario.get("correo", "")
    if correo_usuario not in ADMIN_CORREOS:
        st.error("❌ No tienes permiso para acceder a esta página")
    else:
        st.title("⚙️ Panel de Administración")
        st.success(f"👋 Bienvenido Administrador — {nombre_usuario}")
        
        tab1, tab2 = st.tabs(["📋 Solicitudes de Recolección", "👥 Usuarios Registrados"])
        
        with tab1:
            st.subheader("Solicitudes Pendientes")
            try:
                respuesta = supabase.table("historial_recoleccion").select("*").execute()
                if respuesta.data:
                    st.table(respuesta.data)
                else:
                    st.info("No hay solicitudes registradas")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tab2:
            st.subheader("Lista de Usuarios")
            try:
                respuesta = supabase.table("usuarios").select("*").execute()
                if respuesta.data:
                    st.table(respuesta.data)
                else:
                    st.info("No hay usuarios registrados")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# 🚪 CERRAR SESIÓN
elif menu == "🚪 Cerrar Sesión":
    st.session_state.usuario = None
    st.success("✅ Sesión cerrada correctamente")
    st.rerun()
