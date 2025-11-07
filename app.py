
# This is a Streamlit EDA app scaffold for Starbucks datasets or any uploaded CSV.
# It lets users upload data, preview, clean basic issues, and see quick visuals.

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title='Starbucks EDA', layout='wide')
st.title('Starbucks EDA App')
st.write('Upload the Starbucks datasets (portfolio.json, profile.json, transcript.json) or a CSV to explore.')

with st.sidebar:
    st.header('Data Inputs')
    data_source = st.selectbox('Choose data source', ['Upload CSV', 'Upload JSON trio'])

@st.cache_data
def load_csv(file):
    try:
        df = pd.read_csv(file)
    except Exception:
        df = pd.read_csv(file, encoding='latin1')
    return df

@st.cache_data
def load_json(file):
    return pd.read_json(file, orient='records', lines=False)

if data_source == 'Upload CSV':
    up = st.file_uploader('Upload a CSV file', type=['csv'])
    if up is not None:
        df = load_csv(up)
        st.subheader('Preview')
        st.dataframe(df.head(50))
        st.write('Rows: ' + str(df.shape[0]) + ' | Columns: ' + str(df.shape[1]))

        # Column summary
        st.subheader('Column Summary')
        st.write(df.describe(include='all').transpose())

        # Missingness
        st.subheader('Missing Values')
        miss = df.isna().mean().sort_values(ascending=False) * 100
        st.bar_chart(miss)

        # Numeric correlation heatmap
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if len(num_cols) >= 2:
            st.subheader('Correlation Heatmap (numeric)')
            corr = df[num_cols].corr()
            fig, ax = plt.subplots(figsize=(6,4))
            sns.heatmap(corr, cmap='viridis', annot=False)
            plt.tight_layout()
            st.pyplot(fig)

        # Target exploration if user selects a column
        st.subheader('Quick Visuals')
        col = st.selectbox('Select a column to visualize', df.columns)
        if col:
            if col in num_cols:
                fig, ax = plt.subplots(figsize=(6,4))
                sns.histplot(df[col].dropna(), kde=True)
                plt.tight_layout()
                st.pyplot(fig)
            else:
                vc = df[col].value_counts().head(20)
                st.bar_chart(vc)

else:
    portfolio = st.file_uploader('portfolio.json', type=['json'], key='port')
    profile = st.file_uploader('profile.json', type=['json'], key='prof')
    transcript = st.file_uploader('transcript.json', type=['json'], key='trans')

    if portfolio and profile and transcript:
        port_df = load_json(portfolio)
        prof_df = load_json(profile)
        trans_df = load_json(transcript)

        st.subheader('Data Heads')
        st.write('portfolio')
        st.dataframe(port_df.head(20))
        st.write('profile')
        st.dataframe(prof_df.head(20))
        st.write('transcript')
        st.dataframe(trans_df.head(20))

        # Basic Starbucks-specific EDA
        st.subheader('Offer Types and Difficulty (portfolio)')
        if 'offer_type' in port_df.columns and 'difficulty' in port_df.columns:
            fig, ax = plt.subplots(figsize=(6,4))
            sns.boxplot(data=port_df, x='offer_type', y='difficulty')
            plt.tight_layout()
            st.pyplot(fig)

        st.subheader('Demographics (profile)')
        demo_cols = [c for c in ['age','income','gender'] if c in prof_df.columns]
        if 'age' in demo_cols:
            fig, ax = plt.subplots(figsize=(6,4))
            sns.histplot(prof_df['age'].replace(118, np.nan).dropna(), kde=True)
            plt.tight_layout()
            st.pyplot(fig)
        if 'gender' in demo_cols:
            st.bar_chart(prof_df['gender'].value_counts())

        st.subheader('Event Types (transcript)')
        if 'event' in trans_df.columns:
            st.bar_chart(trans_df['event'].value_counts())

        # Join logic: basic example to compute offer completion rate by type
        try:
            if 'offer id' in trans_df.columns:
                trans_df = trans_df.rename(columns={'offer id':'offer_id'})
            if 'id' in port_df.columns:
                port_df = port_df.rename(columns={'id':'offer_id'})
            comp = trans_df[trans_df['event'].isin(['offer completed','offer received'])]
            pivot = comp.pivot_table(index='offer_id', columns='event', values='person', aggfunc='nunique', fill_value=0)
            pivot = pivot.reset_index().merge(port_df[['offer_id','offer_type']], on='offer_id', how='left')
            pivot['completion_rate'] = np.where(pivot['offer received']>0, pivot['offer completed']/pivot['offer received'], np.nan)
            st.subheader('Offer completion rate by offer type')
            grp = pivot.groupby('offer_type')['completion_rate'].mean().sort_values()
            st.bar_chart(grp)
        except Exception as e:
            st.info('Join analysis skipped: ' + str(e))


# ---- Enhancements: built-in datasets and Starbucks dashboards ----
import io

def load_builtin_csv(name):
    path = name
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.read_csv(path, encoding='latin1')
    return None

st.sidebar.markdown('---')
st.sidebar.subheader('Built-in Starbucks datasets')
use_builtin = st.sidebar.checkbox('Use built-in CSVs if available', value=True)

