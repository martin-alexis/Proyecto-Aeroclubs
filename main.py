
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Float, Date, Text, ForeignKey, Boolean
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

class DatosHistoricos(Base):
    __tablename__ = 'DATOS_HISTORICOS'
    id_datos_historicos = Column(Integer, primary_key=True)
    fecha_carga = Column(Date, nullable=False)
    descripcion = Column(Text)
    horas_vuelo = Column(Integer, nullable=False)
    cantidad_aterrizajes = Column(Integer, nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    usuarios = relationship('Usuarios')

    def __init__(self, fecha_carga, descripcion, horas_vuelo, cantidad_aterrizajes, usuarios_id):
        self.fecha_carga = fecha_carga
        self.descripcion = descripcion
        self.horas_vuelo = horas_vuelo
        self.cantidad_aterrizajes = cantidad_aterrizajes
        self.usuarios_id = usuarios_id


class CMA(Base):
    __tablename__ = 'CMA'
    id_cma = Column(Integer, primary_key=True)
    clase = Column(String(255), nullable=False)
    limitaciones = Column(String(255))
    observaciones = Column(String(255))
    valido_hasta = Column(Date, nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    estado_cma_id = Column(Integer, ForeignKey('ESTADO_CMA.id_estado_cma'))

    def __init__(self, clase, limitaciones, observaciones, valido_hasta, usuarios_id, estado_cma_id):
        self.clase = clase
        self.limitaciones = limitaciones
        self.observaciones = observaciones
        self.valido_hasta = valido_hasta
        self.usuarios_id = usuarios_id
        self.estado_cma_id = estado_cma_id


class EstadoCMA(Base):
    __tablename__ = 'ESTADO_CMA'
    id_estado_cma = Column(Integer, primary_key=True)
    estado = Column(String(45), nullable=False)

    def __init__(self, estado):
        self.estado = estado

class TiposLicencias(Base):
    __tablename__ = 'TIPOS_LICENCIAS'
    id_tipo_licencias = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo


class Licencias(Base):
    __tablename__ = 'LICENCIAS'
    id_licencias = Column(Integer, primary_key=True)
    descripcion = Column(String(255))
    fecha_vencimiento = Column(Date, nullable=False)
    path = Column(Text)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    tipo_licencias_id = Column(Integer, ForeignKey('TIPOS_LICENCIAS.id_tipo_licencias'))

    def __init__(self, descripcion, fecha_vencimiento, path, usuarios_id, tipo_licencias_id):
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.path = path
        self.usuarios_id = usuarios_id
        self.tipo_licencias_id = tipo_licencias_id

class TiposHabilitaciones(Base):
    __tablename__ = 'TIPOS_HABILITACIONES'
    id_tipo_habilitaciones = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo

class Habilitaciones(Base):
    __tablename__ = 'HABILITACIONES'
    id_habilitaciones = Column(Integer, primary_key=True)
    valido_hasta = Column(Date, nullable=False)
    path = Column(Text)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    tipo_habilitaciones_id = Column(Integer, ForeignKey('TIPOS_HABILITACIONES.id_tipo_habilitaciones'))
    usuarios = relationship('Usuarios')
    tipo_habilitaciones = relationship('TiposHabilitaciones')

    def __init__(self, valido_hasta, path, usuarios_id, tipo_habilitaciones_id):
        self.valido_hasta = valido_hasta
        self.path = path
        self.usuarios_id = usuarios_id
        self.tipo_habilitaciones_id = tipo_habilitaciones_id

class CuentaCorriente(Base):
    __tablename__ = 'CUENTA_CORRIENTE'
    id_cuenta_corriente = Column(Integer, primary_key=True)
    saldo_cuenta = Column(Float, nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    movimientos_id = Column(Integer, ForeignKey('TRANSACCIONES.id_transacciones'))
    usuarios = relationship('Usuarios')
    movimientos = relationship('Transacciones')

    def __init__(self, saldo_cuenta, usuarios_id, movimientos_id):
        self.saldo_cuenta = saldo_cuenta
        self.usuarios_id = usuarios_id
        self.movimientos_id = movimientos_id

class TipoPago(Base):
    __tablename__ = 'TIPO_PAGO'
    id_tipo_pago = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)
    observaciones = Column(Text)

    def __init__(self, tipo, observaciones=None):
        self.tipo = tipo
        self.observaciones = observaciones

class Transacciones(Base):
    __tablename__ = 'TRANSACCIONES'
    id_transacciones = Column(Integer, primary_key=True)
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    motivo = Column(Text)
    TIPO_PAGO_id_tipo_pago = Column(Integer, ForeignKey('TIPO_PAGO.id_tipo_pago'), nullable=False)
    tipo_pago = relationship('TipoPago', back_populates='transacciones')

    def __init__(self, monto, fecha, motivo=None, tipo_pago=None):
        self.monto = monto
        self.fecha = fecha
        self.motivo = motivo
        self.tipo_pago = tipo_pago

TipoPago.transacciones = relationship('Transacciones', back_populates='tipo_pago')


class NotasVuelos(Base):
    __tablename__ = 'NOTAS_VUELOS'
    id_notas_vuelos = Column(Integer, primary_key=True)
    descripcion = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    instructores_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    asociados_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    instructores = relationship('Usuarios', foreign_keys=[instructores_id])
    asociados = relationship('Usuarios', foreign_keys=[asociados_id])

    def __init__(self, descripcion, fecha, instructores_id, asociados_id):
        self.descripcion = descripcion
        self.fecha = fecha
        self.instructores_id = instructores_id
        self.asociados_id = asociados_id

class UsuariosPagoCuotasSociales(Base):
    __tablename__ = 'USUARIOS_pago_CUOTAS_SOCIALES'
    id_usuarios_pago_cuota_social = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    cuotas_sociales_id = Column(Integer, ForeignKey('CUOTAS_SOCIALES.id_cuotas_sociales'))
    usuarios = relationship('Usuarios')
    cuotas_sociales = relationship('CuotasSociales')

    def __init__(self, usuarios_id, cuotas_sociales_id):
        self.usuarios_id = usuarios_id
        self.cuotas_sociales_id = cuotas_sociales_id

class CuotasSociales(Base):
    __tablename__ = 'CUOTAS_SOCIALES'
    id_cuotas_sociales = Column(Integer, primary_key=True)
    mes = Column(Date, nullable=False)

    def __init__(self, mes):
        self.mes = mes

class TipoCuotasSociales(Base):
    __tablename__ = 'TIPO_CUOTAS_SOCIALES'
    id_tipo_cuotas_sociales = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)
    vigencia_desde = Column(Date, nullable=False)
    importe = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=False)
    cuotas_sociales_id = Column(Integer, ForeignKey('CUOTAS_SOCIALES.id_cuotas_sociales'))
    cuotas_sociales = relationship('CuotasSociales')
    
    def __init__(self, nombre, vigencia_desde, importe, descripcion, cuotas_sociales_id):
        self.nombre = nombre
        self.vigencia_desde = vigencia_desde
        self.importe = importe
        self.descripcion = descripcion
        self.cuotas_sociales_id = cuotas_sociales_id


