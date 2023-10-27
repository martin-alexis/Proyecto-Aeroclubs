from utils.db import db

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ValorCuota(Base):
    __tablename__ = 'VALOR_CUOTA'
    id_tarifas = Column(Integer, primary_key=True)
    importe = Column(Float, nullable=False)
    vigente_desde = Column(Date, nullable=False)

class Estados(Base):
    __tablename__ = 'ESTADOS'
    id_estados = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)
    estado = Column(Integer, nullable=False)
    productos_id = Column(Integer, nullable=False)

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
    dirección = Column(String(100))
    foto_perfil = Column(Text)
    estados_id = Column(Integer, ForeignKey('ESTADOS.id_estados'))
    estado = relationship("Estados")

class EstadoCMA(Base):
    __tablename__ = 'ESTADO_CMA'
    id_estado_cma = Column(Integer, primary_key=True)
    estado = Column(String(45), nullable=False)

class CMA(Base):
    __tablename__ = 'CMA'
    id_cma = Column(Integer, primary_key=True)
    clase = Column(String(255), nullable=False)
    limitaciones = Column(String(255))
    observaciones = Column(String(255))
    valido_hasta = Column(Date, nullable=False)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    estado_cma_id = Column(Integer, ForeignKey('ESTADO_CMA.id_estado_cma'))
    usuario = relationship("Usuarios")
    estado_cma = relationship("EstadoCMA")

class TiposLicencias(Base):
    __tablename__ = 'TIPOS_LICENCIAS'
    id_tipo_licencias = Column(Integer, primary_key=True)
    tipo = Column(String(45), nullable=False)

class Licencias(Base):
    __tablename__ = 'LICENCIAS'
    id_licencias = Column(Integer, primary_key=True)
    descripcion = Column(String(255))
    fecha_vencimiento = Column(Date, nullable=False)
    path = Column(Text)
    usuarios_id = Column(Integer, ForeignKey('USUARIOS.id_usuarios'))
    tipo_licencias_id = Column(Integer, ForeignKey('TIPOS_LICENCIAS.id_tipo_licencias'))
    usuario = relationship("Usuarios")
    tipo_licencia = relationship("TiposLicencias")

class EstadosAeronaves(Base):
    __tablename__ = 'ESTADOS_AERONAVES'
    id_estados_aeronaves = Column(Integer, primary_key=True)
    estado = Column(String(45), nullable=False)

class Aeronaves(Base):
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
    estados_aeronaves_id = Column(Integer, ForeignKey('ESTADOS_AERONAVES.id_estados_aeronaves'))
    estados_id = Column(Integer, ForeignKey('ESTADOS.id_estados'))
    estado_aeronave = relationship("EstadosAeronaves")
    estado = relationship("Estados")

# Create an engine that stores data in memory
engine = create_engine('mysql://username:password@localhost/mydb')

# Create all tables in the engine
Base.metadata.create_all(engine)
