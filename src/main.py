import streamlit as st
import io
import codec as cd

st.set_page_config(page_title="Image Compression", layout="centered")
st.title("🐥 Chibify 🐥")

tab1, tab2 = st.tabs(["🐣 Compress Image", "🐔 Decompress File"])

# ========== Compress ==========
with tab1:
    img_file = st.file_uploader("Upload Image", type="bmp", accept_multiple_files=False)
    if img_file and st.button("Compress"):
        compressed = cd.compress_image(img_file)
        st.success("File Compressed")
        st.download_button(label="Download your compressed file", data=compressed, file_name= (img_file.name.split(".")[0] + ".chibi"), mime="application/octet-stream")
        
with tab2:
    compressed = st.file_uploader("Upload Image", type="chibi", accept_multiple_files=False)
    if compressed and st.button("Decompress"):
        decompressed = cd.decompress_image(compressed)
        file = io.BytesIO()
        decompressed.save(file, format='BMP')
        file.seek(0)
        st.download_button(label="Download your decompressed file", data=file, file_name= (compressed.name.split(".")[0] + ".bmp"), mime = 'image')