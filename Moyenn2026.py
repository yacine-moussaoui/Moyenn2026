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
    ("Outils de simulation", 1, "TP"),
    ("Physique des composants", 1, "TP"),
    ("Propriétés optiques", 1, "TP"),
    ("Industrie de la Microélectronique", 1, "CONTROL_ONLY")
]

# ===== إعداد الصفحة =====
st.set_page_config(page_title="Moyenne M1 - Yacine", page_icon="🎓", layout="wide")

# ===== تصميم متوافق Dark Mode =====
st.markdown("""
<style>
.big-title {font-size:36px; font-weight:bold; color:#1f4ed8; text-align:center;}
.subtitle {font-size:16px; color:gray; text-align:center;}
.card {padding:15px; border-radius:15px; margin-bottom:10px; background-color:rgba(245,247,255,0.2);}
.stButton>button {background-color:#1f4ed8; color:white;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📊 Calcul Moyenne M1 Microélectronique</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Semestre 1 – Développé par Yacine Moussaoui</div>', unsafe_allow_html=True)
st.divider()

# ===== إدخال النقاط =====
notes = {}
total = 0
total_coef = 0

st.subheader("✍️ Saisie des notes")

for module, coef, typ in modules:
    st.markdown(f"<div class='card'><b>{module}</b> (Coef {coef})</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    if typ == "TD":
        with col1:
            td = st.number_input(f"TD {module}", 0.0, 20.0, step=0.1, key=f"td_{module}")
        with col2:
            control = st.number_input(f"Contrôle {module}", 0.0, 20.0, step=0.1, key=f"control_{module}")
        moyenne = td * 0.4 + control * 0.6

    elif typ == "CONTROL_ONLY":
        control = st.number_input(f"Contrôle {module}", 0.0, 20.0, step=0.1, key=f"control_{module}")
        moyenne = control

    else:  # TP
        tp = st.number_input(f"TP {module}", 0.0, 20.0, step=0.1, key=f"tp_{module}")
        moyenne = tp

    notes[module] = moyenne
    total += moyenne * coef
    total_coef += coef

# ===== Résultats =====
df = pd.DataFrame({
    "Module": list(notes.keys()),
    "Moyenne": [round(v,2) for v in notes.values()]
})

# ===== تحديد Mention لكل مادة =====
def get_mention(val):
    if val < 10:
        return "Échec"
    elif val < 12:
        return "Passable"
    elif val < 14:
        return "Assez Bien"
    elif val < 16:
        return "Bien"
    elif val < 18:
        return "Très Bien"
    else:
        return "Excellent"

df["Mention"] = df["Moyenne"].apply(get_mention)

# ===== تلوين العمود "Mention" فقط =====
def color_mention(val):
    if val == "Échec":
        return 'background-color: #f8d7da; color:black'
    elif val == "Passable":
        return 'background-color: #fff3cd; color:black'
    elif val == "Assez Bien":
        return 'background-color: #cce5ff; color:black'
    elif val == "Bien":
        return 'background-color: #99ccff; color:black'
    elif val == "Très Bien":
        return 'background-color: #d4edda; color:black'
    else:  # Excellent
        return 'background-color: #ffe58a; color:black'

st.subheader("📋 Résultats")
st.dataframe(df.style.applymap(color_mention, subset=["Mention"]), use_container_width=True)

# ===== Moyenne générale + Statut =====
moyenne_generale = total / total_coef
if moyenne_generale < 10:
    statut = "❌ Ajourné"
    mention_gen = "Échec"
elif moyenne_generale < 12:
    statut = "✅ Admis"
    mention_gen = "Passable"
elif moyenne_generale < 14:
    statut = "✅ Admis"
    mention_gen = "Assez Bien"
elif moyenne_generale < 16:
    statut = "✅ Admis"
    mention_gen = "Bien"
elif moyenne_generale < 18:
    statut = "✅ Admis"
    mention_gen = "Très Bien"
else:
    statut = "🏆 Admis"
    mention_gen = "Excellent"

st.subheader("🏆 Résultat Final")
st.metric("Moyenne Générale", f"{moyenne_generale:.2f} / 20")
st.success(f"Statut : {statut}")
st.info(f"Mention : {mention_gen}")
st.progress(int((moyenne_generale / 20) * 100))

# ===== PDF =====
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
    for module, moyenne, mention_mod in zip(df["Module"], df["Moyenne"], df["Mention"]):
        pdf.cell(0, 8, f"{module} : {moyenne:.2f} ({mention_mod})", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Moyenne Générale : {moyenne_generale:.2f}", ln=True)
    pdf.cell(0, 8, f"Statut : {statut}", ln=True)
    pdf.cell(0, 8, f"Mention : {mention_gen}", ln=True)

    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer, 'F')
    pdf_buffer.seek(0)

    st.download_button(
        "⬇️ Télécharger le PDF",
        data=pdf_buffer,
        file_name="Releve_M1_Yacine.pdf",
        mime="application/pdf"
    )

st.caption("© 2026 - Application M1 Microélectronique | Yacine Moussaoui")
