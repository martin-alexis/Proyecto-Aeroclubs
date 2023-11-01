
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Float, Date, Text, ForeignKey, Boolean, Index, UniqueConstraint
from sqlalchemy.orm import relationship

engine = create_engine('mysql+mysqlconnector://root:''@localhost/aeroclub')
Base = declarative_base()


class Usuarios(Base):
    __tablename__ = 'USUARIOS'
    id_usuarios = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)
    apellido = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    telefono = Column(Integer, nullable=False)
    dni = Column(Integer, nullable=False, unique=True)
    fecha_alta = Column(Date, nullable=False)
    fecha_baja = Column(Date, nullable=False)
    direccion = Column(String(100))
    foto_perfil = Column(Text)
    estado_hab_des = Column(Boolean, nullable=False)

# Relaciones
    datos_historicos_usuarios = relationship('DatosHistoricos', backref='usuarios')
    cma_usuarios = relationship('CMA', backref='usuarios')
    licencias_usuarios = relationship('Licencias', backref='usuarios')
    habilitaciones_usuarios = relationship('Habilitaciones', backref='usuarios')
    cuentaCorriente_usuarios = relationship('CuentaCorriente', backref='usuarios')
    tarifaEspecial_usuarios = relationship('TarifaEspecial', backref='usuarios')


    def __init__(self, nombre, apellido, email, telefono, dni, fecha_alta, fecha_baja, dirección, foto_perfil, estado_hab_des):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.dni = dni
        self.fecha_alta = fecha_alta
        self.fecha_baja = fecha_baja
        self.direccion = direccion
        self.foto_perfil = foto_perfil
        self.estado_hab_des = estado_hab_des


#--------------------------------------------------
# USUARIOS -> DATOS_HISTORICOS (0:N)
#--------------------------------------------------
class DatosHistoricos(Base):
    __tablename__ = 'DATOS_HISTORICOS'

    id_datos_historicos = Column(Integer, primary_key=True)
    fecha_carga = Column(Date, nullable=False)
    descripcion = Column(Text)
    horas_vuelo = Column(Integer, nullable=False)
    cantidad_aterrizajes = Column(Integer, nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    

    def __init__(self, fecha_carga, descripcion, horas_vuelo, cantidad_aterrizajes, usuarios_id):
        self.fecha_carga = fecha_carga
        self.descripcion = descripcion
        self.horas_vuelo = horas_vuelo
        self.cantidad_aterrizajes = cantidad_aterrizajes
        self.usuarios_id = usuarios_id
#--------------------------------------------------

#--------------------------------------------------
# USUARIOS -> CMA (1:N)
#--------------------------------------------------
class CMA(Base):
    __tablename__ = 'CMA'
    id_cma = Column(Integer, primary_key=True)
    clase = Column(String(255), nullable=False)
    limitaciones = Column(String(255))
    observaciones = Column(String(255))
    valido_hasta = Column(Date, nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    estado_cma_id = Column(Integer, ForeignKey('ESTADO_CMA.id_estado_cma'), nullable=False)

    def __init__(self, clase, limitaciones, observaciones, valido_hasta, usuarios_id, estado_cma_id):
        self.clase = clase
        self.limitaciones = limitaciones
        self.observaciones = observaciones
        self.valido_hasta = valido_hasta
        self.usuarios_id = usuarios_id
        self.estado_cma_id = estado_cma_id
#--------------------------------------------------

#--------------------------------------------------
# ESTADOS_CMA -> CMA (1:N)
#--------------------------------------------------
class EstadoCMA(Base):
    __tablename__ = 'ESTADO_CMA'
    id_estado_cma = Column(Integer, primary_key=True)
    estado = Column(String(45), nullable=False)

#Relaciones
    cma_estado = relationship('CMA', backref='estado_cma')

    def __init__(self, estado):
        self.estado = estado
#--------------------------------------------------

#--------------------------------------------------
# USUARIOS -> LICENCIAS (0:N)
#--------------------------------------------------
class Licencias(Base):
    __tablename__ = 'LICENCIAS'
    id_licencias = Column(Integer, primary_key=True)
    descripcion = Column(String(255))
    fecha_vencimiento = Column(Date, nullable=False)
    path = Column(Text)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    tipo_licencias_id = Column(Integer, ForeignKey('TIPOS_LICENCIAS.id_tipo_licencias'), nullable=False)

    def __init__(self, descripcion, fecha_vencimiento, path, usuarios_id, tipo_licencias_id):
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.path = path
        self.usuarios_id = usuarios_id
        self.tipo_licencias_id = tipo_licencias_id
#--------------------------------------------------

#--------------------------------------------------
# TIPOS_LICENCIAS -> LICENCIAS (1:N)
#--------------------------------------------------
class TiposLicencias(Base):
    __tablename__ = 'TIPOS_LICENCIAS'
    id_tipo_licencias = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)

#Relaciones
    licencias_tipo = relationship('Licencias', backref='tipos_licencias')


    def __init__(self, tipo):
        self.tipo = tipo
#--------------------------------------------------

#--------------------------------------------------
# USUARIOS -> HABILITACIONES (0:N)
#--------------------------------------------------
class Habilitaciones(Base):
    __tablename__ = 'HABILITACIONES'
    id_habilitaciones = Column(Integer, primary_key=True)
    valido_hasta = Column(Date, nullable=False)
    path = Column(Text)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    tipo_habilitaciones_id = Column(Integer, ForeignKey('TIPOS_HABILITACIONES.id_tipo_habilitaciones'), nullable=False)

    def __init__(self, valido_hasta, path, usuarios_id, tipo_habilitaciones_id):
        self.valido_hasta = valido_hasta
        self.path = path
        self.usuarios_id = usuarios_id
        self.tipo_habilitaciones_id = tipo_habilitaciones_id
#--------------------------------------------------

#--------------------------------------------------
# TIPOS_HABILITACIONES -> HABILITACIONES (1:N)
#--------------------------------------------------
class TiposHabilitaciones(Base):
    __tablename__ = 'TIPOS_HABILITACIONES'
    id_tipo_habilitaciones = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)

