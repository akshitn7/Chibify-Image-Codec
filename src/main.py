import streamlit as st
from PIL import Image
import io
import zipfile

from codec import compress_image_stream, decompress_image_stream

st.set_page_config(page_title="Image Compression", layout="centered")
st.title("🗜️ Huffman Image Compression")

tab1, tab2 = st.tabs(["📤 Compress Image", "📥 Decompress File"])

# ========== Compress ==========
with tab1:
    uploaded_imgs = st.file_uploader("Upload image(s)", type=["png", "jpg", "jpeg", "bmp"], accept_multiple_files=True)
    
    if uploaded_imgs:
        st.write(f"{len(uploaded_imgs)} image(s) selected.")
        results = []

        if st.button("Compress"):
            for img_file in uploaded_imgs:
                img = Image.open(img_file)
                compressed_bytes = compress_image_stream(img)
                results.append((img_file.name.rsplit('.', 1)[0] + ".huff", compressed_bytes))

            # ZIP results
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w") as zipf:
                for fname, data in results:
                    zipf.writestr(fname, data)
            zip_buf.seek(0)

            st.success("Compression complete!")
            st.download_button("📦 Download All as ZIP", zip_buf, file_name="compressed_images.zip")

# ========== Decompress ==========
with tab2:
    uploaded_huff = st.file_uploader("Upload .huff file", type=["huff"])

    if uploaded_huff and st.button("Decompress"):
        decompressed_img = decompress_image_stream(uploaded_huff.read())
        st.image(decompressed_img, caption="Decompressed Image", use_column_width=True)

        buf = io.BytesIO()
        decompressed_img.save(buf, format="PNG")
        buf.seek(0)
        st.download_button("Download as PNG", buf, file_name="decompressed.png", mime="image/png")
