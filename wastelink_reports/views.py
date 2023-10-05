from datetime import datetime
from django.http import HttpResponse
import numpy as np
import pandas as pd

from django.views.decorators.http import condition
column_order = ['Sonipat', 'Jaipur','Jodhpur','Ludhiana','Lucknow', 'Bareilly', 'Kolkata', 'Mumbai', 'Bengaluru', 'Chennai',  'Mangalore', 'Hyderabad', 'Vijaywada','Vizag', 'All']

source_file_ib = r"C://Users//Vikas//Downloads/Daily_Dump.Xlsx"
dest_file_ib = r'C://Users//Vikas//Downloads/Daily_Dump1.csv'
source_file_ob = r"C://Users//Vikas//Downloads/Daily_Dump2.Xlsx"
dest_file_ob = r'C://Users//Vikas//Downloads/Daily_Dump2.csv'

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(source_file_ib)
df1 = pd.read_excel(source_file_ob)

# Save the DataFrame to a CSV file
df.to_csv(dest_file_ib, index=False)
df1.to_csv(dest_file_ob, index=False)

print(f"Data from {source_file_ib} has been converted and saved to {dest_file_ib}.")
print(f"Data from {source_file_ob} has been converted and saved to {dest_file_ob}.")
today = datetime.now()
space = " - "
hub = ["Sonipat","Jaipur","Jodhpur","Ludhiana","Lucknow","Bareilly","Kolkata","Mumbai","Bengaluru","Chennai","Hyderabad","Mangalore","Vijaywada","Vizag"]
Aging_day = ["A. Future Date","B. 0-2","C. 3-4","D. 5-7","E. 8+"]
k_pickup_req_aging = ["A. 0-2","B. 3-4","C. 5+"]
k_pickup_completed_aging = ["A. 0-2","B. 3-4","C. 5+"]
k_pickup_Pending_aging = ["A. 0-2","B. 3-4","C. 5+"]

pickup_status_row_ib = ['New','Pickup Accepted','Pickup Verified','Field Executive Assigned','Field Executive Inspected','WL ID Assigned','Pickup Hold','Request For Cancellation','Planned for Pickup','Vehicle Deployed','Intransit to Wastelink','Pickup Completed','Cancelled','All']
pickup_status_row_ob = ['New','Ready for Dispatch','Request For Cancellation','Planned for Pickup','Vehicle Deployed','Pickup Completed','Cancelled','All']