class EstadosAeronaves(Base):
    __tablename__ = 'ESTADOS_AERONAVES'
    id_estados_aeronaves = Column(Integer, primary_key=True)
    estado = Column(String(45), nullable=False)

    def __init__(self, estado):
        self.estado = estado


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

class TipoVuelosRecibos(Base):
    __tablename__ = 'TIPO_VUELOS_RECIBOS'
    id_tipo_vuelos_recibos = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo


class Recibo(Base):
    __tablename__ = 'RECIBOS'

    id_recibos = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)
    observaciones = Column(Text)
    tipo_recibos_id = Column(Integer, ForeignKey('TIPO_RECIBOS.id_tipo_recibos'), nullable=False)
    cuotas_sociales_id = Column(Integer, ForeignKey('CUOTAS_SOCIALES.id_cuotas_sociales'), nullable=False)
    movimientos_id = Column(Integer, ForeignKey('MOVIMIENTOS.id_movimientos'), nullable=False)
    TRANSACCIONES_id_transacciones = Column(Integer, ForeignKey('TRANSACCIONES.id_transacciones'), nullable=False)
    OPERACIONES_id_movimineto_horas_vuelo = Column(Integer, ForeignKey('OPERACIONES.id_movimineto_horas_vuelo'), nullable=False)
    ITINERARIOS_id_itinerarios = Column(Integer, ForeignKey('ITINERARIOS.id_itinerarios'), nullable=False)

    # Definir las relaciones
    tipo_recibo = relationship('TipoRecibo', back_populates='recibos')
    cuota_social = relationship('CuotaSocial', back_populates='recibos')
    movimiento = relationship('Movimiento', back_populates='recibos')
    transaccion = relationship('Transaccion', back_populates='recibos')
    operacion = relationship('Operacion', back_populates='recibos')
    itinerario = relationship('Itinerario', back_populates='recibos')

    # Índices
    Index('fk_VUELOS_RECIBOS_TIPO_VUELOS_RECIBOS1_idx', tipo_recibos_id)
    Index('fk_RECIBOS_CUOTAS_SOCIALES1_idx', cuotas_sociales_id)
    Index('fk_RECIBOS_MOVIMIENTOS1_idx', movimientos_id)
    Index('fk_RECIBOS_TRANSACCIONES1_idx', TRANSACCIONES_id_transacciones)
    Index('fk_RECIBOS_OPERACIONES1_idx', OPERACIONES_id_movimineto_horas_vuelo)
    Index('fk_RECIBOS_ITINERARIOS1_idx', ITINERARIOS_id_itinerarios)

    def __init__(self, fecha, tipo_recibos_id, cuotas_sociales_id, movimientos_id, 
                 TRANSACCIONES_id_transacciones, OPERACIONES_id_movimineto_horas_vuelo, ITINERARIOS_id_itinerarios,
                 observaciones=None):
        self.fecha = fecha
        self.tipo_recibos_id = tipo_recibos_id
        self.cuotas_sociales_id = cuotas_sociales_id
        self.movimientos_id = movimientos_id
        self.TRANSACCIONES_id_transacciones = TRANSACCIONES_id_transacciones
        self.OPERACIONES_id_movimineto_horas_vuelo = OPERACIONES_id_movimineto_horas_vuelo
        self.ITINERARIOS_id_itinerarios = ITINERARIOS_id_itinerarios
        self.observaciones = observaciones


