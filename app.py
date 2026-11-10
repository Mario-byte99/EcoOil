import streamlit as st
from supabase import create_client, Client

# ==================== CONFIGURACIÓN ====================
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

def init_supabase():
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

supabase = init_supabase()

ADMIN_CORREOS = {
    "chalquenomario18@gmail.com": "3312",
    "josedejesuspalenciaramirez2@gmail.com": "2006",
    "asc720613@gmail.com": "1234",
    "tatisaguilarmtz@gmail.com": "4567"
}

# ==================== FUNCIONES ====================
def registrar_usuario(nombre_usuario, correo, contrasena):
    try:
        supabase.table("usuarios").insert({
            "nombre_usuario": nombre_usuario,
            "correo": correo,
            "contrasena": contrasena
        }).execute()
        return True
    except:
        return False

def iniciar_sesion_usuario(correo, contrasena):
    try:
        respuesta = supabase.table("usuarios").select("*").eq("correo", correo).execute()
        if  not respuesta.data:
            return None, "Correo no encontrado"
            usuario = respuesta.data(0)
        if usuario.get("contrasena") == contrasena:
            return usuario, "Bienvenido, " + usuario["Nombre_usuario"] + "!"
        else: 
            return None, "Contraseña incorrecta"
    except Exception as e:
        return None, f"Error: {str(e)}"

def actualizar_datos_usuario(usuario_id, nombre_taller, ubicacion, litros, tambos):
    supabase.table("usuarios").update({
        "nombre_taller": nombre_taller,
        "ubicacion": ubicacion,
        "litros_aceite": litros,
        "cantidad_tambos": tambos,
        "datos_completos": True
    }).eq("id", usuario_id).execute()

def obtener_datos_usuario(usuario_id):
    respuesta = supabase.table("usuarios").select("*").eq("id", usuario_id).execute()
    return respuesta.data[0] if respuesta.data else None

def obtener_todos_usuarios():
    respuesta = supabase.table("usuarios").select("*").execute()
    return respuesta.data if respuesta.data else []

# ==================== INTERFAZ WEB ====================
st.set_page_config(page_title="Eco-Oil", page_icon="🌿", layout="wide")

# --- Inicializar sesión ---
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "inicio"

# --- Barra lateral personalizada según sesión ---
if st.session_state.usuario:
    if st.session_state.usuario["correo"] in ADMIN_CORREOS:
        menu = st.sidebar.radio("Navegación", [
            "🏠 Inicio",
            "🏢 Datos de la Empresa",
            "✏️ Mis Datos",
            "👥 Administración"
        ])
    else:
        menu = st.sidebar.radio("Navegación", [
            "🏠 Inicio",
            "🏢 Datos de la Empresa",
            "✏️ Mis Datos"
        ])
else:
    menu = st.sidebar.radio("Navegación", [
        "🏠 Inicio",
        "🔐 Iniciar Sesión",
        "📝 Registrarse"
    ])

st.sidebar.write("---")
st.sidebar.markdown("<h3 style='text-align: center; color: #2d7d32;'>🌿 Eco-Oil</h3>", unsafe_allow_html=True)

# ==================== PÁGINAS ====================

