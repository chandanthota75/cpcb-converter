import pandas as pa
from io import BytesIO
import streamlit as st
import bhopal_converter
import mandideep_converter


def excel_file_converter(df):
    output = BytesIO()
    writer = pa.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:A', None)
    writer.save()
    data_encoded = output.getvalue()

    if data_encoded:
        name = st.text_input("Enter the file name with extension (.xlsx)")
        if name:
            st.subheader("")
            st.success("The file is ready to download")
            st.subheader("")
            st.download_button(label='📥 Download the file',
                               data=data_encoded,
                               file_name=f'{name}')
    else:
        st.info("The file is processing")


def main():
    st.set_page_config(
        page_title="CPCB file converter",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    st.markdown('<style>h1, p, h3 {text-align: center;} div[class="row-widget stDownloadButton"] {text-align: c'
                'enter;}</style>', unsafe_allow_html=True)
    st.sidebar.title("CPCB Excel Converter")

    pages_list = ["Bhopal", "Mandideep"]
    page = st.sidebar.radio("GO TO", pages_list)

    if page == "Bhopal":
        bhopal_converter.main()
    if page == "Mandideep":
        mandideep_converter.main()


if __name__ == "__main__":
    main()
