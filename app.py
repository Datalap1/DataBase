import streamlit as st
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from basedate import engine, create_db_and_tables
from models import Estudiante, Actividad, Participacion
from datetime import date

# Crear tablas si no existen
create_db_and_tables()

st.title("Gestión de Estudiantes y Actividades")

# --- Agregar estudiante ---
st.header("Agregar nuevo estudiante")
with st.form("form_estudiante"):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    edad = st.number_input("Edad", min_value=1, max_value=120)
    submit_est = st.form_submit_button("Guardar estudiante")

    if submit_est:
        with Session(engine) as session:
            estudiante = Estudiante(nombre=nombre, correo=correo, edad=edad)
            session.add(estudiante)
            session.commit()
            st.success(f"Estudiante {nombre} agregado correctamente")

# --- Eliminar estudiante ---
st.header("Eliminar estudiante")
with Session(engine) as session:
    estudiantes = session.exec(select(Estudiante)).all()

for est in estudiantes:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"{est.nombre} ({est.correo})")
    with col2:
        if st.button("Eliminar", key=f"delete_est_{est.id}"):
            with Session(engine) as delete_session:
                est_a_borrar = delete_session.get(Estudiante, est.id)
                if est_a_borrar:
                    delete_session.delete(est_a_borrar)
                    delete_session.commit()
                    st.success(f"Estudiante {est.nombre} eliminado correctamente")
                    st.experimental_rerun()

# --- Agregar actividad ---
st.header("Agregar nueva actividad")
with st.form("form_actividad"):
    nombre_actividad = st.text_input("Nombre de la actividad")
    descripcion = st.text_area("Descripción")
    submit_act = st.form_submit_button("Guardar actividad")

    if submit_act:
        with Session(engine) as session:
            actividad = Actividad(nombre=nombre_actividad, descripcion=descripcion)
            session.add(actividad)
            session.commit()
            st.success(f"Actividad {nombre_actividad} agregada correctamente")

# --- Eliminar actividad ---
st.header("Eliminar actividad")
with Session(engine) as session:
    actividades = session.exec(select(Actividad)).all()

for act in actividades:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"{act.nombre}")
    with col2:
        if st.button("Eliminar", key=f"delete_act_{act.id}"):
            with Session(engine) as delete_session:
                act_a_borrar = delete_session.get(Actividad, act.id)
                if act_a_borrar:
                    delete_session.delete(act_a_borrar)
                    delete_session.commit()
                    st.success(f"Actividad {act.nombre} eliminada correctamente")
                    st.experimental_rerun()

# --- Registrar participación ---
st.header("Registrar participación")
with Session(engine) as session:
    estudiantes = session.exec(select(Estudiante)).all()
    actividades = session.exec(select(Actividad)).all()

if estudiantes and actividades:
    est_id = st.selectbox("Selecciona un estudiante", estudiantes, format_func=lambda e: f"{e.nombre} ({e.correo})")
    act_id = st.selectbox("Selecciona una actividad", actividades, format_func=lambda a: a.nombre)
    fecha = st.date_input("Fecha de participación", value=date.today())

    if st.button("Registrar participación"):
        with Session(engine) as session:
            participacion = Participacion(estudiante_id=est_id.id, actividad_id=act_id.id, fecha_participacion=str(fecha))
            session.add(participacion)
            session.commit()
            st.success("Participación registrada correctamente")
else:
    st.info("Agrega primero estudiantes y actividades para registrar participaciones.")

# --- Ver y eliminar participaciones ---
st.header("Lista de participaciones")
with Session(engine) as session:
    participaciones = session.exec(
        select(Participacion)
        .options(
            selectinload(Participacion.estudiante),
            selectinload(Participacion.actividad)
        )
    ).all()

for p in participaciones:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"{p.estudiante.nombre} participó en '{p.actividad.nombre}' el {p.fecha_participacion}")
    with col2:
        if st.button("Eliminar", key=f"delete_part_{p.id}"):
            with Session(engine) as delete_session:
                participacion_a_borrar = delete_session.get(Participacion, p.id)
                if participacion_a_borrar:
                    delete_session.delete(participacion_a_borrar)
                    delete_session.commit()
                    st.success(f"Participación de {p.estudiante.nombre} eliminada correctamente")
                    st.experimental_rerun()

