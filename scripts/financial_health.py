import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from scipy import stats
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    df = df[df.index >= '2002-01-06']
    return df

def calculate_metrics(df):
    df['Savings Rate'] = df['Savings($)'] / df['Income($)'] * 100
    df['Debt-to-Income Ratio'] = df['Credit Card Debt($)'] / df['Income($)']
    df['Net Worth'] = df['Savings($)'] + df['Stocks($)'] + df['Bonds($)'] + df['Real Estate($)'] - df['Credit Card Debt($)']
    return df

def generate_projections(df, periods=26):
    last_quarter = df.last('26W')
    projections = pd.DataFrame(index=pd.date_range(start=df.index[-1] + timedelta(days=1), periods=periods, freq='W'))
    
    for column in df.columns:
        if column in ['Savings($)', 'Net Worth']:
            projections[column] = last_quarter[column].mean()
        else:
            x = np.arange(len(last_quarter))
            y = last_quarter[column].values
            slope, intercept, _, _, _ = stats.linregress(x, y)
            future_x = np.arange(len(last_quarter), len(last_quarter) + periods)
            projections[column] = slope * future_x + intercept
    
    return projections

def create_visualizations(df, projections):
    figs = []
    
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Net Worth'], label='Historical')
    plt.plot(projections.index, projections['Net Worth'], label='Projected', linestyle='--')
    plt.title('Net Worth Trend and Projection')
    plt.xlabel('Date')
    plt.ylabel('Net Worth ($)')
    plt.legend()
    figs.append(plt.gcf())
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Savings Rate'], label='Savings Rate')
    plt.plot(projections.index, projections['Savings Rate'], linestyle='--', label='Projected Savings Rate')
    plt.plot(df.index, df['Debt-to-Income Ratio'], label='Debt-to-Income Ratio')
    plt.plot(projections.index, projections['Debt-to-Income Ratio'], linestyle='--', label='Projected Debt-to-Income Ratio')
    plt.title('Savings Rate and Debt-to-Income Ratio Over Time')
    plt.xlabel('Date')
    plt.ylabel('Ratio')
    plt.legend()
    figs.append(plt.gcf())
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Income($)'], label='Income')
    plt.plot(projections.index, projections['Income($)'], linestyle='--', label='Projected Income')
    plt.plot(df.index, df['Expense($)'], label='Expense')
    plt.plot(projections.index, projections['Expense($)'], linestyle='--', label='Projected Expense')
    plt.title('Income and Expenses Trend')
    plt.xlabel('Date')
    plt.ylabel('Amount ($)')
    plt.legend()
    figs.append(plt.gcf())
    plt.close()

    return figs

def generate_recommendation(df, projections):
    current_savings_rate = df['Savings Rate'].iloc[-1]
    projected_savings_rate = projections['Savings Rate'].iloc[-1]
    current_debt_to_income = df['Debt-to-Income Ratio'].iloc[-1]
    projected_debt_to_income = projections['Debt-to-Income Ratio'].iloc[-1]
    
    if projected_savings_rate < current_savings_rate:
        recommendation = "The projected savings rate is lower than the current rate. Consider reducing non-essential expenses, particularly in the Travel and Home Renovation categories, to improve your savings rate in the coming quarters."
    elif projected_debt_to_income > current_debt_to_income:
        recommendation = "Your projected debt-to-income ratio is increasing. Focus on paying down high-interest debt and avoid taking on new debt to improve your financial health."
    else:
        recommendation = "Your projected financial metrics look positive. To further improve your financial health, consider allocating any excess savings to diversifying your investment portfolio or building an emergency fund."
    return recommendation

def create_pdf_report(df, projections, figs, recommendation):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Financial Health Report", styles['Title']))
    story.append(Spacer(1, 12))

    latest_data = df.iloc[-1]
    current_metrics = [
        ["Metric", "Value"],
        ["Current Savings Rate", f"{latest_data['Savings Rate']:.2f}%"],
        ["Current Debt-to-Income Ratio", f"{latest_data['Debt-to-Income Ratio']:.2f}"],
        ["Current Net Worth", f"${latest_data['Net Worth']:,.2f}"]
    ]
    story.append(Paragraph("Current Financial Metrics", styles['Heading2']))
    story.append(Table(current_metrics, style=[('GRID', (0,0), (-1,-1), 1, colors.black)]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Two-Quarter Projections", styles['Heading2']))
    projected_metrics = [
        ["Metric", "Projected Value"],
        ["Projected Savings Rate", f"{projections['Savings Rate'].iloc[-1]:.2f}%"],
        ["Projected Debt-to-Income Ratio", f"{projections['Debt-to-Income Ratio'].iloc[-1]:.2f}"],
        ["Projected Net Worth", f"${projections['Net Worth'].iloc[-1]:,.2f}"]
    ]
    story.append(Table(projected_metrics, style=[('GRID', (0,0), (-1,-1), 1, colors.black)]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Financial Trends and Projections", styles['Heading2']))
    for fig in figs:
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img = Image(img_buffer)
        img.drawHeight = 300
        img.drawWidth = 500
        story.append(img)
        story.append(Spacer(1, 12))

    story.append(Paragraph("Recommendation", styles['Heading2']))
    story.append(Paragraph(recommendation, styles['BodyText']))

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_financial_report(file_path):
    df = load_data(file_path)
    df = calculate_metrics(df)
    projections = generate_projections(df)
    figs = create_visualizations(df, projections)
    recommendation = generate_recommendation(df, projections)
    
    pdf_buffer = create_pdf_report(df, projections, figs, recommendation)
    
    with open('financial_health_report.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())
    
    print("Financial health report has been generated and saved as 'financial_health_report.pdf'")

generate_financial_report("expanded_financial_data.csv")