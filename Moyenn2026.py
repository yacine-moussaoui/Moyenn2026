import streamlit as st
from fpdf import FPDF
import pandas as pd
from io import BytesIO

# ===== تعريف المواد =====
modules = [
    ("Couches minces", 2, "TD"),
    ("Physique des composants", 3, "TD"),
    ("Outils de simulation", 2, "TD"),
    ("Procédés d'élaboration", 2, "TD"),
    ("Conception et Modélisation", 2, "TD"),
    ("Programmation avancée", 2, "TD"),
    ("TP Outils de simulation", 1, "TP"),
    ("TP Physique des composants", 1, "TP"),
    ("TP Propriétés optiques", 1, "TP"),
    ("Industrie de la Microélectronique", 1, "TD")
]

# ===== إعداد الصفحة =====
st.set_page_config(page_title="Calcul Moyenne M1 - YACINE MOUSSAOUI", layout="wide")
st.title("📊 Calcul Moyenne M1 Microélectronique - Semestre 1")
st.caption("Développé par YACINE MOUSSAOUI")  # يظهر اسمك أسفل العنوان

notes = {}
total = 0
total_coef = 0

st.subheader("Entrez vos notes:")

# ===== إدخال الدرجات =====
for module, coef, typ in modules:
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown(f"**{module} (Coef {coef})**")
    with col2:
        if typ == "TD":
            td = st.number_input(f"TD {module}", 0.0, 20.0, step=0.1, key=f"td_{module}")
            control = st.number_input(f"Contrôle {module}", 0.0, 20.0, step=0.1, key=f"control_{module}")
            moyenne = td * 0.6 + control * 0.4
        else:
            tp = st.number_input(f"TP {module}", 0.0, 20.0, step=0.1, key=f"tp_{module}")
            moyenne = tp

    notes[module] = moyenne
    total += moyenne * coef
    total_coef += coef

# ===== جدول النتائج =====
st.subheader("Résultats par Module:")

df = pd.DataFrame({
    "Module": [m[0] for m in modules],
    "Type": [m[2] for m in modules],
    "Moyenne": [notes[m[0]] for m in modules]
})

def color_moyenne(val):
    if val < 10:
        return 'color: red'
    elif val < 14:
        return 'color: orange'
    else:
        return 'color: green'

st.dataframe(df.style.applymap(color_moyenne, subset=["Moyenne"]))

# ===== المعدل العام =====
if total_coef > 0:
    moyenne_generale = total / total_coef
    st.subheader(f"⭐ Moyenne Générale = {moyenne_generale:.2f}")
    st.progress(int((moyenne_generale / 20) * 100))

# ===== PDF =====
if st.button("📄 Télécharger PDF"):
    pdf = FPDF()
    pdf.add_page()
    
    # العنوان واسمك في PDF
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Moyenne M1 Microélectronique - S1", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 5, "Développé par YACINE MOUSSAOUI", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    for module, moyenne in notes.items():
        pdf.cell(0, 8, f"{module} : {moyenne:.2f}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Moyenne Générale : {moyenne_generale:.2f}", ln=True)

    pdf_bytes = pdf.output(dest="S").encode("latin1")

    st.download_button(
        "📥 Télécharger le PDF",
        data=pdf_bytes,
        file_name="Moyenne_M1.pdf",
        mime="application/pdf"
    )
