import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    usuarios = relationship('Usuario', back_populates='person')
# Clase Usuario que hereda de Base y que representa la tabla usuario
class Usuario(Base):
    __tablename__ = 'usuario'# Aquí defino las columnas de la tabla usuario
    id = Column(Integer, primary_key=True)# defino la columna id como clave primaria
    username = Column(String(250), nullable=False, unique=True)#  defino la columna username como un string de 250 caracteres, no puede ser nulo y debe ser único
    password = Column(String(250), nullable=False)# defino la columna password como un string de 250 caracteres y no puede ser nulo
    email = Column(String(250), nullable=False, unique=True)#  defino la columna email como un string de 250 caracteres, no puede ser nulo y debe ser único
    fecha_subscripcion = Column(String(250), nullable=False)#  defino la columna fecha_subscripcion como un string de 250 caracteres y no puede ser nulo
    nombre = Column(String(250), nullable=False)# defino la columna nombre como un string de 250 caracteres y no puede ser nulo
    apellido = Column(String(250), nullable=False)# defino la columna apellido como un string de 250 caracteres y no puede ser nulo
    address_id = Column(Integer, ForeignKey('address.id'))# defino la columna address_id como un entero y es una clave foránea de la tabla address
    address = relationship('Address', back_populates='usuarios')# defino la relación de la tabla usuario con la tabla address
    person_id = Column(Integer, ForeignKey('person.id'))# defino la columna person_id como un entero y es una clave foránea de la tabla person
    person = relationship('Person', back_populates='usuarios')# defino la relación de la tabla usuario con la tabla person
    favoritos = relationship('Favorito', back_populates='usuario')# defino la relación de la tabla usuario con la tabla favorito
   
    # Propiedad híbrida que devuelve el total de favoritos
    def total_favoritos(self): # defino el método total_favoritos
        return len(self.favoritos)# retorno la longitud de la lista de favoritos
    
   
    def total_personajes(self):# defino el método total_personajes
        return len([f for f in self.favoritos if f.personaje_id is not None])# retorno la longitud de la lista de favoritos que tengan un personaje_id
    
   
    def total_planetas(self):# defino el método total_planetas
        return len([f for f in self.favoritos if f.planeta_id is not None])# retorno la longitud de la lista de favoritos que tengan un planeta_id
    
# Clase Personaje que hereda de Base y que representa la tabla personaje
class Personaje(Base):
    __tablename__ = 'personaje'# Aquí defino las columnas de la tabla personaje
    id = Column(Integer, primary_key=True)# defino la columna id como clave primaria
    nombre = Column(String(250), nullable=False)# defino la columna nombre como un string de 250 caracteres y no puede ser nulo
    descripcion = Column(Text, nullable=True)# defino la columna descripcion como un texto y puede ser nulo
    imagen_url = Column(String(250), nullable=True)# defino la columna imagen_url como un string de 250 caracteres y puede ser nulo
    favoritos = relationship('Favorito', back_populates='personaje')# defino la relación de la tabla personaje con la tabla favorito
    
 # Clase Planeta que hereda de Base y que representa la tabla planeta
class Planeta(Base):
    __tablename__ = 'planeta'
    id = Column(Integer, primary_key=True)# defino la columna id como clave primaria
    nombre = Column(String(250), nullable=False)# defino la columna nombre como un string de 250 caracteres y no puede ser nulo
    descripcion = Column(Text, nullable=True)# defino la columna descripcion como un texto y puede ser nulo
    imagen_url = Column(String(250), nullable=True)# defino la columna imagen_url como un string de 250 caracteres y puede ser nulo
    favoritos = relationship('Favorito', back_populates='planeta') # defino la relación de la tabla planeta con la tabla favorito 
    
    
# Clase Favorito que hereda de Base y que representa la tabla favorito
class Favorito(Base):
    __tablename__ = 'favorito'# Aquí defino las columnas de la tabla favorito
    id = Column(Integer, primary_key=True)# defino la columna id como clave primaria
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)# defino la columna usuario_id como un entero, no puede ser nulo y es una clave foránea de la tabla usuario
    personaje_id = Column(Integer, ForeignKey('personaje.id'))# defino la columna personaje_id como un entero y es una clave foránea de la tabla personaje
    planeta_id = Column(Integer, ForeignKey('planeta.id'))# defino la columna planeta_id como un entero y es una clave foránea de la tabla planeta
    usuario = relationship('Usuario', back_populates='favoritos')# defino la relación de la tabla favorito con la tabla usuario
    personaje = relationship('Personaje', back_populates='favoritos')# defino la relación de la tabla favorito con la tabla personaje
    planeta = relationship('Planeta', back_populates='favoritos') # defino la relación de la tabla favorito con la tabla planeta   
        
class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)
    usuarios = relationship('Usuario', back_populates='address')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