builtin_choice = None
if use_builtin:
    options = []
    if os.path.exists('cleaned_starbucks.csv'):
        options.append('cleaned_starbucks.csv')
    if os.path.exists('starbucks.csv'):
        options.append('starbucks.csv')
    if len(options) > 0:
        builtin_choice = st.sidebar.selectbox('Choose a built-in dataset', options)

if builtin_choice is not None:
    df_built = load_builtin_csv(builtin_choice)
    if df_built is not None:
        st.header('Built-in dataset: ' + builtin_choice)
        st.dataframe(df_built.head(50))
        st.write('Rows: ' + str(df_built.shape[0]) + ' | Columns: ' + str(df_built.shape[1]))

        # Try common Starbucks columns for visuals if present
        num_cols_b = df_built.select_dtypes(include=np.number).columns.tolist()
        cat_cols_b = [c for c in df_built.columns if c not in num_cols_b]

        st.subheader('Quick numeric correlation (built-in)')
        if len(num_cols_b) >= 2:
            corr = df_built[num_cols_b].corr()
            fig, ax = plt.subplots(figsize=(6,4))
            sns.heatmap(corr, cmap='mako', annot=False)
            plt.tight_layout()
            st.pyplot(fig)

        # Starbucks-specific guesses
        st.subheader('Offer funnel and events (if columns available)')
        event_col = None
        for cand in ['event','Event','EVENT']:
            if cand in df_built.columns:
                event_col = cand
                break
        person_col = None
        for cand in ['person','customer_id','user','Person']:
            if cand in df_built.columns:
                person_col = cand
                break
        offer_id_col = None
        for cand in ['offer_id','offer id','id','offer']:
            if cand in df_built.columns:
                offer_id_col = cand
                break
        offer_type_col = None
        for cand in ['offer_type','offer type','type']:
            if cand in df_built.columns:
                offer_type_col = cand
                break
        time_col = None
        for cand in ['time','timestamp','date','datetime']:
            if cand in df_built.columns:
                time_col = cand
                break

        if event_col is not None:
            st.write('Event distribution:')
            st.bar_chart(df_built[event_col].value_counts())

        # Funnel by offer_type
        try:
            df_tmp = df_built.copy()
            if offer_id_col is not None and event_col is not None and person_col is not None:
                comp = df_tmp[df_tmp[event_col].isin(['offer received','offer viewed','offer completed'])]
                pivot = comp.pivot_table(index=offer_id_col, columns=event_col, values=person_col, aggfunc='nunique', fill_value=0).reset_index()
                if offer_type_col is not None:
                    pivot = pivot.merge(df_tmp[[offer_id_col, offer_type_col]].drop_duplicates(), on=offer_id_col, how='left')
                for coln in ['offer received','offer viewed','offer completed']:
                    if coln not in pivot.columns:
                        pivot[coln] = 0
                pivot['view_rate'] = np.where(pivot['offer received']>0, pivot['offer viewed']/pivot['offer received'], np.nan)
                pivot['completion_rate'] = np.where(pivot['offer received']>0, pivot['offer completed']/pivot['offer received'], np.nan)
                if offer_type_col is not None:
                    grp = pivot.groupby(offer_type_col)[['view_rate','completion_rate']].mean().sort_values('completion_rate')
                    st.write('Average funnel rates by offer type:')
                    st.dataframe(grp)
                    fig, ax = plt.subplots(figsize=(6,4))
                    grp['completion_rate'].plot(kind='bar', color='seagreen')
                    plt.ylabel('completion_rate')
                    plt.tight_layout()
                    st.pyplot(fig)
        except Exception as e:
            st.info('Funnel analysis skipped: ' + str(e))

        # Temporal trend of events
        try:
            if time_col is not None and event_col is not None:
                ts = df_built[[time_col, event_col]].copy()
                ts[time_col] = pd.to_datetime(ts[time_col], errors='coerce')
                ts = ts.dropna(subset=[time_col])
                ts['period'] = ts[time_col].dt.to_period('W').astype(str)
                trend = ts.groupby(['period', event_col]).size().reset_index(name='count')
                recent = trend[trend['period'] >= sorted(trend['period'])[:1][0]]
                pivot_t = recent.pivot(index='period', columns=event_col, values='count').fillna(0)
                st.subheader('Weekly event counts')
                st.line_chart(pivot_t)
        except Exception as e:
            st.info('Temporal chart skipped: ' + str(e))

        # Demographics
        try:
            demo_cols = [c for c in ['age','income','gender'] if c in df_built.columns]
            if 'age' in demo_cols:
                fig, ax = plt.subplots(figsize=(6,4))
                sns.histplot(df_built['age'].replace(118, np.nan).dropna(), kde=True)
                plt.tight_layout()
                st.pyplot(fig)
            if 'gender' in demo_cols:
                st.bar_chart(df_built['gender'].value_counts())
            if 'income' in demo_cols:
                fig, ax = plt.subplots(figsize=(6,4))
                sns.boxplot(x=df_built['gender'] if 'gender' in df_built.columns else None, y=df_built['income'])
                plt.tight_layout()
                st.pyplot(fig)
        except Exception as e:
            st.info('Demographics visuals skipped: ' + str(e))