#Relaciones
    habilitaciones_tipo = relationship('Habilitaciones', backref='tipos_habilitaciones')

    def __init__(self, tipo):
        self.tipo = tipo
#--------------------------------------------------

#--------------------------------------------------
# USUARIOS -> CUENTA_CORRIENTE (0:N)
#--------------------------------------------------
class CuentaCorriente(Base):
    __tablename__ = 'CUENTA_CORRIENTE'
    id_cuenta_corriente = Column(Integer, primary_key=True)
    saldo_cuenta = Column(Float, nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    transacciones_id = Column(Integer, ForeignKey('TRANSACCIONES.id_transacciones'), nullable=False)


    def __init__(self, saldo_cuenta, usuarios_id, transacciones_id):
        self.saldo_cuenta = saldo_cuenta
        self.usuarios_id = usuarios_id
        self.transacciones_id = transacciones_id
#--------------------------------------------------

#--------------------------------------------------
# TRANSACCIONES -> CUENTA_CORRIENTE (1:N)
#--------------------------------------------------
class Transacciones(Base):
    __tablename__ = 'TRANSACCIONES'
    id_transacciones = Column(Integer, primary_key=True)
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    motivo = Column(Text)
    tipo_pago_id = Column(Integer, ForeignKey('TIPO_PAGO.id_tipo_pago'), nullable=False)

#Relaciones
    cuentaCorriente_transacciones = relationship('CuentaCorriente', backref='transacciones')


    def __init__(self, monto, fecha, motivo, tipo_pago_id):
        self.monto = monto
        self.fecha = fecha
        self.motivo = motivo
        self.tipo_pago_id = tipo_pago_id
#--------------------------------------------------

#--------------------------------------------------
# TIPO_PAGO -> TRANSACCIONES (1:N)
#--------------------------------------------------
class TipoPago(Base):
    __tablename__ = 'TIPO_PAGO'
    id_tipo_pago = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)
    observaciones = Column(Text)