def aging_report(request):
    df2 = pd.read_csv('C://Users//Vikas//Downloads/Daily_Dump1.csv', low_memory=False)
    df2.loc[(df2['Pickup/Drop Hub'] == "Bareilly-LKO (Bareilly-LKO)"), "Pickup/Drop Hub"] = "Bareilly"
    df2.loc[(df2['Pickup/Drop Hub'] == "Bengaluru (WL-Bengaluru)"), "Pickup/Drop Hub"] = "Bengaluru"
    df2.loc[(df2['Pickup/Drop Hub'] == "Chennai-BLR (Chennai-BLR)"), "Pickup/Drop Hub"] = "Chennai"
    df2.loc[(df2['Pickup/Drop Hub'] == "Hyderabad (Hyderabad-BLR)"), "Pickup/Drop Hub"] = "Hyderabad"
    df2.loc[(df2['Pickup/Drop Hub'] == "Jaipur-SNP (Jaipur-SNP)"), "Pickup/Drop Hub"] = "Jaipur"
    df2.loc[(df2['Pickup/Drop Hub'] == "Jodhpur-SNP (Jodhpur-SNP)"), "Pickup/Drop Hub"] = "Jodhpur"
    df2.loc[(df2['Pickup/Drop Hub'] == "Kolkata-LKO (Kolkata-LKO)"), "Pickup/Drop Hub"] = "Kolkata"
    df2.loc[(df2['Pickup/Drop Hub'] == "Lucknow (WL-Lucknow)"), "Pickup/Drop Hub"] = "Lucknow"
    df2.loc[(df2['Pickup/Drop Hub'] == "Ludhiana-SNP (Ludhiana-SNP)"), "Pickup/Drop Hub"] = "Ludhiana"
    df2.loc[(df2['Pickup/Drop Hub'] == "Mangalore-BLR (Mangalore-BLR)"), "Pickup/Drop Hub"] = "Mangalore"
    df2.loc[(df2['Pickup/Drop Hub'] == "Mumbai (WL-Mumbai)"), "Pickup/Drop Hub"] = "Mumbai"
    df2.loc[(df2['Pickup/Drop Hub'] == "Sonipat (WL-Sonipat)"), "Pickup/Drop Hub"] = "Sonipat"
    df2.loc[(df2['Pickup/Drop Hub'] == "Vijaywada-BLR (Vijaywada-BLR)"), "Pickup/Drop Hub"] = "Vijaywada"
    df2.loc[(df2['Pickup/Drop Hub'] == "Vizag-BLR (Vizag-BLR)"), "Pickup/Drop Hub"] = "Vizag"

    df2['Pickup Datetime'] = pd.to_datetime(df2['Pickup Datetime'])
    today = datetime.now()
    df2['aging_con'] = (today - df2['Pickup Datetime']).dt.days
    df2['Aging_days'] = df2['aging_con'].apply(lambda x: "A. Future Date" if x < 0 else ("B. 0-2" if 0 >= x <= 2 else ("C. 3-4" if 3 >= x <= 4 else ("D. 5-7" if 5 >= x <= 7 else "E. 8+"))))
    filter1 = df2.loc[df2['Pickup Status'] == "WL ID Assigned"]
    filter2 = df2.loc[df2['Pickup Status'] == "Planned for Pickup"]
    filter3 = df2.loc[df2['Pickup Status'] == "Vehicle Deployed"]
    filter4 = df2.loc[df2['Pickup Status'] == "Intransit to Wastelink"]


    aging_table1 = filter1.pivot_table('Req ID', ['Aging_days'], 'Pickup/Drop Hub', aggfunc="count", margins=True)
    columns_in_aging_table1 = list(aging_table1.columns)
    for i in hub:
        if i not in columns_in_aging_table1:
            aging_table1 = aging_table1.assign(**{i: 0})
    aging_table2 = filter2.pivot_table('Req ID', ['Aging_days'], 'Pickup/Drop Hub', aggfunc="count", margins=True)
    columns_in_aging_table2 = list(aging_table2.columns)
    for i in hub:
        if i not in columns_in_aging_table2:
            aging_table2 = aging_table2.assign(**{i: 0})
    aging_table3 = filter3.pivot_table('Req ID', ['Aging_days'], 'Pickup/Drop Hub', aggfunc="count", margins=True)
    columns_in_aging_table3 = list(aging_table3.columns)
    for i in hub:
        if i not in columns_in_aging_table3:
            aging_table3 = aging_table3.assign(**{i: 0})
    aging_table4 = filter4.pivot_table('Req ID', ['Aging_days'], 'Pickup/Drop Hub', aggfunc="count", margins=True)
    columns_in_aging_table4 = list(aging_table4.columns)
    for i in hub:
        if i not in columns_in_aging_table4:
            aging_table4 = aging_table4.assign(**{i: 0})
    aging_table1 = aging_table1[column_order]
    aging_table2 = aging_table2[column_order]
    aging_table3 = aging_table3[column_order]
    aging_table4 = aging_table4[column_order]

    aging_table1.fillna(0, inplace=True)
    aging_table2.fillna(0, inplace=True)
    aging_table3.fillna(0, inplace=True)
    aging_table4.fillna(0, inplace=True)
    aging_pivot1 = aging_table1.astype(int)
    aging_pivot2 = aging_table2.astype(int)
    aging_pivot3 = aging_table3.astype(int)
    aging_pivot4 = aging_table4.astype(int)
    aging_pivot1 = tabulate(aging_table1, headers='keys', tablefmt='html')
    aging_pivot2 = tabulate(aging_table2, headers='keys', tablefmt='html')
    aging_pivot3 = tabulate(aging_table3, headers='keys', tablefmt='html')
    aging_pivot4 = tabulate(aging_table4, headers='keys', tablefmt='html')

    aging = '<div class="report-header">Aging Pivot</div>'
    wlidassigned = '<div class="report-header">Wl ID Assigned</div>'
    plannedforpickup = '<div class="report-header">Planned For Pickup</div>'
    vehicledeployed = '<div class="report-header">Vehicle Deployed Pivot</div>'
    intrasittowastelink = '<div class="report-header">Intrasit To Wastelink</div>'
    agingcss = css_styles = """
             <style>
                /* Style the table */
                table {
                    border-collapse: collapse;
                    text-transform: capitalize first letter;
                    width: 100%;
                    height: 10%;
                    
                }

                /* Style the table headers */
                th {
                    background-color: #ADD8E6;
                    font-weight: 400;
                    text-transform: capitalize first letter;
                    padding: 0.2px;
                    text-align: center;
                    border: 0.5px solid #000;
                }


                /* Style the table data cells */
                td {
                    padding: 0.5px;
                    text-align: left;
                    margin: 10px;
                    border: 1px solid #000;
                    background-color: #rgb(255,2,1);
                }

                /* Apply specific styles to the first column */
                th:first-child,
                td:first-child {
                    background-color: #e0e0e0;
                    text-align: left;
                    font-weight: normal;
                }
                /* Style the report header */
                .report-header {
                    text-align: center;
                    background-color: #f2f2f2;
                    font-weight: bold;
                    border: 1px solid #000; /* Set the border color to black */
                    padding: 5px;
                    font-size: 25px
                }

                /* Style the report footer */
                .report-footer {
                    text-align: center;
                    background-color: #f2f2f2;
                    font-weight: bold;
                    border: 1px solid #000; /* Set the border color to black */
                        padding: 10px;
                }
            </style>
                """
    return HttpResponse(aging+wlidassigned+aging_pivot1+space+plannedforpickup+aging_pivot2+space+vehicledeployed+aging_pivot3+space+intrasittowastelink+aging_pivot4+agingcss)

