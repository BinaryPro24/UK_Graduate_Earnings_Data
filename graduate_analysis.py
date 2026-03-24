import pandas as pd
import matplotlib.pyplot as plt

salary_df = pd.read_csv('salaries_by_sex.csv')
employment_df = pd.read_csv('employment_by_graduate_type.csv')

# Basic Exploration
print("SALARY DATASET:")
print(salary_df.shape)
print(salary_df.head())
print(salary_df['graduate_type'].unique())
print(salary_df['sex'].unique())

# Filter for real median salaries (inflation-adjusted)
# Focus on Total (all genders) first to see the graduate premium
salary_clean = salary_df[
    (salary_df['median_salary_suppression'] == 0) &
    (salary_df['sex'] == 'Total')
][['time_period', 'graduate_type', 'median_real']]

print("\n--- GRADUATE EARNINGS PREMIUM OVER TIME ---")
print(salary_clean.groupby(['time_period', 'graduate_type'])['median_real'].mean().unstack())

# Visualise real earnings over time by graduate type
earnings_over_time = salary_clean.groupby(
    ['time_period', 'graduate_type'])['median_real'].mean().unstack()

plt.figure(figsize=(12, 6))
for col in earnings_over_time.columns:
    plt.plot(earnings_over_time.index, 
             earnings_over_time[col], 
             marker='o', label=col)

plt.title('UK Real Graduate Earnings 2007-2024\n(Inflation-Adjusted)', 
          fontsize=14, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Median Real Earnings (£)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('graduate_earnings_trend.png')
plt.show()

# --- GENDER PAY GAP AMONG GRADUATES ---
gender_salary = salary_df[
    (salary_df['median_salary_suppression'] == 0) &
    (salary_df['graduate_type'] == 'Graduate') &
    (salary_df['sex'] != 'Total')
].groupby(['time_period', 'sex'])['median_real'].mean().unstack()

# Calculate the gap
gender_salary['gap'] = gender_salary['Male'] - gender_salary['Female']
gender_salary['gap_pct'] = (gender_salary['gap'] / 
                             gender_salary['Male'] * 100).round(1)

print("\n--- GRADUATE GENDER PAY GAP OVER TIME ---")
print(gender_salary[['Male', 'Female', 'gap', 'gap_pct']])

# Visualise gender pay gap over time
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('UK Graduate Gender Pay Gap 2007-2024', 
             fontsize=14, fontweight='bold')

# Male vs Female earnings
ax1.plot(gender_salary.index, gender_salary['Male'], 
         marker='o', color='royalblue', label='Male')
ax1.plot(gender_salary.index, gender_salary['Female'], 
         marker='o', color='coral', label='Female')
ax1.set_title('Real Earnings by Gender')
ax1.set_ylabel('Median Real Earnings (£)')
ax1.set_xlabel('Year')
ax1.legend()
ax1.grid(True)

# Gap percentage over time
ax2.plot(gender_salary.index, gender_salary['gap_pct'], 
         marker='o', color='purple', linewidth=2)
ax2.axhline(y=gender_salary['gap_pct'].iloc[0], 
            color='red', linestyle='--', label='2007 baseline (14%)')
ax2.set_title('Gender Pay Gap % Over Time')
ax2.set_ylabel('Gap (%)')
ax2.set_xlabel('Year')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('graduate_gender_pay_gap.png')
plt.show()