class ComponentesAeronaves(Base):
    __tablename__ = 'COMPONENTES_AERONAVES'
    id_componente = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    marca = Column(String(255), nullable=False)
    modelo = Column(String(255), nullable=False)
    horas_usadas = Column(Integer, nullable=False)
    horas_hasta_revision = Column(Integer, nullable=False)
    descripcion = Column(Text)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'))
    aeronaves = relationship('Aeronaves')

    def __init__(self, nombre, marca, modelo, horas_usadas, horas_hasta_revision, descripcion, aeronaves_id):
        self.nombre = nombre
        self.marca = marca
        self.modelo = modelo
        self.horas_usadas = horas_usadas
        self.horas_hasta_revision = horas_hasta_revision
        self.descripcion = descripcion
        self.aeronaves_id = aeronaves_id

class TipoItinerarios(Base):
    __tablename__ = 'TIPO_ITINERARIOS'
    id_tipo_itinerarios = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo

class Itinerario(Base):
    __tablename__ = 'ITINERARIOS'

    id_itinerarios = Column(Integer, primary_key=True)
    hora_salida = Column(Date, nullable=False)
    hora_llegada = Column(Date, nullable=False)
    cantidad_aterrizajes = Column(Integer, nullable=False)
    observaciones = Column(String(255))
    tipo_itinerarios_id = Column(Integer, ForeignKey('TIPO_ITINERARIOS.id_tipo_itinerarios'), nullable=False)
    AERONAVES_id_aeronaves = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'), nullable=False)

    # Definir las relaciones
    tipo_itinerario = relationship('TipoItinerario', back_populates='itinerarios')
    aeronave = relationship('Aeronave', back_populates='itinerarios')

    # Índices
    Index('fk_ITINERARIOS2_TIPO_ITINERARIOS1_idx', tipo_itinerarios_id)
    Index('fk_ITINERARIOS_AERONAVES1_idx', AERONAVES_id_aeronaves)

    def __init__(self, hora_salida, hora_llegada, cantidad_aterrizajes, observaciones, vuelos_recibos_id, tipo_itinerarios_id, AERONAVES_id_aeronaves):
        self.hora_salida = hora_salida
        self.hora_llegada = hora_llegada
        self.cantidad_aterrizajes = cantidad_aterrizajes
        self.observaciones = observaciones
        self.vuelos_recibos_id = vuelos_recibos_id
        self.tipo_itinerarios_id = tipo_itinerarios_id
        self.AERONAVES_id_aeronaves = AERONAVES_id_aeronaves