def pivot(request):
    df1 = pd.read_csv('C://Users//Vikas//Downloads/Daily_Dump2.csv', low_memory=False)
    df = pd.read_csv('C://Users//Vikas//Downloads/Daily_Dump1.csv', low_memory=False)
    df.loc[(df['Pickup/Drop Hub'] == "Bareilly-LKO (Bareilly-LKO)"), "Pickup/Drop Hub"] = "Bareilly"
    df.loc[(df['Pickup/Drop Hub'] == "Bengaluru (WL-Bengaluru)"), "Pickup/Drop Hub"] = "Bengaluru"
    df.loc[(df['Pickup/Drop Hub'] == "Chennai-BLR (Chennai-BLR)"), "Pickup/Drop Hub"] = "Chennai"
    df.loc[(df['Pickup/Drop Hub'] == "Hyderabad (Hyderabad-BLR)"), "Pickup/Drop Hub"] = "Hyderabad"
    df.loc[(df['Pickup/Drop Hub'] == "Jaipur-SNP (Jaipur-SNP)"), "Pickup/Drop Hub"] = "Jaipur"
    df.loc[(df['Pickup/Drop Hub'] == "Jodhpur-SNP (Jodhpur-SNP)"), "Pickup/Drop Hub"] = "Jodhpur"
    df.loc[(df['Pickup/Drop Hub'] == "Kolkata-LKO (Kolkata-LKO)"), "Pickup/Drop Hub"] = "Kolkata"
    df.loc[(df['Pickup/Drop Hub'] == "Lucknow (WL-Lucknow)"), "Pickup/Drop Hub"] = "Lucknow"
    df.loc[(df['Pickup/Drop Hub'] == "Ludhiana-SNP (Ludhiana-SNP)"), "Pickup/Drop Hub"] = "Ludhiana"
    df.loc[(df['Pickup/Drop Hub'] == "Mangalore-BLR (Mangalore-BLR)"), "Pickup/Drop Hub"] = "Mangalore"
    df.loc[(df['Pickup/Drop Hub'] == "Mumbai (WL-Mumbai)"), "Pickup/Drop Hub"] = "Mumbai"
    df.loc[(df['Pickup/Drop Hub'] == "Sonipat (WL-Sonipat)"), "Pickup/Drop Hub"] = "Sonipat"
    df.loc[(df['Pickup/Drop Hub'] == "Vijaywada-BLR (Vijaywada-BLR)"), "Pickup/Drop Hub"] = "Vijaywada"
    df.loc[(df['Pickup/Drop Hub'] == "Vizag-BLR (Vizag-BLR)"), "Pickup/Drop Hub"] = "Vizag"


    df1 = pd.read_csv('C://Users//Vikas//Downloads/Daily_Dump2.csv', low_memory=False)
    df1.loc[(df1['Pickup/Drop Hub'] == "Bareilly-LKO (Bareilly-LKO)"), "Pickup/Drop Hub"] = "Bareilly"
    df1.loc[(df1['Pickup/Drop Hub'] == "Bengaluru (WL-Bengaluru)"), "Pickup/Drop Hub"] = "Bengaluru"
    df1.loc[(df1['Pickup/Drop Hub'] == "Chennai-BLR (Chennai-BLR)"), "Pickup/Drop Hub"] = "Chennai"
    df1.loc[(df1['Pickup/Drop Hub'] == "Hyderabad (Hyderabad-BLR)"), "Pickup/Drop Hub"] = "Hyderabad"
    df1.loc[(df1['Pickup/Drop Hub'] == "Jaipur-SNP (Jaipur-SNP)"), "Pickup/Drop Hub"] = "Jaipur"
    df1.loc[(df1['Pickup/Drop Hub'] == "Jodhpur-SNP (Jodhpur-SNP)"), "Pickup/Drop Hub"] = "Jodhpur"
    df1.loc[(df1['Pickup/Drop Hub'] == "Kolkata-LKO (Kolkata-LKO)"), "Pickup/Drop Hub"] = "Kolkata"
    df1.loc[(df1['Pickup/Drop Hub'] == "Lucknow (WL-Lucknow)"), "Pickup/Drop Hub"] = "Lucknow"
    df1.loc[(df1['Pickup/Drop Hub'] == "Ludhiana-SNP (Ludhiana-SNP)"), "Pickup/Drop Hub"] = "Ludhiana"
    df1.loc[(df1['Pickup/Drop Hub'] == "Mangalore-BLR (Mangalore-BLR)"), "Pickup/Drop Hub"] = "Mangalore"
    df1.loc[(df1['Pickup/Drop Hub'] == "Mumbai (WL-Mumbai)"), "Pickup/Drop Hub"] = "Mumbai"
    df1.loc[(df1['Pickup/Drop Hub'] == "Sonipat (WL-Sonipat)"), "Pickup/Drop Hub"] = "Sonipat"
    df1.loc[(df1['Pickup/Drop Hub'] == "Vijaywada-BLR (Vijaywada-BLR)"), "Pickup/Drop Hub"] = "Vijaywada"
    df1.loc[(df1['Pickup/Drop Hub'] == "Vizag-BLR (Vizag-BLR)"), "Pickup/Drop Hub"] = "Vizag"

    ctr_report_ob = df1.pivot_table('Req ID', ['Pickup Status'], 'Pickup/Drop Hub', aggfunc="count", margins=True)
    columns_in_ctr_report_ob = list(ctr_report_ob.columns)
    for i in hub:
        if i not in columns_in_ctr_report_ob:
            ctr_report_ob = ctr_report_ob.assign(**{i: 0})
    ctr_report_ob.fillna(0, inplace=True)
    outbound = ctr_report_ob.astype(int)
    outbound1=pd.DataFrame(outbound)
    column_order = [9, 4, 13, 6, 5, 0, 14, 8, 1, 2, 7, 3, 10, 11, 12]
    outbound1 = outbound1.iloc[:, column_order]

    outbound1 = tabulate(outbound1, headers='keys', tablefmt='html')

    out = '<div class="report-header">Outbound</div>'
    css_styles = """
         <style>
            /* Style the table */
            table {
                border-collapse: collapse;
                width: 100%;
            }

            /* Style the table headers */
            th {
                background-color: #ADD8E6;
                font-weight: normal;
                padding: 0.2px;
                text-align: center;
                border: 1px solid #000;
            }
            /* Style the table data cells */
            td {
                padding: 1px;
                margin: 10px;
                text-align: left;
                border: 1px solid #000;
                background-color: #rgb(255,2,1);
            }

            /* Apply specific styles to the first column */
            th:first-child,
            td:first-child {
                background-color: #e0e0e0;
                text-align: left;
                font-weight: normal;
            }
            /* Style the report header */
            .report-header {
                text-align: center;
                background-color: #f2f2f2;
                font-weight: bold;
                border: 1px solid #000; /* Set the border color to black */
                padding: 10px;
                font-size: 20px
            }

            /* Style the report footer */
            .report-footer {
                text-align: center;
                background-color: #f2f2f2;
                font-weight: bold;
                border: 1px solid #000; /* Set the border color to black */
                    padding: 10px;
            }
        </style>
            """

    ctr_report_ib = df.pivot_table('Req ID', ['Pickup Status'], 'Pickup/Drop Hub', aggfunc="count", margins=True)
    columns_in_ctr_report_ib = list(ctr_report_ib.columns)
    for i in hub:
        if i not in columns_in_ctr_report_ib:
            ctr_report_ibb = ctr_report_ib.assign(**{i: 0})
    ctr_report_ib.fillna(0, inplace=True)
    inbound=ctr_report_ib.astype(int)
    inbound1=pd.DataFrame(inbound)
    column_order1 = [11, 4, 5, 8, 7, 0, 6, 10, 1, 2, 9, 3, 12, 13, 14]
    inbound1 = inbound1.iloc[:, column_order1]

    inbound1 = tabulate(inbound1, headers='keys', tablefmt='html')

    hd = '<div class="report-header">Control Tower Report</div>'
    inb = '<div class="report-header">Inbound</div>'
    css_styles = """
     <style>
        /* Style the table */
        table {
            border-collapse: collapse;
            width: 100%;
        }
        
        /* Style the table headers */
        th {
            background-color: #FFFF00;
            font-weight: normal;
            padding: 0.5px;
            text-align: center;
            border: 1px solid #000;
        }
        
        
        /* Style the table data cells */
        td {
            padding: 1px;
            text-align: left;
            border: 1px solid #000;
            background-color: #rgb(255,2,1);
        }
        
        /* Apply specific styles to the first column */
        th:first-child,
        td:first-child {
            background-color: #e0e0e0;
            text-align: left;
            margin: 10px;
            font-weight: normal;
        }
        /* Style the report header */
        .report-header {
            text-align: center;
            background-color: #f2f2f2;
            font-weight: bold;
            border: 1px solid #000; /* Set the border color to black */
            padding: 10px;
            font-size: 20px;
        }
        
        /* Style the report footer */
        .report-footer {
            text-align: center;
            background-color: #f2f2f2;
            font-weight: bold;
            border: 1px solid #000; /* Set the border color to black */
                padding: 10px;
        }
    </style>
        """
    inbound1 =  (hd+inb+inbound1+css_styles)
    outbound1 = (out + outbound1 + css_styles)

    return HttpResponse(inbound1+space+outbound1)


