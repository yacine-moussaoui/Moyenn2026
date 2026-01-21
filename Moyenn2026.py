import streamlit as st
from fpdf import FPDF
import pandas as pd

# ===== المواد =====
modules = [
    ("Couches minces", 2, "TD"),
    ("Physique des composants", 3, "TD"),
    ("Outils de simulation", 2, "TD"),
    ("Procédés d'élaboration", 2, "TD"),
    ("Conception et Modélisation", 2, "TP"),
    ("Programmation avancée", 2, "TP"),
    ("TP Outils de simulation", 1, "TP"),
    ("TP Physique des composants", 1, "TP"),
    ("TP Propriétés optiques", 1, "TP"),
    ("Industrie de la Microélectronique", 1, "Contrôle")
]

# ===== إعداد الصفحة =====
st.set_page_config(page_title="Moyenne M1 - Yacine", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.big-title {font-size:40px; font-weight:bold; color:#1f4ed8;}
.subtitle {font-size:18px; color:gray;}
.card {padding:15px; border-radius:15px; background-color:#f5f7ff; margin-bottom:10px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📊 Calcul Moyenne M1 Microélectronique</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Semestre 1 – Développé par Yacine Moussaoui</div>', unsafe_allow_html=True)
st.divider()

notes = {}
total = 0
total_coef = 0

# ===== إدخال النقاط =====
st.subheader("✍️ إدخال النقاط")

for module, coef, typ in modules:
    with st.container():
        st.markdown(f"<div class='card'><b>{module}</b> (Coef {coef})</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        if typ == "TD":
            with col1:
                td = st.number_input(f"TD", 0.0, 20.0, step=0.1, key=f"td_{module}")
            with col2:
                control = st.number_input(f"Contrôle", 0.0, 20.0, step=0.1, key=f"control_{module}")
            moyenne = 0.4 * td + 0.6 * control
        elif typ == "TP":
            with col1:
                tp = st.number_input(f"TP", 0.0, 20.0, step=0.1, key=f"tp_{module}")
            with col2:
                control = st.number_input(f"Contrôle", 0.0, 20.0, step=0.1, key=f"control_{module}")
            moyenne = 0.4 * tp + 0.6 * control
        else:  # Contrôle only
            with col1:
                control = st.number_input(f"Contrôle", 0.0, 20.0, step=0.1, key=f"control_{module}")
            moyenne = control

    notes[module] = moyenne
    total += moyenne * coef
    total_coef += coef

# ===== جدول النتائج =====
st.subheader("📋 Résultats")

df = pd.DataFrame({
    "Module": [m[0] for m in modules],
    "Type": [m[2] for m in modules],
    "Moyenne": [round(notes[m[0]], 2) for m in modules]
})

def color_moyenne(val):
    if val < 10:
        return 'color: red; font-weight: bold'
    elif val < 14:
        return 'color: orange; font-weight: bold'
    else:
        return 'color: green; font-weight: bold'

st.dataframe(df.style.applymap(color_moyenne, subset=["Moyenne"]), use_container_width=True)

# ===== المعدل العام =====
moyenne_generale = total / total_coef
st.subheader("🏆 Moyenne Générale")
st.metric("Moyenne", f"{moyenne_generale:.2f} / 20")
st.progress(int((moyenne_generale / 20) * 100))

# ===== إنشاء PDF =====
if st.button("📄 Télécharger le relevé en PDF"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Moyenne M1 Microélectronique - S1", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 5, "Développé par Yacine Moussaoui", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 11)
    for module, moyenne in notes.items():
        pdf.cell(0, 8, f"{module} : {moyenne:.2f}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Moyenne Générale : {moyenne_generale:.2f}", ln=True)

    pdf_bytes = pdf.output(dest="S").encode("latin1")

    st.download_button(
        "⬇️ Télécharger le PDF",
        data=pdf_bytes,
        file_name="Moyenne_M1_Yacine.pdf",
        mime="application/pdf"
    )

st.divider()
st.caption("© 2026 - Application M1 Microélectronique | Yacine Moussaoui")
