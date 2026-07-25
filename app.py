from campaigns import (
    create_campaign,
    add_draft_to_campaign,
)
from tracking import add_candidate
from templates import (
    get_template_names,
    get_template,
)
from datetime import datetime
import streamlit as st
import pandas as pd

import unicodedata

import re
import drive



# -------------------------------------------------
# Initialisation de la base SQLite
# -------------------------------------------------


st.set_page_config(page_title="Mailing", page_icon="✉️", layout="centered", initial_sidebar_state="expanded")

# Inject custom favicon
_LOGO_B64 = "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"
st.markdown(f'<link rel="shortcut icon" href="data:image/jpeg;base64,{_LOGO_B64}">', unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e8f0; }
.main .block-container { max-width: 820px; padding: 2.5rem 2rem 5rem; }


/* ── Header ── */
.mf-header { display: flex; align-items: center; gap: 18px; margin-bottom: 48px; }
.mf-logo {
  width: 56px; height: 56px; border-radius: 16px; flex-shrink: 0;
  background: linear-gradient(145deg, #c471ed, #7b5ea7, #4776e6);
  display: flex; align-items: center; justify-content: center; font-size: 26px;
  box-shadow: 0 8px 32px rgba(196,113,237,0.35);
}
.mf-title { font-size: 2.8rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1; margin: 0;
  background: linear-gradient(90deg, #c471ed, #7b5ea7, #4776e6);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.mf-sub { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #6b6b88; margin-top: 6px; letter-spacing: 0.06em; }

/* ── Cards ── */
.card { background: #12121a; border: 1px solid #1e1e2e; border-radius: 16px; padding: 26px 28px; margin-bottom: 16px; }
.card-accent { border-color: rgba(196,113,237,0.4); background: linear-gradient(135deg, rgba(196,113,237,0.04), rgba(71,118,230,0.03)); }
.card-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #7b5ea7; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 3px; }
.card-title { font-size: 1rem; font-weight: 700; color: #e8e8f0; margin-bottom: 18px; }

/* ── Variable chips ── */
.var-row { display: flex; gap: 8px; margin-bottom: 14px; }
.var-chip {
  background: rgba(196,113,237,0.12); border: 1px solid rgba(196,113,237,0.3);
  color: #c471ed; border-radius: 6px; padding: 4px 12px;
  font-family: 'DM Mono', monospace; font-size: 0.75rem;
  cursor: pointer; transition: all 0.15s; user-select: none;
}
.var-chip:hover { background: rgba(196,113,237,0.25); border-color: rgba(196,113,237,0.6); }

/* ── Badges ── */
.badge-ok  { display:inline-flex; align-items:center; gap:6px; background:rgba(74,222,128,0.1); border:1px solid rgba(74,222,128,0.3); color:#4ade80; border-radius:6px; padding:4px 12px; font-family:'DM Mono',monospace; font-size:0.74rem; }
.badge-warn{ display:inline-flex; align-items:center; gap:6px; background:rgba(250,204,21,0.1); border:1px solid rgba(250,204,21,0.3); color:#facc15; border-radius:6px; padding:4px 12px; font-family:'DM Mono',monospace; font-size:0.74rem; }

/* ── Example line ── */
.example-line { font-family:'DM Mono',monospace; font-size:0.78rem; color:#6b6b88; margin-top:10px; padding:10px 14px; background:#0e0e18; border-radius:8px; border-left:3px solid #7b5ea7; }
.example-line span { color:#c471ed; }

/* ── Preview card ── */
.prev-card { background:#0e0e18; border:1px solid #1e1e2e; border-radius:10px; padding:14px 18px; margin-bottom:10px; }
.prev-to { font-family:'DM Mono',monospace; font-size:0.7rem; color:#7b5ea7; margin-bottom:4px; letter-spacing:0.04em; }
.prev-subj { font-size:0.9rem; font-weight:600; margin-bottom:8px; }
.prev-body { font-family:'DM Mono',monospace; font-size:0.74rem; color:#6b6b88; border-top:1px solid #1e1e2e; padding-top:8px; white-space:pre-wrap; line-height:1.6; }

/* ── Hint ── */
.hint { background:#0e0e18; border:1px solid #1e1e2e; border-radius:8px; padding:12px 16px; font-family:'DM Mono',monospace; font-size:0.74rem; color:#6b6b88; line-height:1.7; margin-bottom:14px; }
.hint a { color:#c471ed; }
.hint code { background:rgba(196,113,237,0.12); color:#c471ed; padding:1px 6px; border-radius:4px; }
.hint strong { color:#e8e8f0; }

/* ── Logs ── */
.log-ok  { color:#4ade80; font-family:'DM Mono',monospace; font-size:0.76rem; }
.log-err { color:#ff6584; font-family:'DM Mono',monospace; font-size:0.76rem; }
.log-info{ color:#7b5ea7; font-family:'DM Mono',monospace; font-size:0.76rem; }
.log-warn{ color:#facc15; font-family:'DM Mono',monospace; font-size:0.76rem; }

/* ── Streamlit overrides ── */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
  background:#0e0e18 !important; border:1px solid #1e1e2e !important;
  border-radius:10px !important; color:#e8e8f0 !important;
  font-family:'DM Mono',monospace !important; font-size:0.86rem !important;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus { border-color:rgba(196,113,237,0.6) !important; box-shadow:none !important; }
.stSelectbox>div>div { background:#0e0e18 !important; border-color:#1e1e2e !important; color:#e8e8f0 !important; }
label { color:#6b6b88 !important; font-family:'DM Mono',monospace !important; font-size:0.7rem !important; letter-spacing:0.08em !important; text-transform:uppercase !important; }
/* Variable chip buttons */
[data-testid="stHorizontalBlock"] .stButton>button {
  background: rgba(196,113,237,0.12) !important;
  color: #c471ed !important;
  border: 1px solid rgba(196,113,237,0.35) !important;
  border-radius: 6px !important;
  font-family: 'DM Mono', monospace !important;
  font-weight: 400 !important;
  font-size: 0.78rem !important;
  padding: 0.25rem 0.8rem !important;
  box-shadow: none !important;
  transition: all 0.15s !important;
}
[data-testid="stHorizontalBlock"] .stButton>button:hover {
  background: rgba(196,113,237,0.25) !important;
  border-color: rgba(196,113,237,0.6) !important;
  transform: none !important;
  box-shadow: none !important;
}
/* Main CTA buttons — full gradient */
div[data-testid="stVerticalBlock"] > div > div > .stButton>button,
section.main .stButton>button {
  background:linear-gradient(135deg,#c471ed,#7b5ea7,#4776e6) !important;
  color:white !important; border:none !important; border-radius:10px !important;
  font-family:'Syne',sans-serif !important; font-weight:700 !important;
  padding:0.55rem 1.4rem !important; transition:all 0.2s !important;
}
div[data-testid="stVerticalBlock"] > div > div > .stButton>button:hover {
  transform:translateY(-1px); box-shadow:0 8px 24px rgba(196,113,237,0.35) !important;
}
.stButton>button:disabled { opacity:0.35 !important; transform:none !important; }

/* var-chips : force row layout + pill style */
.var-chips + div [data-testid="stHorizontalBlock"],
.var-chips [data-testid="stHorizontalBlock"] {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 4px !important;
  flex-wrap: nowrap !important;
  width: auto !important;
}
.var-chips [data-testid="column"] {
  flex: 0 0 auto !important;
  width: auto !important;
  min-width: max-content !important;
  padding: 0 !important;
}
.var-chips [data-testid="column"] > div,
.var-chips [data-testid="column"] > div > div,
.var-chips [data-testid="column"] > div > div > div { 
  width: auto !important; 
  min-width: max-content !important;
  white-space: nowrap !important; 
}
.var-chips [data-testid="column"] button {
  background: rgba(196,113,237,0.15) !important;
  color: #c471ed !important;
  border: 1px solid rgba(196,113,237,0.4) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.72rem !important;
  font-weight: 400 !important;
  padding: 2px 16px !important;
  height: 26px !important;
  min-height: 0 !important;
  width: auto !important;
  min-width: 0 !important;
  border-radius: 20px !important;
  box-shadow: none !important;
  white-space: nowrap !important;
  line-height: 1 !important;
}
.var-chips [data-testid="column"] button:hover {
  background: rgba(196,113,237,0.28) !important;
  transform: none !important;
  box-shadow: none !important;
}
.stFileUploader { background:#0e0e18 !important; border:2px dashed #1e1e2e !important; border-radius:12px !important; }
.stProgress>div>div { background:linear-gradient(90deg,#c471ed,#4776e6) !important; }
[data-testid="stDataFrame"] { border-radius:10px; overflow:hidden; }
</style>

<script>
function insertVar(fieldId, val) {
  const el = window.parent.document.querySelector(`[data-testid="${fieldId}"] textarea`) ||
             window.parent.document.querySelector(`[data-testid="${fieldId}"] input`);
  if (!el) return;
  const s = el.selectionStart, e = el.selectionEnd;
  el.value = el.value.slice(0,s) + val + el.value.slice(e);
  el.selectionStart = el.selectionEnd = s + val.length;
  el.dispatchEvent(new Event('input', {bubbles:true}));
  el.focus();
}
</script>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="mf-header">
  <div class="mf-logo">✉</div>
  <div>
    <div class="mf-title">Mailing</div>
    <div class="mf-sub">// automatisation de campagnes email personnalisées</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ──
for k, v in {
    "contacts": [],
    "prenom_col": None,
    "nom_col": None,
    "pdfs": []
}.items():
    st.session_state.setdefault(k, v)

# ── Helpers ──

# Titres/certifications LinkedIn à supprimer du nom/prénom
_TITLES = [
    'mba', 'executive mba', 'emba', 'ms', 'm.sc', 'msc', 'phd', 'ph.d', 'md', 'm.d',
    'cfa', 'cpa', 'cfp', 'frm', 'pmp', 'caia', 'acca', 'cma', 'cia', 'mca',
    'llm', 'll.m', 'jd', 'j.d', 'escp', 'hec', 'edhec', 'essec', 'insead',
    'eng', 'meng', 'bsc', 'b.sc', 'ba', 'mres', 'dba',
    'linkedin', 'open to work', 'hiring', 'founder', 'ceo', 'cto', 'coo', 'cfo',
]

import re

def strip_titles(s):
    """Supprime les titres/certifications LinkedIn collés avec --, —, |, / ou , """
    # 1. Couper aux séparateurs forts (-- en premier, avant le simple -)
    parts = re.split(r'--|—|\||/|,', s)
    clean = parts[0].strip()

    # 2. Couper au simple tiret SEULEMENT si ce qui suit est un titre connu
    #    ex: "Justen-M.Sc" → coupe, mais "belotti-de-chanville" → garde
    title_pattern = '|'.join(re.escape(t) for t in sorted(_TITLES, key=len, reverse=True))
    # Cherche un tiret suivi d'un titre (insensible à la casse, avec point optionnel)
    match = re.search(r'-(?=(?:' + title_pattern + r')(?:[.-]|$))', clean, re.IGNORECASE)
    if match:
        clean = clean[:match.start()].strip()

    return clean

def norm_prenom(s):
    """Prénom : supprime titres, espaces → '.'"""
    s = strip_titles(s).lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').replace(' ', '.')

def norm_nom(s):
    """Nom de famille : supprime titres, espaces → '-' pour noms composés"""
    s = strip_titles(s).lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').replace(' ', '-')

def is_censored(val):
    """Retourne True si la valeur ressemble à un nom censuré (1 seul caractère utile)"""
    # On vérifie après nettoyage des titres
    cleaned = strip_titles(val).strip().rstrip('.')
    return len(cleaned) <= 1

def resolve_addr(c, pat, pc, nc):
    prenom = c.get(pc, '').strip()
    nom    = c.get(nc, '').strip()
    # Skip si prénom ou nom censuré (ex: "B" ou "B.")
    if is_censored(prenom) or is_censored(nom):
        return None
    initiale = norm_prenom(prenom)[0] if norm_prenom(prenom) else ''
    return (pat.lower()
               .replace('{prenom}', norm_prenom(prenom))
               .replace('{nom}',    norm_nom(nom))
               .replace('{p}',      initiale))

def resolve_txt(c, txt, pc, nc):

    prenom = c.get(pc, "")
    nom = c.get(nc, "")

    initiale = ""
    if prenom:
        initiale = norm_prenom(prenom)[0]

    return (
        txt
        .replace("{{prenom}}", prenom)
        .replace("{{nom}}", nom)
        .replace("{{p}}", initiale)
        .replace("{{entreprise}}", get_company(c))
        .replace("{{poste}}", get_position(c))
    )
def get_company(contact):
    """
    Détecte automatiquement la colonne entreprise.
    """

    possible_names = {
        "company",
        "entreprise",
        "societe",
        "société",
        "organization",
        "organisation",
        "employer",
        "employeur",
        "firm",
        "business"
    }

    for col in contact.keys():

        if col.lower() in possible_names:

            value = contact.get(col)

            if value:
                return str(value)

    return ""

def get_position(contact):
    """
    Détecte automatiquement la colonne contenant le poste.
    """

    possible_names = {
        "title",
        "job title",
        "position",
        "poste",
        "fonction",
        "role",
        "occupation",
        "job",
        "headline"
    }

    for col in contact.keys():

        if col.lower() in possible_names:

            value = contact.get(col)

            if value:
                return str(value)

    return ""






# ════════════════════════════════════════════════
# 01 — CSV
# ════════════════════════════════════════════════
st.markdown('<div class="card card-accent"><div class="card-label">Étape 01</div><div class="card-title">📋 Importer les contacts</div>', unsafe_allow_html=True)

csv_file = st.file_uploader("Fichier CSV", type=["csv"], label_visibility="collapsed")
if csv_file:
    try:
        try:
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
            if len(df.columns)==1: csv_file.seek(0); df = pd.read_csv(csv_file, sep=',', encoding='utf-8')
        except:
            csv_file.seek(0); df = pd.read_csv(csv_file, sep=',', encoding='latin-1')
        df.columns = df.columns.str.strip()
        st.session_state.contacts = df.to_dict('records')
        cols  = list(df.columns)
        lower = [c.lower() for c in cols]
        dp = next((cols[i] for i,c in enumerate(lower) if 'prenom' in c or 'prénom' in c or 'first' in c), cols[0])
        dn = next((cols[i] for i,c in enumerate(lower) if c=='nom' or 'last' in c), cols[min(1,len(cols)-1)])
        st.markdown(f'<div class="badge-ok" style="margin:10px 0 16px">✓ {len(st.session_state.contacts)} contacts chargés</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.session_state.prenom_col = st.selectbox("Colonne → Prénom", cols, index=cols.index(dp))
        with c2: st.session_state.nom_col    = st.selectbox("Colonne → Nom",    cols, index=cols.index(dn))
        st.dataframe(df[[st.session_state.prenom_col, st.session_state.nom_col]].head(5), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Erreur CSV : {e}")

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# 02 — Pattern email
# ════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-label">Étape 02</div><div class="card-title">📧 Format de l\'adresse email</div>', unsafe_allow_html=True)

if "ep" not in st.session_state: st.session_state.ep = ""
if "ep_inject" not in st.session_state: st.session_state.ep_inject = ""
if st.session_state.ep_inject:
    st.session_state.ep += st.session_state.ep_inject
    st.session_state.ep_inject = ""

st.markdown('<div class="var-chips">', unsafe_allow_html=True)
c1, c2, c3, _ = st.columns([1.5,1.2,0.9,5.4])
with c1: st.button("{prenom}", key="ep_p", on_click=lambda: st.session_state.update(ep_inject="{prenom}"))
with c2: st.button("{nom}",    key="ep_n", on_click=lambda: st.session_state.update(ep_inject="{nom}"))
with c3: st.button("{p}",      key="ep_i", on_click=lambda: st.session_state.update(ep_inject="{p}"))
st.markdown('</div>', unsafe_allow_html=True)

email_pattern = st.text_input("Format", key="ep", placeholder="{prenom}.{nom}@natixis.com", label_visibility="collapsed")

if email_pattern and st.session_state.contacts and st.session_state.prenom_col:
    ex = resolve_addr(st.session_state.contacts[0], email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
    if ex:
        st.markdown(f'<div class="example-line">→ <span>{ex}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="example-line">→ <span style="color:#facc15">premier contact ignoré (nom censuré)</span></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════
# 03 — Contenu
# ════════════════════════════════════════════════

st.markdown(
    '<div class="card"><div class="card-label">Étape 03</div><div class="card-title">✍️ Contenu du mail</div>',
    unsafe_allow_html=True
)

template_names = get_template_names()

if not template_names:
    st.warning("Aucun modèle disponible. Ajoute-en un dans Paramètres.")
    st.stop()

# Initialisation
if "selected_template" not in st.session_state:
    st.session_state.selected_template = template_names[0]

if "ms" not in st.session_state:
    template = get_template(st.session_state.selected_template)
    st.session_state.ms = template["Objet"]
    st.session_state.mb = template["Corps"]

# Sélection du modèle
selected = st.selectbox(
    "Modèle",
    template_names,
    index=template_names.index(st.session_state.selected_template)
)

# Si le modèle change, on recharge automatiquement
if selected != st.session_state.selected_template:

    st.session_state.selected_template = selected

    template = get_template(selected)

    st.session_state.ms = template["Objet"]
    st.session_state.mb = template["Corps"]

    st.rerun()


# ===== Variables =====

st.markdown('<div class="var-chips">', unsafe_allow_html=True)

c1, c2, c3, c4, c5, _ = st.columns([1.2, 1.2, 0.8, 1.8, 1.4, 4])

with c1:
    if st.button("{{prenom}}"):
        st.session_state.mb += "{{prenom}}"

with c2:
    if st.button("{{nom}}"):
        st.session_state.mb += "{{nom}}"

with c3:
    if st.button("{{p}}"):
        st.session_state.mb += "{{p}}"

with c4:
    if st.button("{{entreprise}}"):
        st.session_state.mb += "{{entreprise}}"

with c5:
    if st.button("{{poste}}"):
        st.session_state.mb += "{{poste}}"

st.markdown("</div>", unsafe_allow_html=True)

# Sujet
st.markdown(
    '<p style="font-family:DM Mono,monospace;font-size:0.7rem;color:#6b6b88;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px">Objet</p>',
    unsafe_allow_html=True
)

mail_subject = st.text_input(
    "Objet",
    key="ms",
    label_visibility="collapsed"
)

# Corps
st.markdown(
    '<p style="font-family:DM Mono,monospace;font-size:0.7rem;color:#6b6b88;letter-spacing:0.08em;text-transform:uppercase;margin:12px 0 4px">Corps</p>',
    unsafe_allow_html=True
)

mail_body = st.text_area(
    "Corps",
    key="mb",
    height=220,
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════
# 04 — PDF
# ════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-label">Étape 04</div><div class="card-title">📎 Pièces jointes</div>', unsafe_allow_html=True)

cvs = drive.get_cvs()
letters = drive.get_letters()

cv_options = {f["name"]: f["id"] for f in cvs}
letter_options = {f["name"]: f["id"] for f in letters}

selected_cv = st.selectbox(
    "CV",
    list(cv_options.keys())
)

selected_letter = st.selectbox(
    "Lettre de motivation",
    ["Aucune"] + list(letter_options.keys())
)

st.session_state.selected_cv_id = cv_options[selected_cv]

st.session_state.selected_letter_id = (
    None
    if selected_letter == "Aucune"
    else letter_options[selected_letter]
)

st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════
# 05 — Preview
# ════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-label">Étape 05</div><div class="card-title">🔍 Prévisualisation</div>', unsafe_allow_html=True)

if st.button("Générer la prévisualisation"):
    if not st.session_state.contacts: st.warning("Importe d'abord un CSV.")
    elif not email_pattern: st.warning("Remplis le pattern d'adresse.")
    else:
        shown = 0
        for c in st.session_state.contacts:
            if shown >= 5: break
            to   = resolve_addr(c, email_pattern, st.session_state.prenom_col, st.session_state.nom_col)
            if to is None:
                continue  # skip contacts avec nom censuré
            subj = resolve_txt(c, mail_subject, st.session_state.prenom_col, st.session_state.nom_col)
            body = resolve_txt(c, mail_body,    st.session_state.prenom_col, st.session_state.nom_col)
            st.markdown(f'<div class="prev-card"><div class="prev-to">À → {to}</div><div class="prev-subj">{subj or "(objet vide)"}</div><div class="prev-body">{body or "(corps vide)"}</div></div>', unsafe_allow_html=True)
            shown += 1
        remaining = len(st.session_state.contacts) - shown
        if remaining > 0:
            st.markdown(f'<p style="font-family:DM Mono,monospace;font-size:0.74rem;color:#6b6b88;text-align:center;margin-top:4px">+ {remaining} autres…</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)



# ════════════════════════════════════════════════
# 07 — Envoi
# ════════════════════════════════════════════════
st.markdown(
    '<div class="card"><div class="card-label">Étape 07</div><div class="card-title">🚀 Créer les brouillons</div>',
    unsafe_allow_html=True
)

ready = (
    st.session_state.contacts
    and email_pattern
    and mail_body
)

if not ready:
    missing = [
        x for x, ok in [
            ("CSV", st.session_state.contacts),
            ("Pattern email", email_pattern),
            ("Corps du mail", mail_body),
        ]
        if not ok
    ]
    st.markdown(
        f'<div class="badge-warn">⚠ En attente : {" · ".join(missing)}</div>',
        unsafe_allow_html=True
    )

n = len(st.session_state.contacts)

st.divider()

campaign_name = st.text_input(
    "Nom de la campagne",
    placeholder="Ex : Quant Trading UK"
)

c1, c2 = st.columns(2)

with c1:
    send_date = st.date_input("Date d'envoi")

with c2:
    send_time = st.time_input("Heure d'envoi")

if st.button(
    f"✉ Créer {n} brouillon{'s' if n > 1 else ''} dans Gmail",
    disabled=not (ready and campaign_name.strip())
):

    create_campaign(
        campaign=campaign_name,
        send_date=send_date.strftime("%d/%m/%Y"),
        send_time=send_time.strftime("%H:%M"),
    )

    prog = st.progress(0)
    status = st.empty()
    logs = st.empty()

    lines = []
    ok_count = 0
    err = 0
    skipped = 0

    for i, c in enumerate(st.session_state.contacts):

        to = resolve_addr(
            c,
            email_pattern,
            st.session_state.prenom_col,
            st.session_state.nom_col,
        )

        # Skip contacts avec nom/prénom censuré
        if to is None:
            skipped += 1
            raw = f"{c.get(st.session_state.prenom_col,'?')} {c.get(st.session_state.nom_col,'?')}"
            lines.append(
                f'<div class="log-warn">⚠ Ignoré (nom censuré) — {raw}</div>'
            )

            prog.progress((i + 1) / n)
            logs.markdown("\n".join(lines[-8:]), unsafe_allow_html=True)
            continue

        subj = resolve_txt(
            c,
            mail_subject,
            st.session_state.prenom_col,
            st.session_state.nom_col,
        )

        body = resolve_txt(
            c,
            mail_body,
            st.session_state.prenom_col,
            st.session_state.nom_col,
        )

        try:

            

            add_candidate(
                date=datetime.now().strftime("%d/%m/%Y"),
                prenom=c.get(st.session_state.prenom_col, ""),
                nom=c.get(st.session_state.nom_col, ""),
                entreprise=get_company(c),
                email=to,
                poste=get_position(c),
                notes="",
            )

            add_draft_to_campaign(
                campaign=campaign_name,
                email=to,
                firstname=c.get(st.session_state.prenom_col, ""),
                lastname=c.get(st.session_state.nom_col, ""),
                subject=subj,
                body=body,
            )

            ok_count += 1
            lines.append(f'<div class="log-ok">✓ {to}</div>')

        except Exception as e:

            err += 1
            lines.append(f'<div class="log-err">✗ {to} — {e}</div>')

        prog.progress((i + 1) / n)
        status.markdown(
            f'<div class="log-info">{i + 1}/{n}</div>',
            unsafe_allow_html=True,
        )
        logs.markdown(
            "\n".join(lines[-8:]),
            unsafe_allow_html=True,
        )

    status.empty()

    summary = (f"✅ {ok_count} mails ajoutés à la campagne.\n"
    "Les brouillons Gmail seront créés automatiquement dans la minute."
        )

    if skipped:
        summary += f" · ⚠️ {skipped} ignoré(s)"

    if err:
        summary += f" · ❌ {err} erreur(s)"

    if err == 0:
        st.success(summary)
    else:
        st.warning(summary)

    logs.markdown(
        "\n".join(lines),
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

