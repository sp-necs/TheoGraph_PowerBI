import pandas as pd
import tkinter
from tkinter import simpledialog
import plotly.express as px
from datetime import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

input_dataset = pd.read_csv('Input_dataset.csv')


# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(Client_ID, Year, Quarter, Month, Day, Event_Desc, Event_ID, Event_Subtype, Event_Type, Year.1, Quarter.1, Month.1, Day.1)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:
dataset = input_dataset
root = tkinter.Tk()
# hide the root window because we only want to show dialogs
root.withdraw()
ask_id = True

while ask_id:
    client_id = simpledialog.askinteger("Client ID", "Enter valid Client ID")
    if client_id in dataset['Client_ID'].unique():
        ask_id = False
    elif client_id is None:
        ask_id = False
    else:
        tkinter.messagebox.showinfo("Error",f"Please enter valid Client ID")
if client_id is not None:
    client_dataset = dataset[dataset["Client_ID"] == client_id]
    client_dataset["Start_Date"] = pd.to_datetime(client_dataset["Start_Date"],format='%d/%m/%Y')
    client_dataset["End_Date"] = pd.to_datetime(client_dataset["End_Date"],format='%d/%m/%Y')
    client_dataset["Updated_End_Date"] = client_dataset["End_Date"].fillna(dt.today())
    event_list = list(client_dataset["Event_Type"].unique())
    for i in event_list:
        client_dataset["Event_Type_Rank"] = [event_list.index(x) for x in client_dataset["Event_Type"]]
    #client_dataset["Event_Type_Rank"] = client_dataset["Event_Type"].rank(method="max")
    client_dataset["Event_Subtype_Rank"] = client_dataset.groupby(["Event_Type"])["Event_Subtype"].rank(method="dense",pct=True)
    client_dataset["Event_Type_Subtype_Rank"] = client_dataset["Event_Type_Rank"] + client_dataset["Event_Subtype_Rank"]

    #st.write(client_dataset)
    client_dataset["Date"] = client_dataset.apply(lambda x: pd.date_range(start=x["Start_Date"],end=x["Updated_End_Date"], freq='D'), axis=1)
    client_dataset = client_dataset.explode("Date")
    # if chart_start_date is not None:
    #     client_dataset = client_dataset[client_dataset["Date"]>=pd.to_datetime(chart_start_date)]
    # if chart_end_date is not None:
    #     client_dataset = client_dataset[client_dataset["Date"]<=pd.to_datetime(chart_end_date)]

    #st.write(client_dataset)
    
    fig = px.line(
        x = client_dataset["Date"],
        y = client_dataset["Event_Type_Subtype_Rank"],
        color = client_dataset["Event_Type"],
        #color_discrete_sequence = ['rgb(204, 204, 204)','rgb(204, 20, 204)'],
        symbol = client_dataset["Event_Subtype"],
        symbol_sequence= ['circle', 'circle-dot', 'square-dot', 'square'],
        title = f"Theograph of client ID '{client_id}'",
        custom_data=[client_dataset["Event_ID"],client_dataset["Start_Date"],client_dataset["End_Date"].fillna("Open"),client_dataset["Event_Desc"]]
    )

    # plt.figure(figsize=(10,6))
    # sns.lineplot(data = client_dataset, x="Date",y="Event_Type_Subtype_Rank", hue="Event_Type", markers="Event_Subtype")
    # plt.show()
    fig.update_layout(
        yaxis = dict(
        showticklabels = False
        ),
        xaxis_title = "Date",
        yaxis_title = "Events"
    )
    fig.update_traces(
        mode = "markers",
        hovertemplate = "Event ID: %{customdata[0]} <br>Start Date: %{customdata[1]} <br>End Date: %{customdata[2]} <br>Event Desc: %{customdata[3]}"
    )
    fig.update_legends(
        title = "Event Type / Subtype"
    )
    fig.update_yaxes(
        showgrid = False
    )
    fig.show()
    # st.divider()
    # st.plotly_chart(fig)

    # export_csv = input_dataset[input_dataset["Client_ID"] == client_id].to_csv(index=False)
    # st.download_button(
    #     label = "Download CSV",
    #     data = export_csv,
    #     file_name = str(dt.today().strftime('%Y%m%d'))+"_"+str(client_id)+".csv",
    #     mime = "text/csv"
    # )
    # input_dataset["Start_Date"] = pd.to_datetime(input_dataset["Start_Date"],format='%d/%m/%Y')
    # input_dataset["End_Date"] = pd.to_datetime(input_dataset["End_Date"],format='%d/%m/%Y')
    # st.dataframe(
    #     input_dataset[input_dataset["Client_ID"] == client_id].sort_values(["Start_Date","End_Date"]),
    #     hide_index=True,
    #     column_config={
    #         "Client_ID" : st.column_config.TextColumn("Client ID"),
    #         "Event_ID" : "Event ID",
    #         "Start_Date" : "Start Date",
    #         "End_Date" : "End Date",
    #         "Event_Type" : "Event Type",
    #         "Event_Subtype" : "Event Subtype",
    #         "Event_Desc" : "Event Description"
    #         }
    #     )