import streamlit as st
from supabase import create_client, Client

# --------------------------
# 🖼️ CONFIGURACIÓN DE LA PÁGINA
# --------------------------
st.set_page_config(
    page_title="Eco-Oil — Recolección de Aceite",
    page_icon="🌱",
    layout="centered",
    menu_items=None
)

# Código de verificación de Google
st.html("""
<head>
<meta name="google-site-verification" content="EF6SeijiuTcSklEjDiCRLOm4K4ljPgdo4Oi03lx9aEU" /> 
</head>
""")

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

COSTO_POR_TAMBO = 1000

# --------------------------
# ✅ INICIALIZAR VARIABLES DE SESIÓN
# --------------------------
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# --------------------------
# 🔐 FUNCIONES
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
        datos["costo_total"] = datos.get("tambos", 0) * COSTO_POR_TAMBO
        supabase.table("historial_recoleccion").insert(datos).execute()
        return True, "✅ Solicitud enviada correctamente"
    except Exception as e:
        return False, f"❌ Error al guardar: {str(e)}"


def eliminar_pedido(id_pedido):
    try:
        supabase.table("historial_recoleccion").delete().eq("id", id_pedido).execute()
        return True, "✅ Pedido eliminado correctamente"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def cambiar_estado_pedido(id_pedido, nuevo_estado):
    try:
        supabase.table("historial_recoleccion").update({"estado": nuevo_estado}).eq("id", id_pedido).execute()
        if nuevo_estado == "Completado":
            pedido = supabase.table("historial_recoleccion").select("*").eq("id", id_pedido).execute().data[0]
            datos_completado = {
                "numero_pedido": id_pedido,
                "fecha_pedido": pedido.get("fecha"),
                "cantidad_tambos": pedido.get("tambos"),
                "costo_total": pedido.get("tambos", 0) * COSTO_POR_TAMBO
            }
            supabase.table("pedidos_completados").insert(datos_completado).execute()
        return True, f"✅ Estado cambiado a: {nuevo_estado}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def eliminar_usuario(correo_usuario):
    try:
        supabase.table("usuarios").delete().eq("correo", correo_usuario).execute()
        return True, "✅ Usuario eliminado correctamente"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

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
            "📦 Mis Pedidos",
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
# 📄 PÁGINAS
# --------------------------

