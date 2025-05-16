from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pii_utils import process_image
from io import BytesIO
import os

app = FastAPI()

# ✅ CORS Setup: Allow frontend requests (like from React/Vite on localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with ["http://localhost:5173"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # ✅ Step 1: Read the uploaded file
        contents = await file.read()
        input_path = f"sample_images/{file.filename}"

        # Make sure directory exists
        os.makedirs("sample_images", exist_ok=True)

        with open(input_path, "wb") as f:
            f.write(contents)

        print(f"📥 Image saved at {input_path}")

        # ✅ Step 2: Process image to mask PII
        output_image = process_image(input_path)
        print(f"✅ Image processed successfully")

        # ✅ Step 3: Convert image to stream and return as response
        buffer = BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")

    except Exception as e:
        print("❌ Error occurred:", str(e))
        return JSONResponse(status_code=500, content={"error": "Something went wrong while processing the image."})
