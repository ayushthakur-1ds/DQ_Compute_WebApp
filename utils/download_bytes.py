import io
import zipfile
import pandas as pd


def build_zip(raw_data_dict: dict):
    '''This function will create a zip file containing separate excel raw/calc files for selected KPIs'''

    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for section_name, dfs in raw_data_dict.items():
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                    for i, df in enumerate(dfs):
                        sheet_name = f"{section_name[:25]}_{i+1}"
                        df.to_excel(writer, index=False, sheet_name=sheet_name)

                excel_buffer.seek(0)
                zip_file.writestr(f"{section_name}_Raw.xlsx", excel_buffer.getvalue())
        zip_buffer.seek(0)

        return zip_buffer

    except Exception as e:
        print("There is an error while making a zip file of calc files.")
        print(e)



def merge_final_file(final_dfs: list):
    '''This function returns a final formatted file with combined data for all selected KPIs'''

    try:
        if final_dfs:
            merged_final_df = pd.concat(final_dfs, ignore_index=True)
            final_excel = io.BytesIO()
            with pd.ExcelWriter(final_excel, engine="openpyxl") as writer:
                merged_final_df.to_excel(writer, index=False, sheet_name="Final")

            final_excel.seek(0)

            return final_excel
        
    except Exception as e:
        print("There is an error while merging final formatted files.")

    




