# 🔐 PII Masking Tool (ID Card Redaction AI)

Automatically detect and mask Personally Identifiable Information (PII) like names, addresses, Aadhaar numbers, phone numbers, and more from uploaded ID card images — using OCR + AI.

---

## 🚀 Features

- 🔍 Detects sensitive PII from Aadhaar, PAN, Voter ID, Passport, etc.
- 🧠 Uses EasyOCR (multilingual) to extract text (English + Hindi)
- 🧼 Masks names, addresses, DOB, Aadhaar/PAN numbers, phone & emails
- ⚙️ Built with FastAPI + OpenCV + Regex + React frontend
- 🌗 Dark/light mode toggle
- 🖼 Instant preview & download of masked output
- 💡 Clean, modern UI without Tailwind (pure CSS Modules)

---

## 🧠 Tech Stack

| Layer     | Tool/Library         | Purpose                         |
|-----------|----------------------|---------------------------------|
| Frontend  | React + Vite         | Fast UI rendering               |
| Styling   | CSS Modules          | Scoped component styling        |
| OCR       | EasyOCR              | Extracts text from image        |
| Detection | Regex + Keywords     | Detects Aadhaar, phone, DOB etc |
| Masking   | OpenCV               | Draws black boxes on image      |
| Backend   | FastAPI              | Handles upload + response       |

---

## 📸 Example

Upload Aadhaar/PAN card → tool auto-detects:

- 👤 **Full Name**
- 🏠 **Address** (multi-line)
- 🎂 **Date of Birth**
- 🔢 **Aadhaar Number**
- 📞 **Phone Number**
- 📧 **Email**

→ And masks them with black rectangles before returning the image ✅

---

## 🤖 How It Works

1. 🧠 **EasyOCR** reads text from uploaded image  
2. 🕵️ **Regex + keywords** detect sensitive PII like Aadhaar, phone, DOB  
3. 🧱 **OpenCV** draws black masking boxes on the image  
4. ⚡ **FastAPI** returns the final masked image as a stream  
5. 💻 **Frontend** previews both original & masked image with download button

## 🙌 Author

Built with ❤️ by [manishjr](https://github.com/manishjr18)

---

## 📄 License

MIT License – use freely, modify as needed.

---