# 🏠 INICIO
if menu == "🏠 Inicio":
    try:
        st.image("eco-oil-logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌱 Eco-Oil</h1>", unsafe_allow_html=True)
    st.title("🌱 Eco-Oil — Recolección de Aceite")
    st.subheader("Cuida el planeta, recicla tu aceite usado")
    st.info(f"💰 Costo por tambo/envase: **${COSTO_POR_TAMBO:,} MXN**")
    st.markdown("""
    ### 🟢 Bienvenido a Eco-Oil
    
    Somos una empresa comprometida con el medio ambiente. 
    Recolectamos tu aceite usado y le damos un tratamiento adecuado.
    
    ✅ Contamina menos
    ✅ Cuida el agua y el suelo
    ✅ Recibe un servicio a un costo justo
    
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
    st.info(f"💲 Precio por cada tambo: **${COSTO_POR_TAMBO:,} MXN**")
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
    
    📍 **Ubicación:** Villa de Pozos, S.L.P.
    📞 **Teléfono:** (444) 5424 960
    📧 **Correo:** josedejesuspalenciaramirez2@gmail.com
    
    ### 👥 Nuestro Equipo
    - **Mario Chalqueño** — Coordinador de Logística
    - **José de Jesús** — Jefe de Operaciones
    - **Jacqueline** — Directora General
    - **Cristian** — Recursos Humanos
    - **Emmanuel** — Atención a Clientes
    - **Adolfo** — Marketing
    
    ### 📋 ¿Qué hacemos?
    Recolectamos aceite usado de automóviles de forma segura,
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
                st.session_state.usuario["nombre_usuario"] = nuevo_nombre
            else:
                st.error(msg)

# 📦 NUEVA SOLICITUD
elif menu == "📦 Nueva Solicitud":
    if not st.session_state.usuario:
        st.warning("⚠️ Inicia sesión primero")
    else:
        st.title("📦 Solicitar Recolección")
        st.info(f"💲 Precio por tambo: **${COSTO_POR_TAMBO:,} MXN** — El total se calculará automáticamente")
        nombre_taller = st.text_input("🏢 Nombre del Taller / Negocio")
        ubicacion = st.text_area("📍 Dirección completa")
        referencia = st.text_area("🗺️ Referencias para llegar")
        tambos = st.number_input("Cantidad de tambos/envases", min_value=1, step=1)
        fecha = st.date_input("📅 Fecha preferida")
        horario = st.selectbox("⏰ Horario preferido", ["Mañana (9:00-12:00)", "Tarde (12:00-15:00)", "Por la tarde (15:00-18:00)"])
        if tambos:
            st.subheader(f"💰 Total a pagar: **${tambos * COSTO_POR_TAMBO:,} MXN**")
        if st.button("✅ Enviar Solicitud"):
            datos = {
                "correo_usuario": st.session_state.usuario["correo"],
                "nombre_usuario": st.session_state.usuario["nombre_usuario"],
                "nombre_taller": nombre_taller,
                "ubicacion": ubicacion,
                "referencia": referencia,
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

# 📦 MIS PEDIDOS
elif menu == "📦 Mis Pedidos":
    if not st.session_state.usuario:
        st.warning("⚠️ Inicia sesión primero")
    else:
        st.title("📦 Mis Pedidos")
        try:
            correo = st.session_state.usuario["correo"]
            respuesta = supabase.table("historial_recoleccion").select("*").eq("correo_usuario", correo).order("fecha", desc=True).execute()
            if respuesta.data:
                for solicitud in respuesta.data:
                    st.subheader(f"📅 {solicitud.get('fecha', 'Sin fecha')}")
                    st.write(f"**Cantidad de tambos:** {solicitud.get('tambos', 0)}")
                    estado = solicitud.get('estado', 'Pendiente')
                    if estado == "Pendiente":
                        st.info(f"⏳ **{estado}**")
                    elif estado == "En proceso":
                        st.warning(f"🔄 **{estado}**")
                    elif estado == "Completado":
                        st.success(f"✅ **{estado}**")
                    st.divider()
            else:
                st.info("📋 No tienes pedidos registrados aún")
        except Exception as e:
            st.error(f"Error al cargar pedidos: {str(e)}")

# ⚙️ ADMINISTRACIÓN
elif menu == "⚙️ Administración":
    correo_usuario = st.session_state.usuario.get("correo", "")
    if correo_usuario not in ADMIN_CORREOS:
        st.error("❌ No tienes permiso para acceder a esta página")
    else:
        st.title("⚙️ Panel de Administración")
        st.success(f"👋 Bienvenido Administrador — {st.session_state.usuario.get('nombre_usuario','Administrador')}")
        
        tab1, tab2, tab3 = st.tabs(["📋 Pedidos de Recolección", "✅ Pedidos Completados", "👥 Usuarios Registrados"])
        
        with tab1:
            st.subheader("Pedidos de Recolección")
            try:
                respuesta = supabase.table("historial_recoleccion").select("*").order("fecha", desc=True).execute()
                if respuesta.data:
                    for idx, pedido in enumerate(respuesta.data):
                        pedido_id = pedido.get("id")
                        st.markdown(f"**Pedido #{pedido_id}** — 📅 {pedido.get('fecha', 'Sin fecha')}")
                        st.write(f"👤 Usuario: {pedido.get('nombre_usuario', '')}")
                        st.write(f"🏢 Taller: {pedido.get('nombre_taller', '')}")
                        st.write(f"📍 Ubicación: {pedido.get('ubicacion', '')}")
                        st.write(f"📦 Tambos: {pedido.get('tambos', 0)} — 💰 Total: ${pedido.get('tambos', 0) * COSTO_POR_TAMBO:,}")
                        
                        estado_actual = pedido.get('estado', 'Pendiente')
                        st.info(f"Estado actual: **{estado_actual}**")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("🔄 En proceso", key=f"proc_{idx}") and estado_actual != "En proceso":
                                ok, msg = cambiar_estado_pedido(pedido_id, "En proceso")
                                st.success(msg)
                                st.rerun()
                        with col2:
                            if st.button("✅ Completar", key=f"comp_{idx}") and estado_actual != "Completado":
                                ok, msg = cambiar_estado_pedido(pedido_id, "Completado")
                                st.success(msg)
                                st.rerun()
                        with col3:
                            if st.button("🗑️ Eliminar", key=f"del_{idx}"):
                                ok, msg = eliminar_pedido(pedido_id)
                                if ok:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
            except Exception as e:
                        st.error(f"❌ Error al cargar pedidos: {str(e)}")
            
            with tab2:
                st.subheader("✅ Pedidos Completados")
                try:
                    respuesta_completados = supabase.table("pedidos_completados").select("*").order("fecha_pedido", desc=True).execute()
                    if respuesta_completados.data:
                        for pc in respuesta_completados.data:
                            st.markdown(f"**Pedido #{pc.get('numero_pedido')}**")
                            st.write(f"📅 Fecha: {pc.get('fecha_pedido')}")
                            st.write(f"📦 Tambos: {pc.get('cantidad_tambos')}")
                            st.write(f"💰 Total: ${pc.get('costo_total'):,}")
                            st.divider()
                    else:
                        st.info("📋 No hay pedidos completados aún")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            with tab3:
                st.subheader("👥 Usuarios Registrados")
                try:
                    respuesta_usuarios = supabase.table("usuarios").select("*").execute()
                    if respuesta_usuarios.data:
                        for usr in respuesta_usuarios.data:
                            st.markdown(f"**{usr.get('nombre_usuario')}**")
                            st.write(f"📧 {usr.get('correo')}")
                            correo_usr = usr.get("correo")
                            if correo_usr not in ADMIN_CORREOS:
                                if st.button(f"🗑️ Eliminar usuario", key=f"delusr_{correo_usr}"):
                                    ok_del, msg_del = eliminar_usuario(correo_usr)
                                    if ok_del:
                                        st.success(msg_del)
                                        st.rerun()
                                    else:
                                        st.error(msg_del)
                            st.divider()
                    else:
                        st.info("📋 No hay usuarios registrados aún")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# 🚪 Cerrar Sesión
elif menu == "🚪 Cerrar Sesión":
    st.session_state.usuario = None
    st.success("✅ Sesión cerrada correctamente")
    st.rerun()