def kelloggs_report(request):
    kgr = pd.read_csv('C://Users//Vikas//Downloads/Daily_Dump1.csv', low_memory=False)
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Bareilly-LKO (Bareilly-LKO)"), "Pickup/Drop Hub"] = "Bareilly"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Bengaluru (WL-Bengaluru)"), "Pickup/Drop Hub"] = "Bengaluru"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Chennai-BLR (Chennai-BLR)"), "Pickup/Drop Hub"] = "Chennai"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Hyderabad (Hyderabad-BLR)"), "Pickup/Drop Hub"] = "Hyderabad"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Jaipur-SNP (Jaipur-SNP)"), "Pickup/Drop Hub"] = "Jaipur"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Jodhpur-SNP (Jodhpur-SNP)"), "Pickup/Drop Hub"] = "Jodhpur"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Kolkata-LKO (Kolkata-LKO)"), "Pickup/Drop Hub"] = "Kolkata"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Lucknow (WL-Lucknow)"), "Pickup/Drop Hub"] = "Lucknow"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Ludhiana-SNP (Ludhiana-SNP)"), "Pickup/Drop Hub"] = "Ludhiana"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Mangalore-BLR (Mangalore-BLR)"), "Pickup/Drop Hub"] = "Mangalore"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Mumbai (WL-Mumbai)"), "Pickup/Drop Hub"] = "Mumbai"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Sonipat (WL-Sonipat)"), "Pickup/Drop Hub"] = "Sonipat"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Vijaywada-BLR (Vijaywada-BLR)"), "Pickup/Drop Hub"] = "Vijaywada"
    kgr.loc[(kgr['Pickup/Drop Hub'] == "Vizag-BLR (Vizag-BLR)"), "Pickup/Drop Hub"] = "Vizag"

    kgr['Pickup Datetime'] = pd.to_datetime(kgr['Pickup Datetime'])
    today = datetime.now()
    kgr['kelloggs_req_aging'] = (today - kgr['Pickup Datetime']).dt.days
    kgr['kelloggs_req_aging_cond'] = kgr['kelloggs_req_aging'].apply(lambda x: "A. 0-2" if x <= 2 else ("B. 3-4" if 23 >= x <= 4 else 'C. 5+'))
    kg_r1 = kgr.loc[kgr['Customer/Supplier Name'].str.contains("Kelloggs")]


    kelloggs_final = pd.DataFrame(kg_r1.to_records())
    kelloggs_final.to_csv('C://Users//Vikas//Downloads/kll.csv')
    kelloggs_final.fillna(0, inplace=True)

    kg_r1 = kg_r1.pivot_table('Req ID', ['Distributor State'], 'kelloggs_req_aging_cond', aggfunc="count")
    kg_r1.fillna(0, inplace=True)
    kg_r1 = kg_r1.astype(int)
    kg_r1 = pd.DataFrame(kg_r1)
    kg_r1 = tabulate(kg_r1, headers='keys', tablefmt='html')

    return HttpResponse(kg_r1)