class Roles(Base):
    __tablename__ = 'ROLES'
    id_roles = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo

class Medidas(Base):
    __tablename__ = 'MEDIDAS'
    id_medidas = Column(Integer, primary_key=True)
    medida = Column(String(255), nullable=False)

    def __init__(self, medida):
        self.medida = medida

class Productos(Base):
    __tablename__ = 'PRODUCTOS'
    id_productos = Column(Integer, primary_key=True)
    nombre_producto = Column(String(45), nullable=False)
    stock = Column(Float, nullable=False)
    precio = Column(Float, nullable=False)
    cantidad_minima = Column(Integer, nullable=False)
    cantidad_maxima = Column(Integer, nullable=False)
    fecha_ultimo_encargue = Column(Date, nullable=False)
    medidas_id = Column(Integer, ForeignKey('MEDIDAS.id_medidas'))
    estado_hab_des = Column(Boolean, nullable=False)
    medidas = relationship('Medidas')

    def __init__(self, nombre_producto, stock, precio, cantidad_minima, cantidad_maxima, fecha_ultimo_encargue, medidas_id, estado_hab_des):
        self.nombre_producto = nombre_producto
        self.stock = stock
        self.precio = precio
        self.cantidad_minima = cantidad_minima
        self.cantidad_maxima = cantidad_maxima
        self.fecha_ultimo_encargue = fecha_ultimo_encargue
        self.medidas_id = medidas_id
        self.estado_hab_des = estado_hab_des

class UsuariosTieneRoles(Base):
    __tablename__ = 'USUARIOS_tiene_ROLES'
    id_usuarios_tiene_roles = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    roles_id = Column(Integer, ForeignKey('ROLES.id_roles'))
    usuarios = relationship('Usuarios')
    roles = relationship('Roles')

    def __init__(self, usuarios_id, roles_id):
        self.usuarios_id = usuarios_id
        self.roles_id = roles_id

class Tarifas(Base):
    __tablename__ = 'TARIFAS'
    id_tarifas = Column(Integer, primary_key=True, nullable=True)
    vigente_desde = Column(Date, nullable=False)
    importe_vuelo = Column(Float, nullable=False)
    importe_instruccion = Column(Float, nullable=False)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'), nullable=False)
    
    def __init__(self, vigente_desde, importe_vuelo, importe_instruccion, aeronaves_id):
        self.vigente_desde = vigente_desde
        self.importe_vuelo = importe_vuelo
        self.importe_instruccion = importe_instruccion
        self.aeronaves_id = aeronaves_id


