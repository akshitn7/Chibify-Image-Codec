import streamlit as st
import io
import codec as cd

st.set_page_config(page_title="Image Compression", layout="centered")
st.title("🐥 Chibify 🐥")

tab1, tab2 = st.tabs(["🐣 Compress Image", "🐔 Decompress File"])

# ========== Compress ==========
with tab1:
    img_files = st.file_uploader("Upload Images (up to 10)", type="bmp", accept_multiple_files=True)
    if img_files and len(img_files) > 10:
        st.warning("Please upload up to 10 files only.")
    elif img_files and st.button("Compress"):
        try:
            compressed_files = []
            for img_file in img_files:
                compressed = cd.compress_image(img_file)
                compressed_files.append((img_file.name.rsplit('.', 1)[0] + ".chibi", compressed))
            st.success(f"{len(compressed_files)} files compressed successfully! Download below:")
            for filename, data in compressed_files:
                st.download_button(
                    label=f"Download {filename}",
                    data=data,
                    file_name=filename,
                    mime="application/octet-stream"
                )
        except Exception as e:
            st.error(f"An error occurred during compression: {e}")

# ========== Decompress ==========
with tab2:
    compressed = st.file_uploader("Upload Compressed File", type="chibi", accept_multiple_files=False)
    if compressed and st.button("Decompress"):
        try:
            decompressed = cd.decompress_image(compressed)
            file = io.BytesIO()
            decompressed.save(file, format='BMP')
            file.seek(0)
            st.download_button(
                label="Download your decompressed file",
                data=file,
                file_name=(compressed.name.split(".")[0] + ".bmp"),
                mime='image/bmp',
            )
        except Exception as e:
            st.error(f"An error occurred during decompression: {e}")

