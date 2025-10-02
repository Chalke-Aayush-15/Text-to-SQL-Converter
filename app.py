# ==========================================
# STREAMLIT WEB INTERFACE
# ==========================================

"""
Streamlit web interface for Text-to-SQL Converter.
Run with: streamlit run app.py
"""

import streamlit as st
import json
from datetime import datetime
import sys
import os

# Import main converter (assumes text_to_sql.py is in same directory)
from text_to_sql import TextToSQLConverter, DatabaseSchema

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Converter",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sql-output {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        font-family: 'Courier New', monospace;
        font-size: 1rem;
    }
    .example-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e8eaf6;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .example-box:hover {
        background-color: #c5cae9;
        transform: translateY(-2px);
    }
    .schema-table {
        background-color: #fff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_converter():
    """Load the Text-to-SQL converter (cached)."""
    schema = DatabaseSchema()
    converter = TextToSQLConverter(schema=schema)
    return converter, schema


def display_schema(schema: DatabaseSchema):
    """Display database schema in sidebar."""
    st.sidebar.header("📊 Database Schema")
    
    for table_name, table_info in schema.schema['tables'].items():
        with st.sidebar.expander(f"🗂️ {table_name}", expanded=False):
            for col in table_info['columns']:
                col_display = f"• **{col['name']}** ({col['type']})"
                if col.get('primary_key'):
                    col_display += " 🔑"
                if col.get('foreign_key'):
                    col_display += f" → {col['foreign_key']}"
                st.markdown(col_display)


def main():
    """Main Streamlit application."""
    
    # Initialize session state for user input
    if 'user_question' not in st.session_state:
        st.session_state.user_question = ""
    
    # Header
    st.markdown('<p class="main-header">🗄️ Text-to-SQL Converter</p>', unsafe_allow_html=True)
    st.markdown("**Transform natural language questions into SQL queries instantly**")
    st.markdown("---")
    
    # Load converter
    try:
        converter, schema = load_converter()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.info("The app will use rule-based conversion instead.")
        schema = DatabaseSchema()
        converter = TextToSQLConverter(schema=schema)
    
    # Display schema in sidebar
    display_schema(schema)
    
    # Add model info to sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Settings")
    model_name = st.sidebar.text_input(
        "Model Name",
        value="cssupport/t5-small-awesome-text-to-sql",
        help="HuggingFace model identifier"
    )
    max_length = st.sidebar.slider("Max SQL Length", 50, 512, 256)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💬 Natural Language Input")
        
        # Text input - using session state value
        user_question = st.text_area(
            "Enter your question:",
            value=st.session_state.user_question,
            height=150,
            placeholder="e.g., Show me all customers who ordered in January",
            key="question_input"
        )
        
        # Convert button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            convert_btn = st.button("🚀 Convert to SQL", type="primary", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_btn:
            st.session_state.user_question = ""
            st.rerun()
    
    with col2:
        st.subheader("📝 Generated SQL Query")
        
        # Placeholder for SQL output
        sql_placeholder = st.empty()
        
        if convert_btn and user_question:
            with st.spinner("Converting to SQL..."):
                try:
                    sql_query = converter.convert(user_question, max_length=max_length)
                    
                    # Display SQL
                    sql_placeholder.markdown(
                        f'<div class="sql-output">{sql_query}</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Add copy button
                    st.code(sql_query, language="sql")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download SQL",
                        data=sql_query,
                        file_name=f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql",
                        mime="text/plain"
                    )
                    
                    st.success("✅ SQL query generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        elif convert_btn:
            st.warning("⚠️ Please enter a question first!")
    
    # Example queries section
    st.markdown("---")
    st.subheader("📚 Example Queries")
    st.markdown("Click on any example to try it out:")
    
    examples = [
        ("Show me all customers who ordered in January", "Customer orders in specific month"),
        ("What are the top 5 products by price?", "Top products by price"),
        ("Find customers from New York with orders over $1000", "Filtered customer search"),
        ("List all pending orders with customer names", "Orders with customer details"),
        ("Show total sales by product category", "Aggregate sales analysis"),
        ("How many orders were placed in 2024?", "Count queries"),
        ("Get customer emails for orders above $500", "Specific column retrieval"),
        ("Which products are out of stock?", "Stock status check")
    ]
    
    cols = st.columns(2)
    for idx, (example_q, description) in enumerate(examples):
        with cols[idx % 2]:
            if st.button(f"💡 {description}", key=f"example_{idx}", use_container_width=True):
                st.session_state.user_question = example_q
                st.rerun()
            st.caption(example_q)
    
    # Batch processing section
    st.markdown("---")
    st.subheader("🔄 Batch Processing")
    
    with st.expander("Process Multiple Questions"):
        batch_input = st.text_area(
            "Enter questions (one per line):",
            height=150,
            placeholder="Show all customers\nList top 10 products\nGet pending orders"
        )
        
        if st.button("🔄 Process Batch"):
            if batch_input:
                questions = [q.strip() for q in batch_input.split('\n') if q.strip()]
                
                with st.spinner(f"Processing {len(questions)} questions..."):
                    results = converter.batch_convert(questions)
                    
                    # Display results
                    for i, (q, sql) in enumerate(results, 1):
                        st.markdown(f"**{i}. {q}**")
                        st.code(sql, language="sql")
                    
                    # Download all results
                    batch_output = "\n\n".join([
                        f"-- Question {i}: {q}\n{sql};"
                        for i, (q, sql) in enumerate(results, 1)
                    ])
                    
                    st.download_button(
                        label="📥 Download All Queries",
                        data=batch_output,
                        file_name=f"batch_queries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql",
                        mime="text/plain"
                    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>Text-to-SQL Converter v1.0</strong></p>
        <p>Powered by Transformer Models | Built with Streamlit</p>
        <p style='font-size: 0.8rem;'>⚠️ Note: Generated SQL queries are not executed. Always review before running on production databases.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()