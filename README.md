# 🔐 Secure Data Encryption System

A secure web application built with Streamlit that allows users to encrypt, store, and retrieve sensitive data using strong encryption methods.

## 🚀 Features

- 🔐 **Secure Encryption**: Uses Fernet encryption for data security
- 🔑 **Passkey Protection**: Passkeys are hashed using SHA-256
- ⏳ **Auto-Expiry**: Option to set expiration time for stored data
- 🚫 **Security Measures**: Access blocked after 3 failed attempts
- 📦 **Data Storage**: Secure storage of encrypted data
- 🔍 **Easy Retrieval**: Simple interface for data retrieval
- 📂 **Data Management**: View all stored encrypted data

## 🛠️ Technical Details

- Built with Python and Streamlit
- Uses `cryptography.fernet` for encryption
- Implements SHA-256 hashing for passkeys
- Session-based data storage
- Automatic data expiration system

## 📋 Pages

1. **🏠 Home**: Overview of the system
2. **📦 Store Data**: Encrypt and store new data
3. **🔍 Retrieve Data**: Decrypt and retrieve stored data
4. **📂 View Stored**: View all stored encrypted data
5. **🔑 Login**: Admin reauthorization page

## 🔒 Security Features

- Fixed encryption key for data security
- Passkey hashing for additional security
- Failed attempt tracking
- Admin reauthorization system
- Automatic data expiration

## 🚨 Important Notes

- The system blocks access after 3 failed decryption attempts
- Stored data automatically expires based on set time
- Admin password is required for reauthorization
- All passkeys are hashed and never stored in plain text

## ⚙️ Setup

1. Install required packages:
```bash
pip install streamlit cryptography
```

2. Run the application:
```bash
streamlit run app.py
```

## 📝 Usage

1. **Storing Data**:
   - Enter your secret data
   - Create a passkey
   - Set expiration time
   - Click "Encrypt & Store"

2. **Retrieving Data**:
   - Paste the encrypted text
   - Enter your passkey
   - Click "Decrypt"

3. **Viewing Stored Data**:
   - Access the "View Stored" page
   - See all encrypted entries
   - Check remaining time for each entry

## ⚠️ Disclaimer

This application is for demonstration purposes. For production use, additional security measures should be implemented. "# Secure-Data-Encryption" 
"# Secure-Data-Encryption" 