def instockmtddone(request):
    sv = pd.read_csv("D:/wldata/Sep-23/monthly_volume_0923.csv", low_memory=False)
    len(sv.index)

    sv.drop(sv[sv['distributor_name'] == "TestWD"].index, inplace=True)
    sv.drop(sv[sv['customer_name'] == "Bankers Hill Food"].index, inplace=True)
    sv.drop(sv[sv['customer_name'] == "Sukhanand Feed Industries"].index, inplace=True)
    sv.drop(sv[sv['customer_name'] == "Shahi Feed"].index, inplace=True)
    sv.drop(sv[sv['customer_name'] == "Alpha FMCG Pvt. Ltd."].index, inplace=True)
    sv.drop(sv[sv['customer_name'] == "Millennium Feed"].index, inplace=True)
    sv.drop(sv[sv['customer_name'] == "Narmada Poultry Farm"].index, inplace=True)
    sv.drop(sv[sv['customer_name'] == "Nestle DL DB"].index, inplace=True)
    sv.drop(sv[sv['customer_name'].str.contains("Wastelink")].index, inplace=True)

    len(sv.index)

    sv.customer_name = sv['customer_name'].str.strip()
    sv.distributor_name = sv['distributor_name'].str.strip()

    sv.loc[sv.ticket_id == "ID-1648", "scheduled_date"] = "2020-09-18"
    sv['datef'] = sv['scheduled_date'].apply(str)
    sv['datef'] = sv['scheduled_date'].str[:7]
    sv['datef'] = sv['datef'].apply(str)
    sv.fillna(0, inplace=True)
    len(sv.index)

    # Alternate Option : Utilizing pandas functions for faster execution
    sv['new_date'] = pd.to_datetime(sv['pickup_date']).dt.strftime('%Y-%m-%d').where(sv['pickup_date'] != 0,
                                                                                     sv['scheduled_date'])
    sv['newdatef'] = pd.to_datetime(sv['new_date']).dt.strftime('%Y-%m')

    print(sv.status.unique())

    final = sv.pivot_table('item_weight', ['customer_name'], 'newdatef', aggfunc="sum")
    final.fillna(0, inplace=True)

    sv_final = pd.DataFrame(final.to_records())
    sv_final.to_csv('D://wldata/Sep-23/output_0923.csv')
    sv_final.fillna(0, inplace=True)

    # MTD Break instock vs shipment picked

    instockmtd = sv[sv['status'].str.contains('Instock Mark Done')]
    instockmtd = instockmtd[instockmtd['newdatef'].str.contains('2023-09')]
    # instockmtd=instockmtd.pivot_table('item_weight', ['customer_name','ticket_id'], 'newdatef',aggfunc = "sum")
    instockmtd = instockmtd.pivot_table('item_weight', ['customer_name'], 'newdatef', aggfunc="sum")
    instockmtd = pd.DataFrame(instockmtd.to_records())
    #instockmtd.to_csv('D://Wldata/Sep-23//instockmt_0922.csv')

    # instockmtd.to_csv('D://Wldata/Mar//instockmt_DATA.csv')
    instockmtd = tabulate(instockmtd, headers='keys', tablefmt='html')
    return HttpResponse(instockmtd)

