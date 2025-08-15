import os, requests, streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="CliniOps.AI — Painel", layout="centered")
st.title("CliniOps.AI — Painel")

tab1, tab2 = st.tabs(["Buscar Protocolos", "IA de Suporte"])

with tab1:
    st.caption("Digite termos, sintomas ou título de protocolo.")
    q = st.text_input("Buscar")
    if st.button("Buscar") and q:
        try:
            r = requests.get(f"{API}/protocols", params={"q": q}, timeout=20)
            r.raise_for_status()
            st.json(r.json())
        except Exception as e:
            st.error(f"Falha ao buscar: {e}")

    st.divider()
    st.caption("Cadastrar novo protocolo (demo)")
    t = st.text_input("Título")
    s = st.text_input("Especialidade (opcional)")
    c = st.text_area("Conteúdo", height=150)
    if st.button("Cadastrar protocolo") and t and c:
        try:
            r = requests.post(f"{API}/protocols", json={"title": t, "specialty": s or None, "content": c}, timeout=20)
            r.raise_for_status()
            st.success("Protocolo cadastrado.")
        except Exception as e:
            st.error(f"Falha ao cadastrar: {e}")

with tab2:
    st.caption("Sugestões com base em sintomas/contexto e especialidade (opcional).")
    symptoms = st.text_area("Sintomas/Contexto", height=150)
    specialty = st.text_input("Especialidade (opcional)")
    if st.button("Sugerir") and symptoms:
        try:
            r = requests.post(f"{API}/ai/suggest", json={"symptoms": symptoms, "specialty": specialty or None}, timeout=20)
            r.raise_for_status()
            st.json(r.json())
        except Exception as e:
            st.error(f"Falha ao sugerir: {e}")
