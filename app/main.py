import streamlit as st
import duckdb
import requests

st.set_page_config(page_title="2026 local knowledge engine", page_icon="📚")
st.title("📚 2026 Local Knowledge Engine")

# Helper to get DB path
def get_db_path():
    return 'data/processed/knowledge_base.duckdb'

db_path = get_db_path()

# --- DEBUG SECTION ---
if st.checkbox("🛠️ Show Database Content (Debug)"):
    try:
        conn = duckdb.connect(db_path)
        # Show the first 5 rows so you can see what words are actually in there
        db_content = conn.execute("SELECT document_id, content FROM vector_store LIMIT 5").df()
        st.write("Current data in DuckDB:")
        st.dataframe(db_content)
        conn.close()
    except Exception as e:
        st.error(f"Could not read DB: {e}")

# --- SEARCH SECTION ---
query = st.text_input("Search your documents:", placeholder="Type a word from your PDF...")

if query:
    with st.spinner("🔍 Searching..."):
        try:
            conn = duckdb.connect(db_path)
            # IMPROVED SQL: Case-insensitive partial match
            # ILIKE '%word%' finds the word anywhere in the text
            search_query = f"SELECT content, document_id FROM vector_store WHERE content ILIKE '%{query}%' LIMIT 3"
            results = conn.execute(search_query).df()
            conn.close()
            
            if results.empty:
                st.warning(f"No matches for '{query}'. Check 'Debug' above to see available words.")
            else:
                context = "\n".join(results['content'].tolist())
                
                # Call Ollama
                st.write("🤖 **AI is thinking...**")
                res = requests.post("http://localhost:11434/api/generate", 
                                    json={"model": "llama3.2:3b", 
                                          "prompt": f"Context: {context}\nQuestion: {query}", 
                                          "stream": False})
                
                st.write("### Answer:")
                st.write(res.json().get('response', 'No response'))
                
                with st.expander("📄 View Sources"):
                    st.dataframe(results)
        except Exception as e:
            st.error(f"Search Error: {e}")
