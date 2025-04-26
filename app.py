import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import time

# --- Use a Fixed Key ---
KEY = b'Pb2d20XtUvZx4dBRkU7shW8QpZy0bm-Tv9Q7JQKoO1M='
cipher = Fernet(KEY)

st.set_page_config(page_title="Secure Data Vault", layout="centered")

# --- Session State ---
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "reauthorized" not in st.session_state:
    st.session_state.reauthorized = True

# --- Helper Functions ---
def hash_passkey(passkey: str) -> str:
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text: str, passkey: str):
    hashed = hash_passkey(passkey)
    data = st.session_state.stored_data.get(encrypted_text)

    if data:
        if time.time() > data["expiry"]:
            return "⏰ Data Expired!"

        if data["passkey"] == hashed:
            try:
                decrypted = cipher.decrypt(encrypted_text.encode()).decode()
                st.session_state.failed_attempts = 0
                return decrypted
            except Exception:
                return None
        else:
            st.session_state.failed_attempts += 1
            return None
    else:
        return None

def reset_attempts():
    st.session_state.failed_attempts = 0
    st.session_state.reauthorized = True

# --- Sidebar ---
st.sidebar.title("🔐 Secure Data System")
page = st.sidebar.radio("Navigate", ["🏠 Home", "📦 Store Data", "🔍 Retrieve Data", "📂 View Stored", "🔑 Login"])

# --- Home Page ---
if page == "🏠 Home":
    st.title("🛡️ Secure Data Encryption System")
    st.write("Welcome! This app allows you to securely **encrypt and store your data** using a unique passkey.")
    st.markdown("""
    - 🔐 Encrypted using `Fernet` encryption  
    - 🔑 Passkeys are hashed using SHA-256  
    - ⏳ Option to auto-expire data  
    - 🚫 Access is blocked after 3 failed attempts  
    """)
    st.info("Use the sidebar to navigate.")

# --- Store Data ---
elif page == "📦 Store Data":
    st.header("📦 Store Your Secret Data")

    user_input = st.text_area("Enter the secret data you want to encrypt")
    user_pass = st.text_input("Create a Passkey", type="password")
    expire_after = st.slider("Set Data Expiry (in minutes)", 1, 60, 10)

    if st.button("🔐 Encrypt & Store"):
        if user_input and user_pass:
            encrypted = encrypt_data(user_input)
            hashed_passkey = hash_passkey(user_pass)
            expiry_time = time.time() + (expire_after * 60)

            st.session_state.stored_data[encrypted] = {
                "encrypted_text": encrypted,
                "passkey": hashed_passkey,
                "expiry": expiry_time
            }

            st.success("✅ Your data is securely stored!")

            with st.expander("🔒 Show Encrypted Text"):
                st.code(encrypted, language="text")

            st.download_button("⬇️ Download Encrypted Text", encrypted, file_name="secret.txt")
        else:
            st.warning("⚠️ Both fields are required!")

# --- Retrieve Data ---
elif page == "🔍 Retrieve Data":
    if st.session_state.failed_attempts >= 3 and not st.session_state.reauthorized:
        st.error("🚫 Access Denied! Too many failed attempts.")
        st.stop()

    st.header("🔍 Retrieve Your Secret")

    enc_input = st.text_area("Paste Encrypted Text")
    passkey = st.text_input("Enter Your Passkey", type="password")

    if st.button("🔓 Decrypt"):
        if enc_input and passkey:
            result = decrypt_data(enc_input, passkey)
            if result == "⏰ Data Expired!":
                st.error("⏰ This data has expired.")
            elif result:
                st.success("✅ Successfully Decrypted!")
                st.code(result, language="text")
            else:
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Invalid passkey or corrupted text! Attempts remaining: {remaining}")
        else:
            st.warning("⚠️ Please fill in both fields.")

# --- View Stored Data ---
elif page == "📂 View Stored":
    st.header("📂 Stored Encrypted Data")

    if st.session_state.stored_data:
        for i, (k, v) in enumerate(st.session_state.stored_data.items(), 1):
            with st.expander(f"🔐 Entry #{i}"):
                st.write("Encrypted:", k[:50] + "...")
                remaining_time = int(v["expiry"] - time.time())
                minutes_left = max(0, remaining_time // 60)
                st.write(f"⏳ Time left: {minutes_left} min")
    else:
        st.info("📭 No data stored yet.")

# --- Login Page ---
elif page == "🔑 Login":
    st.header("🔐 Admin Reauthorization")
    master_key = st.text_input("Enter Admin Password", type="password")

    if st.button("🔓 Reauthorize"):
        if master_key == "admin123":
            reset_attempts()
            st.success("✅ Access Restored! You may now try again.")
        else:
            st.error("❌ Incorrect admin password!")