#Relaciones
    transacciones_tipoPago = relationship('Transacciones', backref='tipos_pago')


    def __init__(self, tipo, observaciones=None):
        self.tipo = tipo
        self.observaciones = observaciones
#--------------------------------------------------

#--------------------------------------------------
# USUARIOS -> TARIFA_ESPECIAL (0:N)
#--------------------------------------------------
class TarifaEspecial(Base):
    __tablename__ = 'TARIFA_ESPECIAL'

    id_tarifa_especial = Column(Integer, primary_key=True)
    aplica = Column(Boolean, nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    
    def __init__(self, aplica, usuarios_id):
        self.aplica = aplica
        self.usuarios_id = usuarios_id
#--------------------------------------------------

#--------------------------------------------------
class NotasVuelos(Base):
    __tablename__ = 'NOTAS_VUELOS'

    id_notas_vuelos = Column(Integer, primary_key=True, nullable=True)
    descripcion = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    instructores_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    asociados_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=False)
    
#Relaciones
    instructores = relationship('Usuarios', foreign_keys=[instructores_id], back_populates='notas_vuelos_instructor')
    asociados = relationship('Usuarios', foreign_keys=[asociados_id], back_populates='notas_vuelos_asociado')

    def __init__(self, descripcion, fecha, instructores_id, asociados_id):
        self.descripcion = descripcion
        self.fecha = fecha
        self.instructores_id = instructores_id
        self.asociados_id = asociados_id
#--------------------------------------------------

#--------------------------------------------------
class UsuariosPagoCuotaSocial(Base):
    __tablename__ = 'USUARIOS_pago_CUOTAS_SOCIALES'

    id_usuarios_pago_cuota_social = Column(Integer, primary_key=True, autoincrement=True)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    cuotas_sociales_id = Column(Integer, ForeignKey('CUOTAS_SOCIALES.id_cuotas_sociales'), nullable=False)

# Relaciones
    usuario = relationship('Usuario', back_populates='pagos_cuotas_sociales')
    cuota_social = relationship('CuotasSociales', back_populates='usuarios_pago_cuotas_sociales')

    def __init__(self, usuarios_id, cuotas_sociales_id):
        self.usuarios_id = usuarios_id
        self.cuotas_sociales_id = cuotas_sociales_id
#--------------------------------------------------

#--------------------------------------------------
class CuotasSociales(Base):
    __tablename__ = 'CUOTAS_SOCIALES'

    id_cuotas_sociales = Column(Integer, primary_key=True)
    mes = Column(Date, nullable=False)

# Relaciones
    tipo_cuotas_sociales = relationship('TipoCuotasSociales', back_populates='cuota_social')

    def __init__(self, mes):
        self.mes = mes
#--------------------------------------------------

#--------------------------------------------------
class TipoCuotasSociales(Base):
    __tablename__ = 'TIPO_CUOTAS_SOCIALES'

    id_tipo_cuotas_sociales = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)
    vigencia_desde = Column(Date, nullable=False)
    importe = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=False)
    cuotas_sociales_id = Column(Integer, ForeignKey('CUOTAS_SOCIALES.id_cuotas_sociales'), nullable=False)

# Relaciones
    cuota_social = relationship('CuotasSociales', back_populates='tipo_cuotas_sociales')

    def __init__(self, nombre, vigencia_desde, importe, descripcion, cuotas_sociales_id):
        self.nombre = nombre
        self.vigencia_desde = vigencia_desde
        self.importe = importe
        self.descripcion = descripcion
        self.cuotas_sociales_id = cuotas_sociales_id
#--------------------------------------------------

#--------------------------------------------------
class Rol(Base):
    __tablename__ = 'ROLES'

    id_roles = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)
    usuarios_tienen_recibos_id = Column(Integer, ForeignKey('USUARIOS_tienen_RECIBOS.id_usuarios_tienen_recibos'), nullable=False)

    # Definición de la relación con la tabla USUARIOS_tienen_RECIBOS
    usuarios_tienen_recibos_roles = relationship('UsuariosTienenRecibos', back_populates='rol')

    # Definición del método __init__
    def __init__(self, tipo, usuarios_tienen_recibos_id):
        self.tipo = tipo
        self.usuarios_tienen_recibos_id = usuarios_tienen_recibos_id#--------------------------------------------------

