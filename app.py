import os
import re
import streamlit as st

def file_exists(filepath):
    """Check if the file exists."""
    return os.path.isfile(filepath)

def clean_text(text):
    """Remove markdown formatting and URLs while preserving essential content."""
    text = re.sub(r'http\S+|\[.*?\]\(.*?\)', '', text)
    text = text.replace('**', '').replace('__', '').replace('#', '')
    return text.strip()

def find_lines_with_headings(content, keyword):
    """Find lines containing the keyword along with their headings."""
    sections = re.split(r'\n\s*\n', content)
    results = []
    current_heading = "Untitled Section"

    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue

        # Detect heading
        if lines[0].strip().endswith(':') or lines[0].isupper():
            current_heading = lines[0].strip(':').strip()

        # Check each line for the keyword
        for line in lines:
            if re.search(r'\b' + re.escape(keyword) + r'\b', line, re.IGNORECASE):
                cleaned_line = clean_text(line)
                if cleaned_line:
                    results.append((current_heading, cleaned_line))

    return results if results else None

def search_definition(filepath, keyword):
    """Search for keyword and return matching lines with headings."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        return find_lines_with_headings(content, keyword)

# Streamlit UI
st.set_page_config(page_title="FitWellHub Data Assistant 📚", layout="wide")
st.title("📚 FitWellHub Data Assistant")


file_path = "Fit.txt"

if not file_exists(file_path):
    st.error("⚠️ Data file 'Fit.txt' not found in the app directory.")
else:
  #  st.success("✅ Fit.txt loaded and ready for queries!")

    query = st.text_input("Enter your question:")

    # 🔘 Add search button
    if st.button("Search"):
        if query:
            if query.lower() in ["developer", "who is your developer?", "what is your developer name?"]:
                st.info("👨‍💻 Developer: Rao Zain")
            elif query.lower() == "exit":
                st.stop()
            else:
                keyword = re.sub(r'^(what is|tell me about|explain|show|where)\s+', '', query.lower()).strip(' ?')
                results = search_definition(file_path, keyword)

                if results:
                    st.subheader(f"🔍 Results for: **{keyword}**")
                    for i, (heading, line) in enumerate(results[:10]):
                        with st.expander(f"📖 {heading} — Match {i+1}"):
                            st.write(line)
                else:
                    st.warning(f"No content found for **{keyword}**.")
        else:
            st.error("❌ Please enter a question to search.")