# --- 🏠 INICIO ---
if menu == "🏠 Inicio":
    st.markdown("<h1 style='text-align: center; color: #2d7d32;'>🌿 Eco-Oil</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Sistema de Recolección de Aceite Vegetal</h3>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("♻️ Bienvenido")
        st.write("Eco-Oil es un proyecto dedicado a la recolección y reciclaje de aceite vegetal usado. ¡Cuida el planeta con nosotros!")
        st.write("🔹 Registra los datos de tu taller")
        st.write("🔹 Indica la cantidad de aceite disponible")
        st.write("🔹 Nosotros vamos por ti")
        st.write("📍 San Luis Potosí, S.L.P.")
    
    with col2:
        st.image("https://images.unsplash.com/photo-1532996122724-e4b4938ff3e5?w=500", caption="Protejamos nuestro planeta 🌍")
    
    if not st.session_state.usuario:
        st.info("👈 Inicia sesión o regístrate en el menú lateral")

# --- 🔐 INICIAR SESIÓN ---
elif menu == "🔐 Iniciar Sesión":
    st.markdown("<h2 style='text-align: center;'>🔐 Iniciar Sesión</h2>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1497435307147-9e53b114c9ee?w=300", use_container_width=True)
        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")
        
        if st.button("🔑 Ingresar", use_container_width=True):
            usuario = iniciar_sesion_usuario(correo, contrasena)
            if usuario:
                st.session_state.usuario = usuario
                st.rerun()
            else:
                st.error("❌ Correo o contraseña incorrectos")

# --- 📝 REGISTRARSE ---
elif menu == "📝 Registrarse":
    st.markdown("<h2 style='text-align: center;'>📝 Crear Cuenta</h2>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        nombre_usuario = st.text_input("Nombre de usuario")
        correo = st.text_input("Correo electrónico")
        contrasena = st.text_input("Contraseña", type="password")
        confirmar = st.text_input("Confirmar contraseña", type="password")
        
        if st.button("✅ Registrarse", use_container_width=True):
            if contrasena == confirmar and nombre_usuario and correo:
                if registrar_usuario(nombre_usuario, correo, contrasena):
                    st.success("✅ ¡Cuenta creada! Ahora inicia sesión")
                else:
                    st.error("❌ Este correo o usuario ya está registrado")
            else:
                st.warning("⚠️ Verifica los datos")

# --- ✏️ MIS DATOS (Usuario completa/modifica su información) ---
elif menu == "✏️ Mis Datos":
    usuario = st.session_state.usuario
    if not usuario:
        st.warning("⚠️ Inicia sesión primero")
    else:
        st.markdown("<h2 style='text-align: center;'>✏️ Mis Datos</h2>", unsafe_allow_html=True)
        st.write("---")
        
        datos_actuales = obtener_datos_usuario(usuario["id"])
        if datos_actuales and datos_actuales.get("datos_completos"):
            st.info("Puedes actualizar tu información cuando lo necesites 👇")
        
        with st.form("form_datos_taller"):
            st.subheader("🏢 Datos del Taller")
            nombre_taller = st.text_input("Nombre del taller", 
                                         value=datos_actuales.get("nombre_taller", "") if datos_actuales else "")
            ubicacion = st.text_input("Ubicación (Dirección completa)",
                                     value=datos_actuales.get("ubicacion", "") if datos_actuales else "")
            
            st.subheader("🛢️ Información de Recolección")
            litros = st.number_input("Cantidad de litros de aceite disponibles", 
                                    min_value=0.0, step=1.0,
                                    value=float(datos_actuales.get("litros_aceite", 0)) if datos_actuales else 0.0)
            tambos = st.number_input("Cantidad de tambos a recolectar", 
                                    min_value=0, step=1,
                                    value=int(datos_actuales.get("cantidad_tambos", 0)) if datos_actuales else 0)
            
            if st.form_submit_button("💾 Guardar Cambios", use_container_width=True):
                if nombre_taller and ubicacion:
                    actualizar_datos_usuario(usuario["id"], nombre_taller, ubicacion, litros, tambos)
                    st.success("✅ ¡Datos guardados correctamente!")
                    st.rerun()
                else:
                    st.warning("⚠️ Completa nombre del taller y ubicación")

# --- 🏢 DATOS DE LA EMPRESA ---
elif menu == "🏢 Datos de la Empresa":
    st.markdown("<h2 style='text-align: center;'>🏢 Conoce a Eco-Oil</h2>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://images.unsplash.com/photo-153813578502c-d7502c0a49f0?w=250", caption="Eco-Oil 🌿")
    
    with col2:
        st.subheader("♻️ ¿Quiénes somos?")
        st.write("""
        *Eco-Oil* es una empresa comprometida con el medio ambiente. Nos dedicamos a la recolección 
        profesional de aceite vegetal usado para su tratamiento y reciclaje adecuado.
        
        Nuestra misión es evitar que el aceite llegue a nuestros ríos y drenajes, protegiendo el agua 
        y el ecosistema de San Luis Potosí.
        """)
    
    st.write("---")
    st.subheader("👥 Nuestro Equipo")
    
    personal = [
        {"nombre": "Mario Chalque", "cargo": "Coordinador de Recolección"},
        {"nombre": "José de Jesús Palencia", "cargo": "Jefe de Operaciones"},
        {"nombre": "Alicia Sánchez", "cargo": "Atención a Clientes"},
        {"nombre": "Tania Aguilar", "cargo": "Administración"}
    ]
    
    cols = st.columns(4)
    for i, miembro in enumerate(personal):
        with cols[i]:
            st.markdown(f"""
            <div style='text-align: center; padding: 10px; background-color: #f0f8f0; border-radius: 10px;'>
                <h4>{miembro['nombre']}</h4>
                <p style='color: #555;'>{miembro['cargo']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.write("---")
    st.info("📍 Estamos en San Luis Potosí, S.L.P. 🇲🇽 | 📧 contacto@eco-oil.mx")

# --- 👥 PANEL DE ADMINISTRACIÓN ---
elif menu == "👥 Administración":
    if not st.session_state.usuario or st.session_state.usuario["correo"] not in ADMIN_CORREOS:
        st.warning("⚠️ Solo administradores")
    else:
        st.markdown("<h2 style='text-align: center;'>👥 Panel de Administración</h2>", unsafe_allow_html=True)
        st.write("---")
        
        usuarios = obtener_todos_usuarios()
        if usuarios:
            st.subheader("📋 Datos Registrados de Talleres")
            
            datos_tabla = []
            for u in usuarios:
                datos_tabla.append({
                    "Usuario": u.get("nombre_usuario", ""),
                    "Correo": u.get("correo", ""),
                    "Nombre del Taller": u.get("nombre_taller", "---"),
                    "Ubicación": u.get("ubicacion", "---"),
                    "Litros Disponibles": u.get("litros_aceite", 0),
                    "Tambos": u.get("cantidad_tambos", 0)
                })
            
            st.table(datos_tabla)
            
            total_litros = sum(u.get("litros_aceite", 0) for u in usuarios)
            total_tambos = sum(u.get("cantidad_tambos", 0) for u in usuarios)
            
            col1, col2 = st.columns(2)
            col1.metric("🛢️ Total Litros Reportados", f"{total_litros:.2f} L")
            col2.metric("📦 Total Tambos", total_tambos)
        else:
            st.info("📂 Aún no hay usuarios registrados")

# --- Cerrar sesión ---
if st.session_state.usuario:
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.usuario = None
        st.rerun()