#--------------------------------------------------
class UsuariosTieneRoles(Base):
    __tablename__ = 'USUARIOS_tiene_ROLES'

    id_usuarios_tiene_roles = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=False)
    roles_id = Column(Integer, ForeignKey('ROLES.id_roles'), nullable=False)

# Relaciones
    usuario = relationship('Usuarios', back_populates='roles')
    rol = relationship('Roles', back_populates='usuarios_tiene_roles')

    def __init__(self, usuarios_id, roles_id):
        self.usuarios_id = usuarios_id
        self.roles_id = roles_id
#--------------------------------------------------

#--------------------------------------------------
class Producto(Base):
    __tablename__ = 'PRODUCTOS'

    id_productos = Column(Integer, primary_key=True)
    nombre_producto = Column(String(45), nullable=False)
    stock = Column(Float, nullable=False)
    precio = Column(Float, nullable=False)
    cantidad_minima = Column(Integer, nullable=False)
    cantidad_maxima = Column(Integer, nullable=False)
    fecha_ultimo_encargue = Column(Date, nullable=False)
    estado_hab_des = Column(Boolean, nullable=False)
    medidas_id = Column(Integer, ForeignKey('MEDIDAS.id_medidas'), nullable=False)

# Relaciones
    medidas = relationship('Medida', back_populates='productos')

    def __init__(self, nombre_producto, stock, precio, cantidad_minima, cantidad_maxima, fecha_ultimo_encargue, estado_hab_des, medidas_id):
        self.nombre_producto = nombre_producto
        self.stock = stock
        self.precio = precio
        self.cantidad_minima = cantidad_minima
        self.cantidad_maxima = cantidad_maxima
        self.fecha_ultimo_encargue = fecha_ultimo_encargue
        self.estado_hab_des = estado_hab_des
        self.medidas_id = medidas_id
#--------------------------------------------------

#--------------------------------------------------
class Medida(Base):
    __tablename__ = 'MEDIDAS'

    id_medidas = Column(Integer, primary_key=True)
    medida = Column(String(255), nullable=False, unique=True)

    # Definición del método __init__
    def __init__(self, medida):
        self.medida = medida
#--------------------------------------------------

#--------------------------------------------------
class Movimiento(Base):
    __tablename__ = 'MOVIMIENTOS'

    id_movimientos = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    matricula = Column(String(100), nullable=False)
    cantidad = Column(Float, nullable=False)
    productos_id = Column(Integer, ForeignKey('PRODUCTOS.id_productos'), nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)

#Relaciones
    productos_movimientos = relationship('Producto', back_populates='movimientos')
    usuarios_movimientos = relationship('Usuario', back_populates='movimientos')

    # Definición del método __init__
    def __init__(self, fecha, matricula, cantidad, productos_id, usuarios_id):
        self.fecha = fecha
        self.matricula = matricula
        self.cantidad = cantidad
        self.productos_id = productos_id
        self.usuarios_id = usuarios_id
#--------------------------------------------------

#--------------------------------------------------
class CuentaCorrienteHoras(Base):
    __tablename__ = 'CUENTA_CORRIENTE_HORAS'

    id_cuenta_corriente_horas = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)

# Relaciones
    usuarios_cc_horas = relationship('Usuario', back_populates='cuenta_corriente_horas')

    # Definición del método __init__
    def __init__(self, usuarios_id):
        self.usuarios_id = usuarios_id
#--------------------------------------------------

#--------------------------------------------------
class Operacion(Base):
    __tablename__ = 'OPERACIONES'

    id_operaciones = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    descripcion = Column(Text)
    cantidad_horas = Column(Float, nullable=False)
    cuenta_corriente_horas_id = Column(Integer, ForeignKey('CUENTA_CORRIENTE_HORAS.id_cuenta_corriente_horas'), nullable=False)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'), nullable=False)

