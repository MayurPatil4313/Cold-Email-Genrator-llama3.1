import streamlit as st

email = """
Dear Hiring Management,

I came across your job posting for a Lead Data Scientist and was impressed by the scope of responsibilities and the skills required for the role. As a Business Development Executive at TCS, I believe our organization can significantly contribute to your data analytics and science initiatives.

Our team of experts has extensive experience in designing, developing, and programming methods to consolidate and analyze structured and unstructured data sources, generating actionable insights and solutions for client services and product enhancement. We have successfully implemented similar projects, leveraging our expertise in Python, Machine Learning, Statistics, Business Intelligence, Data Analytics, SQL programming, Data Visualization, and Time Series Forecasting.

I'd like to highlight a few relevant portfolio items that demonstrate our capabilities in machine learning and data analytics:

* Our work on a machine learning-based project for a leading e-commerce company, where we developed predictive models using Python and Magento, resulting in a 25% increase in sales (https://example.com/machinelearning-magento-php-portfolio).
* A data analytics project for a financial institution, where we built a data visualization platform using Java, JavaScript, and Machine Learning, enabling the client to make data-driven decisions (https://example.com/java-javascript-machinelearning-portfolio).
* A project for a healthcare company, where we developed a predictive analytics solution using Machine Learning, PostgreSQL, and SQL Server, resulting in a 30% reduction in operational costs (https://example.com/machinelearning-postgresql-sqlserver-portfolio).

Our team is well-equipped to lead complex data science projects, interact with cross-functional teams, and communicate insights and findings to stakeholders. We believe our expertise can help your organization drive business growth, improve operational efficiency, and enhance customer experiences.

I'd be delighted to discuss how TCS can support your data science initiatives and explore potential collaboration opportunities. Please feel free to contact me at your convenience.

Best regards,
Sagar Patil
Business Development Executive, TCS
"""
# Set full-width layout for proper use of screen
st.set_page_config(layout="wide")


# # Inject CSS & JS for dynamic theme support and full-width formatting
# copy_button_and_code = f"""
# <style>
#     .custom-code-wrapper {{
#         max-width: 100%;
#         width: 100%;
#     }}

#     .custom-code {{
#         background-color: var(--background-secondary);
#         color: var(--text-color);
#         padding: 1em;
#         border-radius: 6px;
#         font-family: monospace;
#         white-space: pre-wrap;
#         word-break: break-word;
#         border: 1px solid var(--primary-color);
#         box-sizing: border-box;
#     }}

#     .copy-btn {{
#         background-color: var(--primary-color);
#         color: var(--text-color);
#         border: none;
#         border-radius: 5px;
#         padding: 6px 12px;
#         font-size: 14px;
#         cursor: pointer;
#         margin-bottom: 10px;
#     }}
# </style>

# <div class="custom-code-wrapper">
#     <button class="copy-btn" id="copyBtn">📋 Copy to Clipboard</button>
#     <div class="custom-code" id="emailText">{email}</div>
# </div>

# <script>
# function copyToClipboard(text) {{
#     navigator.clipboard.writeText(text).then(function() {{
#         const streamlitEvent = new Event("copied");
#         document.dispatchEvent(streamlitEvent);
#     }});
# }}

# document.addEventListener("DOMContentLoaded", function() {{
#     document.getElementById("copyBtn").addEventListener("click", function() {{
#         const text = document.getElementById("emailText").innerText;
#         copyToClipboard(text);
#     }});
# }});
# </script>
# """

# # JS event handler to show Streamlit toast on copy
# toast_script = """
# <script>
# document.addEventListener("copied", function() {
#     const streamlitFrame = window.parent.document.querySelector('iframe[title="streamlit_app"]');
#     const event = new CustomEvent("streamlit:toast", {
#         detail: { type: "success", message: "Copied!" }
#     });
#     streamlitFrame.contentWindow.postMessage(event.detail, "*");
# });
# </script>
# """

# # Display everything
# st.markdown(copy_button_and_code, unsafe_allow_html=True)
# st.components.v1.html(toast_script, height=0)




# HTML block with fixed JS logic
copy_button_and_code = f"""
<style>
    .custom-code-wrapper {{
        max-width: 800px;
        width: 100%;
        margin: auto;
    }}

    .custom-code {{
        background-color: var(--background-secondary);
        color: var(--text-color);
        padding: 1em;
        border-radius: 6px;
        font-family: monospace;
        white-space: pre-wrap;
        word-break: break-word;
        border: 1px solid var(--primary-color);
        box-sizing: border-box;
        line-height: 1.6;
    }}

    .copy-btn {{
        background-color: var(--primary-color);
        color: var(--text-color);
        border: none;
        border-radius: 5px;
        padding: 6px 12px;
        font-size: 14px;
        cursor: pointer;
        margin-bottom: 10px;
    }}
</style>

<div class="custom-code-wrapper">
    <button class="copy-btn" onclick="copyToClipboard()">📋 Copy to Clipboard</button>
    <div class="custom-code" id="emailText">{email}</div>
</div>

<script>
function copyToClipboard() {{
    const text = document.getElementById("emailText").innerText;
    navigator.clipboard.writeText(text).then(function() {{
        const streamlitFrame = window.parent.document.querySelector('iframe[title="streamlit_app"]');
        const event = new CustomEvent("streamlit:toast", {{
            detail: {{ type: "success", message: "Copied!" }}
        }});
        streamlitFrame.contentWindow.postMessage(event.detail, "*");
    }});
}}
</script>
"""

# Render everything
st.markdown(copy_button_and_code, unsafe_allow_html=True)