
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

# Page Configuration
st.set_page_config(
    page_title="Employee Feedback & Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .kpi-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center; }
    .kpi-title { font-size: 14px; color: #6c757d; font-weight: 600; }
    .kpi-value { font-size: 24px; color: #343a40; font-weight: bold; margin-top: 5px; }
    </style>
""",
    unsafe_allow_html=True,
)


# Load Dataset
@st.cache_data
def load_data():
  file_path = "Employee_feedback_modified.xlsx"
  df_sheet2 = pd.read_excel(file_path, sheet_name="Employee_feedback_dataset")
  return df_sheet2


df = load_data()

# Sidebar Navigation
st.sidebar.title("🚀 Project Dashboard")
st.sidebar.markdown(
    "*Use of Data in Employee Feedback & Performance Reviews*"
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "💬 Feedback Analysis",
        "🎯 Performance Analysis",
        "👥 Employee Insights",
        "📈 Relationships",
        "💡 Key Findings"
        
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")
dept_filter = st.sidebar.selectbox(
    "Department", ["All"] + list(df["Dept"].unique())
)
age_filter = st.sidebar.selectbox("Age Group", ["All"] + list(df["Age"].unique()))

# Apply Filters
filtered_df = df.copy()
if dept_filter != "All":
  filtered_df = filtered_df[filtered_df["Dept"] == dept_filter]
if age_filter != "All":
  filtered_df = filtered_df[filtered_df["Age"] == age_filter]

# Top KPI Cards
st.markdown("## 📊 Employee Feedback & Performance Dashboard")
col1, col2, col3, col4 = st.columns(4)

total_emp = 100  # As requested
avg_perf = (
    round(filtered_df["Performance"].mean(), 2)
    if not filtered_df.empty
    else 0
)
avg_fb_quality = (
    round(filtered_df["Feedback_quality"].mean(), 2)
    if not filtered_df.empty
    else 0
)
avg_sat = (
    round(filtered_df["Satisfaction"].mean(), 2)
    if not filtered_df.empty
    else 0
)

with col1:
  st.markdown(
      f'<div class="kpi-card"><div class="kpi-title">👥 Total Employees</div><div class="kpi-value">{total_emp}</div></div>',
      unsafe_allow_html=True,
  )
with col2:
  st.markdown(
      f'<div class="kpi-card"><div class="kpi-title">⭐Avg Performance</div><div class="kpi-value">{avg_perf} /5</div></div>',
      unsafe_allow_html=True,
  )
with col3:
  st.markdown(
      f'<div class="kpi-card"><div class="kpi-title">📋 Avg Feedback Quality</div><div class="kpi-value">{avg_fb_quality} / 5</div></div>',
      unsafe_allow_html=True,
  )
with col4:
  st.markdown(
      f'<div class="kpi-card"><div class="kpi-title">😊 Avg Job Satisfaction</div><div class="kpi-value">{avg_sat} /5</div></div>',
      unsafe_allow_html=True,
  )

st.markdown("---")

# 🏠 OVERVIEW SECTION
if menu == "🏠 Overview":
  st.subheader("🏠 Dashboard Overview & Original Dataset")
  st.write(
      "This overview section displays key performance indicators, department distributions,and job satisfaction metrics from the dataset"
        "It also provides a complete view of the original employee feedback records."
  )

  c1, c2 = st.columns(2)
  with c1:
    fig_dept = px.bar(
        filtered_df["Dept"].value_counts().reset_index(),
        x="Dept",
        y="count",
        title="Employee Count by Department",
        color="Dept",
    )
    st.plotly_chart(fig_dept, use_container_width=True)
  with c2:
    fig_sat = px.histogram(
        filtered_df,
        x="Satisfaction",
        title="Job Satisfaction Distribution",
        color_discrete_sequence=["#636EFA"],
    )
    st.plotly_chart(fig_sat, use_container_width=True)

  st.markdown("### 📂 Original Dataset (Employee_feedback_dataset)")
  st.dataframe(filtered_df)

# 💬 FEEDBACK ANALYSIS SECTION
elif menu == "💬 Feedback Analysis":
  st.subheader("💬 Feedback Analysis")

  r1c1, r1c2 = st.columns(2)
  with r1c1:
    df_fb_q = (
        filtered_df.groupby("Feedback_quality")["Performance"]
        .mean()
        .reset_index()
    )
    fig1 = px.bar(
        df_fb_q,
        x="Feedback_quality",
        y="Performance",
        title="Feedback Quality vs Performance",
        color="Performance",
    )
    st.plotly_chart(fig1, use_container_width=True)

  with r1c2:
    df_fb_h = (
        filtered_df.groupby("Feedback_Help")["Performance"].mean().reset_index()
    )
    fig2 = px.bar(
        df_fb_h,
        x="Feedback_Help",
        y="Performance",
        title="Feedback Impact vs Performance",
        color="Performance",
    )
    st.plotly_chart(fig2, use_container_width=True)

  r2c1, r2c2 = st.columns(2)
  with r2c1:
    df_fb_f = (
        filtered_df.groupby("Feedback_Freq")["Performance"].mean().reset_index()
    )
    fig3 = px.bar(
        df_fb_f,
        x="Feedback_Freq",
        y="Performance",
        title="Feedback Frequency vs Performance",
        color="Performance",
    )
    st.plotly_chart(fig3, use_container_width=True)

  with r2c2:
    fig4 = px.pie(
        filtered_df,
        names="Feedback_mode",
        title="Feedback Method Distribution",
        hole=0.4,
    )
    st.plotly_chart(fig4, use_container_width=True)

  
# 🎯 PERFORMANCE ANALYSIS SECTION
elif menu == "🎯 Performance Analysis":
  st.subheader("🎯 Performance Analysis")

  c1, c2,c3 = st.columns(3)
  with c1:
    df_dept_p = (
        filtered_df.groupby("Dept")["Performance"].mean().reset_index()
    )
    fig1 = px.bar(
        df_dept_p, x="Dept", y="Performance", title="Department vs Performance"
    )
    st.plotly_chart(fig1, use_container_width=True)

  with c2:
    df_sat_p = (
        filtered_df.groupby("Satisfaction")["Performance"]
        .mean()
        .reset_index()
    )
    fig2 = px.bar(
        df_sat_p,
        x="Satisfaction",
        y="Performance",
        title="Job Satisfaction vs Performance",
    )
    st.plotly_chart(fig2, use_container_width=True)


  with c3:
    df_promo = (
        filtered_df.groupby("Promotion")["Performance"].mean().reset_index()
    )
    fig3 = px.bar(
        df_promo,
        x="Promotion",
        y="Performance",
        title="Performance vs Promotion",
    )
    st.plotly_chart(fig3, use_container_width=True)

  
# 👥 EMPLOYEE INSIGHTS SECTION
elif menu == "👥 Employee Insights":
  st.subheader("👥 Employee Insights")

  c1, c2 = st.columns(2)
  with c1:
    fig1 = px.histogram(
        filtered_df,
        x="Training_need",
        title="Training Need Distribution",
        color="Training_need",
    )
    st.plotly_chart(fig1, use_container_width=True)



  c2, c3= st.columns(2)
  with c2:
    df_dept_perf = (
        filtered_df.groupby("Dept")["Performance"].mean().reset_index()
    )
    fig3 = px.bar(
        df_dept_perf,
        x="Dept",
        y="Performance",
        title="Department-wise Performance",
    )
    st.plotly_chart(fig3, use_container_width=True)

  with c3:
    fig4 = px.pie(
        filtered_df, names="Promotion", title="Promotion Distribution"
    )
    st.plotly_chart(fig4, use_container_width=True)

# 📈 RELATIONSHIPS SECTION
elif menu == "📈 Relationships":
  st.subheader("📈 Key Relationships & Correlations")

  fig1 = px.scatter(
      filtered_df,
      x="Satisfaction",
      y="Performance",
      title="Job Satisfaction ↔ Performance",
      trendline="ols",
  )
  st.plotly_chart(fig1, use_container_width=True)

  fig2 = px.scatter(
      filtered_df,
      x="Absent_days",
      y="Performance",
      title="Absenteeism ↔ Performance",
      trendline="ols",
  )
  st.plotly_chart(fig2, use_container_width=True)



# Key Findings 
elif menu == "💡 Key Findings":
  st.subheader("💡 Overall Key Findings & Insights")
  st.write(
      "This section highlights the critical conclusions and trends derived"
      " from the employee feedback and performance dataset."
  )

  st.markdown(
      """
    ### 📊 Key Insights:
     1. **Feedback Impact:** Higher feedback quality and helpfulness directly correlate with better overall employee performance scores.\n
     2. **Satisfaction & Performance:** Employees with higher job satisfaction ratings tend to demonstrate superior performance metrics.\n
     3. **Attendance Effect:** Lower absenteeism (fewer absent days) shows a positive alignment with higher productivity and performance scores.\n
     4. **Salary Growth:** Employees receiving higher salary increments generally maintain stable or higher performance tiers.\n
     5.  Job satisfaction and performance show a strong positive relationship.\n
     6.  Technical, Sales, and Healthcare departments lead in average performance.\n
     7.  Face-to-face meeting is the most predominant feedback channel.
     
            """
  )
