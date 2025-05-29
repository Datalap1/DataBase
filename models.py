from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import date

class Estudiante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    edad: int

    participaciones: list["Participacion"] = Relationship(back_populates="estudiante")

class Actividad(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str

    participaciones: list["Participacion"] = Relationship(back_populates="actividad")

class Participacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiante.id")
    actividad_id: int = Field(foreign_key="actividad.id")
    fecha_participacion: str

    estudiante: Optional[Estudiante] = Relationship(back_populates="participaciones")
    actividad: Optional[Actividad] = Relationship(back_populates="participaciones")
