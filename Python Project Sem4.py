import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\jeetl\Downloads\carapi-opendatafeed-sample.csv")

# Data Cleaning

print("\n------------------------------------------------------------------------------------")
print("Data Frame Information")
print("------------------------------------------------------------------------------------")
df.info()
print()
print("------------------------------------------------------------------------------------")
print("Data Frame Description")
print("------------------------------------------------------------------------------------")
print(df.describe())
print()
print("------------------------------------------------------------------------------------")
print("Head")
print("------------------------------------------------------------------------------------")
print(df.head())
print()
print("------------------------------------------------------------------------------------")
print("Tail")
print("------------------------------------------------------------------------------------")
print(df.tail())
print()
print("------------------------------------------------------------------------------------")
print("Column Names")
print("------------------------------------------------------------------------------------")
print(df.columns)
print()
print("------------------------------------------------------------------------------------")
print("Shape of the Data Frame")
print("------------------------------------------------------------------------------------")
print(df.shape)
print()
print("------------------------------------------------------------------------------------")
print("Missing Values:")
print("------------------------------------------------------------------------------------")
print(df.isnull().sum())
print()
df.dropna()
print()
print("------------------------------------------------------------------------------------")
print("Outliers:")
print("------------------------------------------------------------------------------------")
Q1 = df['Mileage Fuel Tank Capacity'].quantile(0.25)
Q3 = df['Mileage Fuel Tank Capacity'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['Mileage Fuel Tank Capacity'] < lower_bound) | (df['Mileage Fuel Tank Capacity'] > upper_bound)]
print("Outliers using IQR:")
print(outliers)

plt.figure(figsize=(8, 6))
plt.scatter(df['Make Name'], df['Mileage Fuel Tank Capacity'], color='blue')
plt.title('Outlier Detection Using Scatter Plot')
plt.xticks(rotation=90)
plt.show()

# -----------------------------------------------------------------------------------------------------------------------------------------------

# Objective 1: Identify the most common Car Types and Car Brands.

# (1.1) Top 5 most common Car Type

print("------------------------------------------------------------------------------------")
print("Top 5 Most Common Car Types:")
print("------------------------------------------------------------------------------------")
print(df['Body Type'].value_counts().head())

# Plot for Car Types

plt.figure(figsize=(12, 6))
bars = plt.bar(df['Body Type'].value_counts().head().index, df['Body Type'].value_counts().head().values, color='skyblue')
plt.title('Top 5 Most Common Vehicle Types')
plt.xlabel('Car Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height + 0.5, f"{int(height)}", ha='center', va='bottom')
plt.show()

# (1.2) Top 5 most common Car Brand

print("------------------------------------------------------------------------------------")
print("Top 5 Most Common Car Brand:")
print("------------------------------------------------------------------------------------")
print(df['Make Name'].value_counts().head())

# Plot for makes

plt.figure(figsize=(12, 6))
bars = plt.bar(df['Make Name'].value_counts().head().index, df['Make Name'].value_counts().head().values, color='salmon')
plt.title('Top 5 Most Common Makes')
plt.xlabel('Car Brand')
plt.ylabel('Count')
plt.xticks(rotation=45)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height + 0.5, f"{int(height)}", ha='center', va='bottom')
plt.show()

# -----------------------------------------------------------------------------------------------------------------------------------------------

# Objective 2: Compare fuel efficiency across different vehicle types (e.g., SUVs, Sedans).

print("------------------------------------------------------------------------------------")
print("Comparing fuel efficiency across different Car Types")
print("------------------------------------------------------------------------------------")
comp = df.groupby('Body Type')['Mileage Fuel Tank Capacity'].mean()
print(comp)
print()

# Plot for Comparision

bars = sns.violinplot(x='Body Type', y='Mileage Fuel Tank Capacity', data=df)
plt.title('Fuel Efficiency Across Car Types')
plt.xticks(rotation=90)
for bar in bars.patches:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height + 1.0, f'{height:.2f}', ha='center', va='bottom')
plt.title('Average Fuel Efficiency by Vehicle Type')
plt.ylabel('Fuel Efficiency')
plt.xlabel('Car Type')
plt.show()


# -----------------------------------------------------------------------------------------------------------------------------------------------

# Objective 3: Analyze the count of each company production in different years.

print("------------------------------------------------------------------------------------")
print("Count of Each Car Brand Production per Year")
print("------------------------------------------------------------------------------------")
production_counts = df.groupby(['Make Name', 'Trim Year']).size().reset_index(name='production_count')
print()
pivot_table = production_counts.pivot(index='Make Name', columns='Trim Year', values='production_count')
print(pivot_table)
print()

# Plot for Comparision

plt.figure(figsize=(10, 6))
for company in production_counts['Trim Year'].unique():
    company_data = production_counts[production_counts['Trim Year'] == company]
    plt.plot(company_data['Make Name'], company_data['production_count'], label=company)

plt.title('Production Count by Company Over Years')
plt.xlabel('Car Brand')
plt.ylabel('Production Count')
plt.legend(title='Year')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

# -----------------------------------------------------------------------------------------------------------------------------------------------

# Objective 4: Preferred Engine oil type by customers (Ex. Gas, Hybrid).

print("------------------------------------------------------------------------------------")
print("Preferred Engine Oil Type by Customers")
print("------------------------------------------------------------------------------------")
oil_preference = df.groupby(['Engine Type']).size().reset_index(name='count')
print(oil_preference)
print()

# Plot for Comparision

plt.figure(figsize=(12, 8))
bars = sns.barplot(
    data=oil_preference,
    x='Engine Type',
    y='count',
    hue='Engine Type'
)
plt.title('Preferred Engine Oil Type by Fuel Type')
plt.xlabel('Fuel Type')
plt.ylabel('Customer Count')
for bar in bars.patches:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height + 1.0, f"{int(height)}", ha='center', va='bottom')
plt.show()

# -----------------------------------------------------------------------------------------------------------------------------------------------

# Objective 5: Preferred Driving mode by customers (Ex. All wheel drive).

print("------------------------------------------------------------------------------------")
print("Preferred Driving mode by Customers")
print("------------------------------------------------------------------------------------")
driving_mode_counts = df.groupby('Engine Drive Type').size().reset_index(name='count')
print(driving_mode_counts)
print()

# Plot for Comparision

plt.figure(figsize=(8, 8))
plt.pie(
    driving_mode_counts['count'],
    labels=driving_mode_counts['Engine Drive Type'],
    autopct='%1.1f%%',
    startangle=140
)
plt.title('Preferred Driving Modes')
plt.show()

# -----------------------------------------------------------------------------------------------------------------------------------------------

# Objective 6: Compare among the highest Ground Clearance given by a company.

print("------------------------------------------------------------------------------------")
print("Compare among highest Ground Clearance given by each Car Brand")
print("------------------------------------------------------------------------------------")
max_clearance = df.groupby('Make Name')['Body Ground Clearance'].max().reset_index()
print(max_clearance)
print()

# Plot for comparision

plt.figure(figsize=(8, 6))
plt.scatter(
    max_clearance['Make Name'],
    max_clearance['Body Ground Clearance'],
    color='blue',
    s=100,
    edgecolor='black'
)
plt.title('Highest Ground Clearance by Company', fontsize=14)
plt.xlabel('Company Name')
plt.ylabel('Ground Clearance (cm)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=90)
plt.show()

# -----------------------------------------------------------------------------------------------------------------------------------------------