def suppliervolume(request):
    svq = pd.read_csv('D://wldata/Sep-23/monthly_volume_0923.csv', low_memory=False)
    len(svq.index)

    svq.drop(svq[svq['distributor_name'] == "TestWD"].index, inplace=True)
    svq.drop(svq[svq['customer_name'] == "Narmada Poultry Farm"].index, inplace=True)
    svq.drop(svq[svq['customer_name'] == "Nestle DL DB"].index, inplace=True)
    svq.drop(svq[svq['customer_name'].str.contains("Wastelink")].index, inplace=True)

    len(svq.index)
    #print()

    svq.customer_name = svq['customer_name'].str.strip()
    svq.distributor_name = svq['distributor_name'].str.strip()
    svq.loc[svq.ticket_id == "ID-1648", "scheduled_date"] = "2020-09-18"
    svq.fillna(0, inplace=True)

    # Alternate Option : Utilizing pandas functions for faster execution
    svq['new_date'] = pd.to_datetime(svq['pickup_date']).dt.strftime('%Y-%m-%d').where(svq['pickup_date'] != 0,
                                                                                     svq['scheduled_date'])
    svq['newdatef'] = pd.to_datetime(svq['new_date']).dt.strftime('%Y-%m')

    final = svq.pivot_table('item_weight', ['customer_name'], 'newdatef', aggfunc="sum")
    final.fillna(0, inplace=True)
    svq1_final = pd.DataFrame(final.to_records())
    svq1_final.to_csv('D://Wldata/Sep-23/output_0923.csv')
    svq1_final.fillna(0, inplace=True)
    #svq1.to_csv('D://wldata/Sep-23/df1.csv')
    svq1_final.to_csv("output.csv")

    # itcmum_df = df[df['customer_name'] =="ITC Mumbai Distributors"]
    # mumdisfinal=itcmum_df.pivot_table('item_weight', ['distributor_name'], 'newdatef',aggfunc = "sum")
    # mum=pd.DataFrame(mumdisfinal.to_records())

    # mum.to_csv('D://wldata/Sep-23/mumdist_0918.csv')

    svq1_final = tabulate(svq1_final, headers='keys', tablefmt='html')
    return HttpResponse(svq1_final)