# Relaciones
    cuenta_corriente_horas_operacion = relationship('CuentaCorrienteHoras', back_populates='operaciones')
    aeronave_operacion = relationship('Aeronave', back_populates='operaciones')

    # Definición del método __init__
    def __init__(self, fecha, descripcion, cantidad_horas, cuenta_corriente_horas_id, aeronaves_id):
        self.fecha = fecha
        self.descripcion = descripcion
        self.cantidad_horas = cantidad_horas
        self.cuenta_corriente_horas_id = cuenta_corriente_horas_id
        self.aeronaves_id = aeronaves_id
#--------------------------------------------------

#--------------------------------------------------
class UsuariosTienenRecibos(Base):
    __tablename__ = 'USUARIOS_tienen_RECIBOS'

    id_usuarios_tienen_recibos = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=True)
    recibos_id = Column(Integer, ForeignKey('RECIBOS.id_recibos'), nullable=False)
    
    # Definición del método __init__
    def __init__(self, usuarios_id, recibos_id):
        self.usuarios_id = usuarios_id
        self.recibos_id = recibos_id
#--------------------------------------------------

#--------------------------------------------------
class Recibo(Base):
    __tablename__ = 'RECIBOS'

    id_recibos = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)
    observaciones = Column(Text)
    tipo_recibos_id = Column(Integer, ForeignKey('TIPO_RECIBOS.id_tipo_recibos'), nullable=False)
    cuotas_sociales_id = Column(Integer, ForeignKey('CUOTAS_SOCIALES.id_cuotas_sociales'), nullable=True)
    transacciones_id = Column(Integer, ForeignKey('TRANSACCIONES.id_transacciones'), nullable=True)
    operaciones_id = Column(Integer, ForeignKey('OPERACIONES.id_operaciones'), nullable=True)
    itinerarios_id = Column(Integer, ForeignKey('ITINERARIOS.id_itinerarios'), nullable=True)
    movimientos_id = Column(Integer, ForeignKey('MOVIMIENTOS.id_movimientos'), nullable=False)

    # Definición de las relaciones con las tablas TIPO_RECIBOS, CUOTAS_SOCIALES, TRANSACCIONES, OPERACIONES, ITINERARIOS y MOVIMIENTOS
    tipo_recibo_recibo = relationship('TipoRecibo', back_populates='recibos')
    cuotas_sociales_recibo = relationship('CuotaSocial', back_populates='recibos')
    transaccion_recibo = relationship('Transaccion', back_populates='recibos')
    operacion_recibo = relationship('Operacion', back_populates='recibos')
    itinerario_recibo = relationship('Itinerario', back_populates='recibos')
    movimiento_recibo = relationship('Movimiento', back_populates='recibos')

    # Definición del método __init__
    def __init__(self, fecha, observaciones, tipo_recibos_id, cuotas_sociales_id, transacciones_id, operaciones_id, itinerarios_id, movimientos_id):
        self.fecha = fecha
        self.observaciones = observaciones
        self.tipo_recibos_id = tipo_recibos_id
        self.cuotas_sociales_id = cuotas_sociales_id
        self.transacciones_id = transacciones_id
        self.operaciones_id = operaciones_id
        self.itinerarios_id = itinerarios_id
        self.movimientos_id = movimientos_id
#--------------------------------------------------


#--------------------------------------------------
class TipoRecibo(Base):
    __tablename__ = 'TIPO_RECIBOS'

    id_tipo_recibos = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False, unique=True)

    # Definición del método __init__
    def __init__(self, tipo):
        self.tipo = tipo
#--------------------------------------------------