class CodigosAeropuertos(Base):
    __tablename__ = 'CODIGOS_AEROPUERTOS'
    id_codigos_aeropuertos = Column(Integer, primary_key=True)
    codigo_aeropuerto = Column(String(45), nullable=False)

    def __init__(self, codigo_aeropuerto):
        self.codigo_aeropuerto = codigo_aeropuerto

class ItinerariosTienenCodigosAeropuertos(Base):
    __tablename__ = 'ITINERARIOS_tienen_CODIGOS_AEROPUERTOS'
    id_itinerarios_tienen_codigos = Column(Integer, primary_key=True)
    itinerarios_id = Column(Integer, ForeignKey('ITINERARIOS.id_itinerarios'))
    codigos_aeropuertos_id = Column(Integer, ForeignKey('CODIGOS_AEROPUERTOS.id_codigos_aeropuertos'))
    itinerarios = relationship('Itinerarios')
    codigos_aeropuertos = relationship('CodigosAeropuertos')

    def __init__(self, itinerarios_id, codigos_aeropuertos_id):
        self.itinerarios_id = itinerarios_id
        self.codigos_aeropuertos_id = codigos_aeropuertos_id


class UsuariosTienenRecibos(Base):
    __tablename__ = 'USUARIOS_tienen_RECIBOS'

    id_usuarios_tienen_recibos = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'), nullable=False)
    vuelos_recibos_id = Column(Integer, ForeignKey('RECIBOS.id_recibos'), nullable=False)

    # Definir las relaciones
    usuario = relationship('Usuario', back_populates='recibos_asociados')
    recibo = relationship('Recibo', back_populates='usuarios_asociados')

    # Índices
    Index('fk_USUARIOS_has_VUELOS_RECIBOS_VUELOS_RECIBOS1_idx', vuelos_recibos_id)
    Index('fk_USUARIOS_has_VUELOS_RECIBOS_USUARIOS1_idx', usuarios_id)


class Movimientos(Base):
    __tablename__ = 'MOVIMIENTOS'
    idMOVIMIENTOS = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    matricula = Column(String(100), nullable=False)
    cantidad = Column(Float, nullable=False)
    productos_id = Column(Integer, ForeignKey('PRODUCTOS.id_productos'))
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    productos = relationship('Productos')
    usuarios = relationship('Usuarios')

    def __init__(self, fecha, matricula, cantidad, productos_id, usuarios_id):
        self.fecha = fecha
        self.matricula = matricula
        self.cantidad = cantidad
        self.productos_id = productos_id
        self.usuarios_id = usuarios_id

class Reportes(Base):
    __tablename__ = 'REPORTES'
    id_reportes = Column(Integer, primary_key=True)
    reportes_falla = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'))
    aeronaves = relationship('Aeronaves')

    def __init__(self, reportes_falla, fecha, aeronaves_id):
        self.reportes_falla = reportes_falla
        self.fecha = fecha
        self.aeronaves_id = aeronaves_id





class Seguros(Base):
    __tablename__ = 'SEGUROS'
    id_seguros = Column(Integer, primary_key=True)
    fecha_carga = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    importe = Column(Float, nullable=False)
    identificacion = Column(String(255), nullable=False)
    aeronaves_id = Column(Integer, ForeignKey('AERONAVES.id_aeronaves'))
    aeronaves = relationship('Aeronaves')

    def __init__(self, fecha_carga, fecha_vencimiento, importe, identificacion, aeronaves_id):
        self.fecha_carga = fecha_carga
        self.fecha_vencimiento = fecha_vencimiento
        self.importe = importe
        self.identificacion = identificacion
        self.aeronaves_id = aeronaves_id



Session = sessionmaker(engine)
session = Session()

if __name__=='__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)