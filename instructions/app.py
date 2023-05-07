from flask import Flask, render_template, Response, request
import psycopg2
import pandas as pd
import plotly.graph_objs as go

import io
import csv


import mpld3
import json

app = Flask(__name__)

#   DB Connect

def get_db_conn():
    #  Connect to PostgreSQL database
    conn = psycopg2.connect(dbname="brx1", 
                            user="process_trending", 
                            password="abc123", 
                            host="localhost")
    return conn

@app.route('/', methods=['GET', 'POST']) 

#   Display Plots and Tables

def index():
    
    conn = get_db_conn()
    cursor = conn.cursor()

    

    # table 1 begin
    
    if request.method == "POST":
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        cursor.execute('SELECT * FROM public."CM_HAM_DO_AI1/Temp_value" WHERE time BETWEEN %s AND %s;', (start_time, end_time))
        table1_data = cursor.fetchall()
    
    else:
        # Execute the SQL query to retrieve the data from the database
        cursor.execute('SELECT * FROM public."CM_HAM_DO_AI1/Temp_value" LIMIT 5;')
        table1_data = cursor.fetchall()
    
    # cursor.execute(f'SELECT * FROM public."CM_HAM_DO_AI1/Temp_value" LIMIT 5;')
    # table1_data = cursor.fetchall()
    # Extract the timestamp and value data from the database result
    timestamps = [row[0] for row in table1_data]
    values = [row[1] for row in table1_data]

    # Create a line chart with the timestamp and value data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=values, mode='lines'))

    # Set the chart title and axis labels
    fig.update_layout(title='Temperature Vs Time', xaxis_title='Time', yaxis_title='Temperature')

    # Render the chart in the Flask template
    chart1 = fig.to_html(full_html=False)

    
    # table 1 done
    
    # table 2 begin
    
    if request.method == "POST":
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        cursor.execute('SELECT * FROM public."CM_HAM_PH_AI1/pH_value" WHERE time BETWEEN %s AND %s;', (start_time, end_time))
        table2_data = cursor.fetchall()
    
    else:
        # Execute the SQL query to retrieve the data from the database
        cursor.execute('SELECT * FROM public."CM_HAM_PH_AI1/pH_value" LIMIT 5;')
        table2_data = cursor.fetchall()
    
    # Execute the database query and extract the timestamp and value data
    # cursor.execute(f'SELECT * FROM public."CM_HAM_PH_AI1/pH_value" LIMIT 5;')
    # table2_data = cursor.fetchall()
    timestamps = [row[0] for row in table2_data]
    values = [row[1] for row in table2_data]

    # Create a line chart with the timestamp and value data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=values, mode='lines'))

    # Set the chart title and axis labels
    fig.update_layout(title='pH Value Vs Time', xaxis_title='Time', yaxis_title='pH_value')

    # Render the chart in the Flask template
    chart2 = fig.to_html(full_html=False)
    
    # table 2 done
    
    # table 3 begin
    
    if request.method == "POST":
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        cursor.execute('SELECT * FROM public."CM_PID_DO/Process_DO" WHERE time BETWEEN %s AND %s;', (start_time, end_time))
        table3_data = cursor.fetchall()
    
    else:
        # Execute the SQL query to retrieve the data from the database
        cursor.execute('SELECT * FROM public."CM_PID_DO/Process_DO" LIMIT 5;')
        table3_data = cursor.fetchall()
    
    # Execute the database query and extract the timestamp and value data
    # cursor.execute(f'SELECT * FROM public."CM_PID_DO/Process_DO" LIMIT 5;')
    # table3_data = cursor.fetchall()
    timestamps = [row[0] for row in table3_data]
    values = [row[1] for row in table3_data]

    # Create a line chart with the timestamp and value data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=values, mode='lines'))

    # Set the chart title and axis labels
    fig.update_layout(title='Process_DO Vs Time', xaxis_title='Time', yaxis_title='Process_DO')

    # Render the chart in the Flask template
    chart3 = fig.to_html(full_html=False)
    # table 3 done
    
    # table 4 begin
    
    if request.method == "POST":
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        cursor.execute('SELECT * FROM public."CM_PRESSURE/Output" WHERE time BETWEEN %s AND %s;', (start_time, end_time))
        table4_data = cursor.fetchall()
    
    else:
        # Execute the SQL query to retrieve the data from the database
        cursor.execute('SELECT * FROM public."CM_PRESSURE/Output" LIMIT 5;')
        table4_data = cursor.fetchall()

    # Extract the timestamp and value data from the database result
    timestamps = [row[0] for row in table4_data]
    values = [row[1] for row in table4_data]

    # Create a line chart trace with the timestamp and value data
    line_trace = go.Scatter(x=timestamps, y=values, mode='lines')

    # Create the layout for the chart
    layout = go.Layout(title='Pressure Vs Time', xaxis_title='Time', yaxis_title='Pressure')

    # Create a figure that contains the trace and layout
    fig = go.Figure(data=[line_trace], layout=layout)

    # Convert the figure to HTML and save it as a string
    chart4 = fig.to_html(full_html=False)

    
    # table 4 done
    
    # Pass the data to the dashboard.html template for rendering
    return render_template("dashboard.html", table1_data = table1_data, table2_data = table2_data, table3_data = table3_data, table4_data = table4_data, chart1 = chart1, chart2 = chart2, chart3 = chart3, chart4 = chart4)