#--------------------------------------------------
class Itinerario(Base):
    __tablename__ = 'ITINERARIOS'

    id_itinerarios = Column(Integer, primary_key=True)
    hora_salida = Column(Date, nullable=False)
    hora_llegada = Column(Date, nullable=False)
    cantidad_aterrizajes = Column(Integer, nullable=False)
    observaciones = Column(String(255))
    tipo_itinerarios_id = Column(Integer, ForeignKey('TIPO_ITINERARIOS.id_tipo_itinerarios'), nullable=False)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'), nullable=False)

    # Definición de las relaciones con las tablas TIPO_ITINERARIOS y AERONAVES
    tipo_itinerario = relationship('TipoItinerario', back_populates='itinerarios')
    aeronave = relationship('Aeronave', back_populates='itinerarios')

    # Definición del método __init__
    def __init__(self, hora_salida, hora_llegada, cantidad_aterrizajes, observaciones, tipo_itinerarios_id, aeronaves_id):
        self.hora_salida = hora_salida
        self.hora_llegada = hora_llegada
        self.cantidad_aterrizajes = cantidad_aterrizajes
        self.observaciones = observaciones
        self.tipo_itinerarios_id = tipo_itinerarios_id
        self.aeronaves_id = aeronaves_id
#--------------------------------------------------


#--------------------------------------------------
class ItinerarioTieneCodigoAeropuerto(Base):
    __tablename__ = 'ITINERARIOS_tienen_CODIGOS_AEROPUERTOS'

    id_itinerarios_tienen_codigos = Column(Integer, primary_key=True)
    itinerarios_id = Column(Integer, ForeignKey('ITINERARIOS.id_itinerarios'), nullable=False)
    codigos_aeropuertos_id = Column(Integer, ForeignKey('CODIGOS_AEROPUERTOS.id_codigos_aeropuertos'), nullable=False)

# Relaciones
    itinerarios = relationship('Itinerarios')
    codigos_aeropuertos = relationship('CodigosAeropuertos')

    # Definición del método __init__
    def __init__(self, itinerarios_id, codigos_aeropuertos_id):
        self.itinerarios_id = itinerarios_id
        self.codigos_aeropuertos_id = codigos_aeropuertos_id
#--------------------------------------------------

#--------------------------------------------------
class CodigoAeropuerto(Base):
    __tablename__ = 'CODIGOS_AEROPUERTOS'

    id_codigos_aeropuertos = Column(Integer, primary_key=True)
    codigo_aeropuerto = Column(String(45), nullable=False, unique=True)

    # Definición del método __init__
    def __init__(self, codigo_aeropuerto):
        self.codigo_aeropuerto = codigo_aeropuerto
#--------------------------------------------------

#--------------------------------------------------
class TipoItinerario(Base):
    __tablename__ = 'TIPO_ITINERARIOS'

    id_tipo_itinerarios = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False, unique=True)

    # Definición del método __init__
    def __init__(self, tipo):
        self.tipo = tipo
#--------------------------------------------------

#--------------------------------------------------
class Aeronave(Base):
    __tablename__ = 'AERONAVES'

    id_aeronaves = Column(Integer, primary_key=True)
    marca = Column(String(45), nullable=False)
    modelo = Column(String(45), nullable=False)
    matricula = Column(String(45), nullable=False, unique=True)
    potencia = Column(String(45), nullable=False)
    clase = Column(String(45), nullable=False)
    fecha_adquisicion = Column(Date, nullable=False)
    consumo_por_hora = Column(Integer, nullable=False)
    path_documentacion = Column(Text)
    descripcion = Column(Text)
    path_imagen_aeronave = Column(Text)
    estado_hab_des = Column(Boolean, nullable=False)
    estados_aeronaves_id = Column(Integer, ForeignKey('ESTADOS_AERONAVES.id_estados_aeronaves'), nullable=False)

    # Definir las relaciones
    estado_aeronave = relationship('EstadoAeronave', back_populates='aeronaves')

    # Índices
    Index('fk_AERONAVES_ESTADOS_AERONAVES1_idx', estados_aeronaves_id)
    UniqueConstraint('matricula', name='matricula_UNIQUE')

