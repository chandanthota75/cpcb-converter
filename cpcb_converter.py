import pandas as pa
import streamlit as st


def main():
    st.set_page_config(
        page_title="CPCB file Processor"
    )

    st.title("CPCB file Processor")

    upload_file = st.file_uploader(label="Select the file", accept_multiple_files=False)
    if upload_file is not None:
        dataframe = pa.read_excel(upload_file, sheet_name="Sheet1")

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

        with pa.ExcelWriter('cpcb_converted.xlsx', engine='xlsxwriter') as writer:
            final_dataframe.to_excel(writer, sheet_name='data', index=False)


if __name__ == "__main__":
    main()
