import pandas as pd
import streamlit as st
from user_agents import parse



def get_browser(raw_user_agent: str) -> str:
    """
    Gets the browser name from a user agent string
    :param raw_user_agent: The input user agent
    :return: The browser name
    """
    user_agent = parse(raw_user_agent)
    return user_agent.browser.family


def get_os(raw_user_agent: str) -> str:
    """
    Returns the operating system from a user agent string
    :param raw_user_agent: The input user agent string
    :return: The operating system
    """
    user_agent = parse(raw_user_agent)
    return user_agent.os.family


# Get the data.
data = pd.read_csv('demo_data.csv')
data['browser'] = data['user_agent'].apply(get_browser)
data['os'] = data['user_agent'].apply(get_os)

st.metric(value=len(data['browser'].unique()), label="Unique Browsers", delta=2)

tech_tab, location_tab = st.tabs(["Technical Details", "Location Information"])
col1, col2 = tech_tab.columns(2)
with tech_tab:
    with col1:
        st.header('Browsers')
        st.bar_chart(data['browser'].value_counts().sort_values(ascending=False).head(5))
    with col2:
        st.header('Operating Systems')
        st.bar_chart(data['os'].value_counts().sort_values(ascending=False).head(5))

with location_tab:
    st.title("Location Details")
    st.write("Shows where in the world our users are located.")
    st.bar_chart(data['country'].value_counts().sort_values())

st.dataframe(data=data, use_container_width=True, hide_index=True)