def __init__(self, marca, modelo, matricula, potencia, clase, fecha_adquisicion, consumo_por_hora,
                 path_documentacion=None, descripcion=None, path_imagen_aeronave=None, estado_hab_des=True):
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula
        self.potencia = potencia
        self.clase = clase
        self.fecha_adquisicion = fecha_adquisicion
        self.consumo_por_hora = consumo_por_hora
        self.path_documentacion = path_documentacion
        self.descripcion = descripcion
        self.path_imagen_aeronave = path_imagen_aeronave
        self.estado_hab_des = estado_hab_des
#--------------------------------------------------

#--------------------------------------------------
class EstadosAeronaves(Base):
    __tablename__ = 'ESTADOS_AERONAVES'
    id_estados_aeronaves = Column(Integer, primary_key=True)
    estado = Column(String(45), nullable=False)

    def __init__(self, estado):
        self.estado = estado
#--------------------------------------------------

#--------------------------------------------------
class Reporte(Base):
    __tablename__ = 'REPORTES'

    id_reportes = Column(Integer, primary_key=True)
    reportes_falla = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'), nullable=True)

    # Definición de la relación con la tabla AERONAVES
    aeronave_reporte = relationship('Aeronave', back_populates='reportes')

    # Definición del método __init__
    def __init__(self, reportes_falla, fecha, aeronaves_id):
        self.reportes_falla = reportes_falla
        self.fecha = fecha
        self.aeronaves_id = aeronaves_id
#--------------------------------------------------

#--------------------------------------------------
class Seguro(Base):
    __tablename__ = 'SEGUROS'

    id_seguros = Column(Integer, primary_key=True)
    fecha_carga = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    importe = Column(Float, nullable=False)
    identificacion = Column(String(255), nullable=False)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'), nullable=False)

    # Definición de la relación con la tabla AERONAVES
    aeronave_seguro = relationship('Aeronave', back_populates='seguros')

    # Definición del método __init__
    def __init__(self, fecha_carga, fecha_vencimiento, importe, identificacion, aeronaves_id):
        self.fecha_carga = fecha_carga
        self.fecha_vencimiento = fecha_vencimiento
        self.importe = importe
        self.identificacion = identificacion
        self.aeronaves_id = aeronaves_id
#--------------------------------------------------

#--------------------------------------------------
class ComponenteAeronave(Base):
    __tablename__ = 'COMPONENTES_AERONAVES'

    id_componente = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    marca = Column(String(255), nullable=False)
    modelo = Column(String(255), nullable=False)
    horas_usadas = Column(Integer, nullable=False)
    horas_hasta_revision = Column(Integer, nullable=False)
    descripcion = Column(Text)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'), nullable=False)

    # Definición de la relación con la tabla AERONAVES
    aeronave_componentes = relationship('Aeronave', back_populates='componentes')

    # Definición del método __init__
    def __init__(self, nombre, marca, modelo, horas_usadas, horas_hasta_revision, descripcion, aeronaves_id):
        self.nombre = nombre
        self.marca = marca
        self.modelo = modelo
        self.horas_usadas = horas_usadas
        self.horas_hasta_revision = horas_hasta_revision
        self.descripcion = descripcion
        self.aeronaves_id = aeronaves_id
#--------------------------------------------------

#--------------------------------------------------
class Tarifa(Base):
    __tablename__ = 'TARIFAS'

    id_tarifas = Column(Integer, primary_key=True)
    vigente_desde = Column(Date, nullable=False)
    importe_vuelo = Column(Float, nullable=False)
    importe_instruccion = Column(Float, nullable=False)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'), nullable=False)

    # Definición de la relación con la tabla AERONAVES
    aeronave = relationship('Aeronave', back_populates='tarifas')

    # Definición del método __init__
    def __init__(self, vigente_desde, importe_vuelo, importe_instruccion, aeronaves_id):
        self.vigente_desde = vigente_desde
        self.importe_vuelo = importe_vuelo
        self.importe_instruccion = importe_instruccion
        self.aeronaves_id = aeronaves_id
#--------------------------------------------------


Session = sessionmaker(engine)
session = Session()

if __name__=='__main__':
    Base.metadata.create_all(engine)