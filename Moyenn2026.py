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
    ("Conception et Modélisation", 2, "TP"),  # بدل TD نستخدمو TP
    ("Programmation avancée", 2, "TP"),       # بدل TD نستخدمو TP
    ("TP Outils de simulation", 1, "TP"),
    ("TP Physique des composants", 1, "TP"),
    ("TP Propriétés optiques", 1, "TP"),
    ("Industrie de la Microélectronique", 1, "Contrôle")  # غير الكونطرول
]

# ===== دالة لحساب المعدل =====
def calculer_moyenne(notes):
    total_coef = 0
    total_note = 0
    for module, coef, type_mod in modules:
        module_key = module.strip()
        
        if type_mod == "Contrôle":
            note = notes.get(f"{module_key}_Contrôle", 0)
        else:
            note_tp = notes.get(f"{module_key}_TP", 0)
            note_controle = notes.get(f"{module_key}_Contrôle", 0)
            # المعدل = 40% TP + 60% Controle
            note = 0.4 * note_tp + 0.6 * note_controle
        
        total_note += note * coef
        total_coef += coef
    
    return total_note / total_coef if total_coef != 0 else 0

# ===== دالة إنشاء PDF =====
def create_pdf(notes, moyenne):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Resultats M1 Microelectronique", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    for module, coef, type_mod in modules:
        module_key = module.strip()
        if type_mod == "Contrôle":
            note = notes.get(f"{module_key}_Contrôle", 0)
            pdf.cell(0, 8, f"{module}: {note}/20 (Contrôle)", ln=True)
        else:
            note_tp = notes.get(f"{module_key}_TP", 0)
            note_controle = notes.get(f"{module_key}_Contrôle", 0)
            note_finale = 0.4 * note_tp + 0.6 * note_controle
            pdf.cell(0, 8, f"{module}: TP={note_tp}, Contrôle={note_controle}, Moyenne={note_finale:.2f}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Moyenne Generale: {moyenne:.2f}/20", ln=True, align="C")
    
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

# ===== واجهة Streamlit =====
st.title("Calcul Moyenne M1 - YACINE MOUSSAOUI")

notes = {}

for module, coef, type_mod in modules:
    st.subheader(module)
    if type_mod == "Contrôle":
        notes[f"{module}_Contrôle"] = st.number_input(f"Note {module} (Contrôle)", 0.0, 20.0, 0.0)
    elif type_mod == "TP":
        notes[f"{module}_TP"] = st.number_input(f"Note {module} (TP)", 0.0, 20.0, 0.0)
        notes[f"{module}_Contrôle"] = st.number_input(f"Note {module} (Contrôle)", 0.0, 20.0, 0.0)
    else:
        notes[f"{module}_TD"] = st.number_input(f"Note {module} (TD)", 0.0, 20.0, 0.0)
        notes[f"{module}_Contrôle"] = st.number_input(f"Note {module} (Contrôle)", 0.0, 20.0, 0.0)

if st.button("Calculer la moyenne"):
    moyenne = calculer_moyenne(notes)
    st.success(f"Votre moyenne est: {moyenne:.2f}/20")
    
    # توليد PDF
    pdf_buffer = create_pdf(notes, moyenne)
    st.download_button(
        label="Télécharger le PDF",
        data=pdf_buffer,
        file_name="resultats_m1.pdf",
        mime="application/pdf"
    )
