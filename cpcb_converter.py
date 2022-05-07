import pandas as pa
from io import BytesIO
import streamlit as st


def main():
    st.set_page_config(
        page_title="CPCB file Processor"
    )

    st.markdown('<style>h1, p, h3 {text-align: center;} div[class="row-widget stDownloadButton"] {text-align: c'
                'enter;}</style>', unsafe_allow_html=True)

    st.title("CPCB file Processor")

    upload_file = st.file_uploader(label="Select the file", accept_multiple_files=False)
    if upload_file is not None:
        dataframe = pa.read_excel(upload_file, sheet_name="Sheet1")
        st.subheader("")
        st.success("The file uploaded successfully")
        st.subheader("")
        dataframe.drop(dataframe.head(15).index, inplace=True)
        dataframe = (dataframe.astype(str).reset_index()).drop(["index"], axis=1)

        index = dataframe[dataframe["CENTRAL POLLUTION CONTROL BOARD"] == "Remarks"].index.values.tolist()

        first_half = (dataframe[: index[0] - 3].reset_index()).drop(["index"], axis=1).rename(columns=dataframe.iloc[0])
        second_half = dataframe[index[0] + 1: index[1] - 3].reset_index().drop(["index"], axis=1)
        third_half = dataframe[index[1] + 1: index[2] - 3].reset_index().drop(["index"], axis=1)
        fourth_half = dataframe[index[2] + 1:].reset_index().drop(["index"], axis=1)

        first_half = first_half.tail(first_half.shape[0] - 1)
        second_half = second_half.rename(columns=second_half.iloc[0]).drop(["From Date", "To Date"], axis=1).tail(
            second_half.shape[0] - 1)
        third_half = third_half.rename(columns=third_half.iloc[0]).drop(["From Date", "To Date"], axis=1).tail(
            third_half.shape[0] - 1)
        fourth_half = fourth_half.rename(columns=fourth_half.iloc[0]).drop(["From Date", "To Date", "nan"],
                                                                           axis=1).tail(fourth_half.shape[0] - 1)

        final_dataframe = pa.concat([first_half, second_half, third_half, fourth_half],
                                    axis=1, join='inner').reset_index().drop(["index"], axis=1)

        def excel_file_converter(df):
            output = BytesIO()
            writer = pa.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            worksheet = writer.sheets['Sheet1']
            worksheet.set_column('A:A', None)
            writer.save()
            data_encoded = output.getvalue()
            return data_encoded

        df_xlsx = excel_file_converter(final_dataframe)
        if df_xlsx:
            name = st.text_input("Enter the file name with extension (.xlsx)")
            if name:
                st.subheader("")
                st.success("The file is ready to download")
                st.subheader("")
                st.download_button(label='📥 Download the file',
                                   data=df_xlsx,
                                   file_name=f'{name}')
        else:
            st.info("The file is processing")


if __name__ == "__main__":
    main()