from tabulate import tabulate
clickbutton = ('''<div class="div_"><a href="\pivot" class="btn">View CTR Report</a></div>''')
clickbutton1 = ('''<div class="div_"> <a href="\\aging_report" class="btn">View Aging Report</a></div>''')
clickbutton2 = ('''<div class="div_"> <a href="\instockmtddone" class="btn">Instock MTD Done</a></div>''')
clickbutton3 = ('''<div class="div_"> <a href="\suppliervolume" class="btn">Supplier Volume</a></div>''')
clickbutton4 = ('''<div class="div_"> <a href="\kelloggs_report" class="btn">Kellogs reports</a></div>''')



welcome_page = '<div class="down center"><h1>Welcome to Reports</h1></div>'

css_style1 = """
     <style>
     html {
  
     
  background-color: #10151B;
  background: url('http://logistics.wastelink.co/assets/img/wastelink_logo_new.png') no-repeat center top ;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: auto;
  background-size: 400px 300px;
  margin-top: 10px
}

body {
  font-family: "Oswald", sans-serif;
  -webkit-font-smoothing: antialiased;
  font-smoothing: antialiased;
    display: block;
    
    margin: 100px;
    margin-top: 10px;
    margin-right: 100px;
    margin-bottom: 1em;
    margin-left: 100px;
    text-align: center;
    
}

h1 {
  line-height: .95;
  color: #000;
  font-weight: 900;
  font-size: 50px;
  text-transform: uppercase;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  pointer-events: none;
}

.center {
  display: flex;
    justify-content: center;
    align-items: center;
  position: absolute;
  margin: auto;
  top: 300;
  left: 0;
  right: 0;
  bottom: 0;
  width: 700px;
  height: 10%;
}

.div_ {
    display: inline-block; /* Make the div a block element */
    padding: 5px 5px; /* Adjust the padding for width and height */
    font-size: 15px; /* Reduce the font size */
     
  margin-top: 363px;
  margin-right: 10px;
  width: 300px;
  height: 50px;
  padding: 1px 0 0 5px;
  border: 2.5px solid #66fcf1;
  border-radius: 20px;
  font-size: 18px;
  line-height: 54px;
  color: #000;
  letter-spacing: .25em;
 
  font-weight: 800;
  text-transform: uppercase;
  vertical-align: middle;
  text-align: center;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  -webkit-transition: background .3s, color .4s;
  transition: background .4s, color .4s;

}

.btn {
  background: #FFFFFF;
  color: #none;
   text-decoration: none;
   cursor: pointer;
   
}

</style> """
def home(request):

    #return HttpResponse('''<a href="\pivot">View CTR Report</a>''')
    return HttpResponse(clickbutton+clickbutton1+clickbutton2+clickbutton3+clickbutton4+welcome_page+css_style1)