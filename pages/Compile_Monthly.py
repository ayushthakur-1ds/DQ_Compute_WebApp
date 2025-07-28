import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import streamlit as st
import pandas as pd
from datetime import datetime

from utils import execution, download_bytes



def show():
    st.title("📊 DQ KPI Calculations App - Monthly/MTD")

    # Step 1: Date inputs
    col1, col2 = st.columns(2)
    with col1:
        from_date = st.date_input("From Date:")
    with col2:
        to_date = st.date_input("To Date:")

    # Validate date range
    if from_date > to_date:
        st.error("❌ 'From Date' cannot be after 'To Date'. Please select a valid range.")
        return

    # Step 2: Checkboxes
    st.markdown("### Select Sections For Compilation")
    selected_sections = []

    col1, col2 = st.columns(2)
    with col1:
        availability = st.checkbox("Availability")
        sov = st.checkbox("Share Of Visibility Search")
        sprinklr = st.checkbox("Sprinklr (Ecom + Social)")
    with col2:
        gs_calc = st.checkbox("ON-OFF Platform GS Calc")
        performance = st.checkbox("Performance Marketing")

    if availability: selected_sections.append("Availability")
    if sov: selected_sections.append("Share Of Visibility Search")
    if sprinklr: selected_sections.append("Sprinklr (Ecom + Social)")
    if gs_calc: selected_sections.append("ON-OFF Platform GS Calc")
    if performance: selected_sections.append("Performance Marketing")

    # Step 3: Show file inputs immediately if Sprinklr selected
    file1 = file2 = file3 = None
    missing_files = []

    if sprinklr:
        st.markdown("#### Upload required files for Sprinklr (Ecom + Social)")
        file1 = st.file_uploader("Upload FileName1.xlsx", type=["xlsx"], key="sprinklr1")
        file2 = st.file_uploader("Upload FileName2.xlsx", type=["xlsx"], key="sprinklr2")
        file3 = st.file_uploader("Upload FileName3.xlsx", type=["xlsx"], key="sprinklr3")

        # Realtime validation
        if file1 and file1.name != "FileName1.xlsx":
            st.error("❌ Incorrect file: Expected FileName1.xlsx")
        if file2 and file2.name != "FileName2.xlsx":
            st.error("❌ Incorrect file: Expected FileName2.xlsx")
        if file3 and file3.name != "FileName3.xlsx":
            st.error("❌ Incorrect file: Expected FileName3.xlsx")

        if not file1 or file1.name != "FileName1.xlsx":
            missing_files.append("FileName1.xlsx")
        if not file2 or file2.name != "FileName2.xlsx":
            missing_files.append("FileName2.xlsx")
        if not file3 or file3.name != "FileName3.xlsx":
            missing_files.append("FileName3.xlsx")

    # Step 4: Compile button
    # Step 4: Compile button
    if st.button("✅ Compile Files"):
        if sprinklr and missing_files:
            st.error(f"❌ Cannot compile. Missing or incorrect files: {', '.join(missing_files)}")
        else:
            with st.spinner("🌀 Compilation in progress... Check logs to see real-time progress."):
                raw_data_dict, final_dfs = execution.monthly_compile(selected_sections, from_date, to_date, "FY2025 Q3 OND")

                st.session_state["calc_zip_file"] = download_bytes.build_zip(raw_data_dict)
                st.session_state["final_compiled_file"] = download_bytes.merge_final_file(final_dfs)
                st.session_state["from_date_str"] = from_date.strftime("%Y-%b-%d")
                st.session_state["to_date_str"] = to_date.strftime("%Y-%b-%d")

            st.success("🎉 YAY! ITS DONE")

    # Step 5: Show download buttons if files are ready
    if "calc_zip_file" in st.session_state and "final_compiled_file" in st.session_state:
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="⬇️ Download Raw Data (ZIP)",
                data=st.session_state["calc_zip_file"],
                file_name=f"CalcFile Data {st.session_state['from_date_str']}-{st.session_state['to_date_str']}.zip",
                mime="application/zip",
                key="download_zip"
            )

        with col2:
            st.download_button(
                label="⬇️ Download Merged Final Formatted Output",
                data=st.session_state["final_compiled_file"],
                file_name=f"Merged_Final_Output {st.session_state['from_date_str']}-{st.session_state['to_date_str']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_final"
            )


        st.success("🎉 Download the files above ")

    # Step 5: Section Summary
    # st.markdown("### ✅ Sections Selected:")
    # st.write(selected_sections)


show()