#   Download CSVs

@app.route('/download_pressure_csv')
def download_pressure_csv():
    conn = get_db_conn()
    df = pd.read_sql_query('SELECT * FROM "public"."CM_PRESSURE/Output"', conn)

    # Convert the DataFrame to a CSV file
    csv_file = df.to_csv(index=False)

    # Create a response object that contains the CSV file
    response = Response(
        csv_file,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=pressure.csv'}
    )

    return response

@app.route('/download_process_csv')
def download_process_csv():
    conn = get_db_conn()
    df = pd.read_sql_query('SELECT * FROM "public"."CM_PID_DO/Process_DO"', conn)

    # Convert the DataFrame to a CSV file
    csv_file = df.to_csv(index=False)

    # Create a response object that contains the CSV file
    response = Response(
        csv_file,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=process_do.csv'}
    )

    return response

@app.route('/download_ph_csv')
def download_ph_csv():
    conn = get_db_conn()
    df = pd.read_sql_query('SELECT * FROM "public"."CM_HAM_PH_AI1/pH_value"', conn)

    # Convert the DataFrame to a CSV file
    csv_file = df.to_csv(index=False)

    # Create a response object that contains the CSV file
    response = Response(
        csv_file,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=ph.csv'}
    )

    return response

@app.route('/download_temp_csv')
def download_temp_csv():
    conn = get_db_conn()
    df = pd.read_sql_query('SELECT * FROM "public"."CM_HAM_DO_AI1/Temp_value"', conn)

    # Convert the DataFrame to a CSV file
    csv_file = df.to_csv(index=False)

    # Create a response object that contains the CSV file
    response = Response(
        csv_file,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=temp.csv'}
    )

    return response

#   Update without refreshing page

@app.route('/update_data')
def update_data():
    conn = get_db_conn()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM public."CM_HAM_DO_AI1/Temp_value" LIMIT 5;')
    table1_data = cursor.fetchall()
    
    cursor.execute('SELECT * FROM public."CM_HAM_PH_AI1/pH_value" LIMIT 5;')
    table2_data = cursor.fetchall()
    
    cursor.execute('SELECT * FROM public."CM_PID_DO/Process_DO" LIMIT 5;')
    table3_data = cursor.fetchall()
    
    cursor.execute('SELECT * FROM public."CM_PRESSURE/Output" LIMIT 5;')
    table4_data = cursor.fetchall()
    
    return render_template('dashboard.html',
                           table1_data=table1_data,
                           table2_data=table2_data,
                           table3_data=table3_data,
                           table4_data=table4_data)
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)
