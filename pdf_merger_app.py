import streamlit as st
from PyPDF2 import PdfFileReader, PdfFileWriter
import io
import base64

# Streamlit UI
st.title("PDF Merger")

uploaded_files = st.file_uploader("Upload PDF files to merge", accept_multiple_files=True)

if uploaded_files:
    merged_pdf = PdfFileWriter()
    corrupted_files = []

    for file in uploaded_files:
        try:
            pdf_reader = PdfFileReader(file)
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                merged_pdf.addPage(page)
        except Exception as e:
            corrupted_files.append(file.name)
            st.warning(f"Skipping {file.name} due to an error: {str(e)}")

    if corrupted_files:
        st.warning(f"The following files could not be merged due to errors: {', '.join(corrupted_files)}")

    if merged_pdf.getNumPages() > 0:
        st.write("Merged PDF successfully!")

        # Create a download link
        download_button = st.button("Download Merged PDF")

        if download_button:
            output_pdf = io.BytesIO()
            merged_pdf.write(output_pdf)
            pdf_bytes = output_pdf.getvalue()

            # Provide download link
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="merged.pdf">Download Merged PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("No valid PDF files were merged.")
