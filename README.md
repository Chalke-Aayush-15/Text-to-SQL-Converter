# 🚀 Quick Start Guide - Text-to-SQL Converter

Get up and running with the Text-to-SQL converter in 5 minutes!

## ⚡ Installation (2 minutes)

### Step 1: Download the Project Files

Save these files to a directory called `text-to-sql-converter`:

```
text-to-sql-converter/
├── text_to_sql.py          # Main converter
├── app.py                  # Streamlit UI
├── schema.json             # Database schema
├── requirements.txt        # Dependencies
├── test_converter.py       # Tests
├── api_usage.py           # API examples
└── README.md              # Documentation
```

### Step 2: Install Dependencies

Open terminal/command prompt and run:

```bash
cd text-to-sql-converter
pip install -r requirements.txt
```

**That's it!** You're ready to go.

---

## 🎯 Usage Options

### Option 1: Command Line (Fastest)

Run the main script:

```bash
python text_to_sql.py
```

**You'll see:**
1. Database schema loaded
2. 5 example queries with SQL outputs
3. Interactive prompt where you can type questions

**Example interaction:**
```
Enter your question: Show me customers from New York
Generated SQL: SELECT * FROM customers WHERE city = 'New York'
```

---

### Option 2: Web Interface (Most User-Friendly)

Launch the Streamlit app:

```bash
streamlit run app.py
```

**Your browser will open automatically with:**
- Beautiful visual interface
- Example query buttons
- Schema browser
- Copy/download SQL buttons
- Batch processing

**Access at:** `http://localhost:8501`

---

### Option 3: Python API (For Developers)

Use in your own code:

```python
from text_to_sql import TextToSQLConverter

# Initialize
converter = TextToSQLConverter()

# Convert a question
sql = converter.convert("Show me all customers")
print(sql)
# Output: SELECT * FROM customers
```

---

## 📊 Try These Examples

Copy and paste these questions:

### Basic Queries
```
Show me all customers
List all products
Get all orders
```

### Filtered Queries
```
Show me customers from California
Find products under $50
Get orders from last month
```

### Joins & Complex Queries
```
Show me all customers who ordered in January
List all pending orders with customer names
Find customers from New York with orders over $1000
```

### Aggregations
```
Show total sales by product category
Count customers by country
Calculate average order value
```

### Top N Queries
```
What are the top 5 products by price?
Show the 10 most recent orders
List top customers by purchase amount
```

---

## 🎨 Customizing Your Database Schema

Edit `schema.json` to match your database:

```json
{
  "database_name": "your_database",
  "tables": {
    "your_table": {
      "columns": [
        {
          "name": "id",
          "type": "INT",
          "primary_key": true
        },
        {
          "name": "name",
          "type": "VARCHAR(255)"
        }
      ]
    }
  }
}
```

**After editing:** Restart the application to load your schema!

---

## 🔧 Common Issues & Solutions

### Issue: "Module not found"
**Solution:** Install requirements:
```bash
pip install -r requirements.txt
```

### Issue: Model download is slow
**Solution:** First run downloads the model (~500MB). Subsequent runs are instant.

### Issue: Out of memory
**Solution:** The default model is lightweight. If issues persist, restart Python.

### Issue: Poor SQL quality
**Solutions:**
1. Provide more detailed schema in `schema.json`
2. Use more specific questions
3. Try the web interface with examples

---

## 📈 Performance Tips

### Speed Up Inference
1. **First run**: Downloads model (slow, one-time only)
2. **Subsequent runs**: Uses cached model (fast)
3. **Batch processing**: Process multiple queries together for efficiency

### Improve Accuracy
1. **Add descriptions** to schema columns
2. **Use specific questions** with table/column names
3. **Provide examples** in your domain
4. **Test with example queries** first

---

## 🎓 Learning Path

### Beginner (5 minutes)
1. ✅ Install dependencies
2. ✅ Run `python text_to_sql.py`
3. ✅ Try 3-5 example questions
4. ✅ Edit `schema.json` with one custom table

### Intermediate (15 minutes)
1. Launch Streamlit app
2. Try all example queries
3. Use batch processing
4. Review generated SQL for accuracy
5. Customize schema for your database

### Advanced (30 minutes)
1. Read `api_usage.py` examples
2. Integrate into your Python project
3. Run test suite: `python test_converter.py`
4. Try different models in the code
5. Implement error handling and validation

---

## 💡 Pro Tips

1. **Test First**: Always test generated SQL on a non-production database
2. **Be Specific**: "Show customers in California" is better than "show data"
3. **Use Examples**: The web interface has great example queries
4. **Batch Process**: Convert multiple queries at once for efficiency
5. **Cache Results**: Generated SQL doesn't change for same questions
6. **Review SQL**: Always review before executing on production data

---

## 🎉 Next Steps

Now that you're up and running:

1. **Explore Examples**: Try all the example queries
2. **Customize Schema**: Edit `schema.json` for your database
3. **Read Documentation**: Check `README.md` for advanced features
4. **Run Tests**: Execute `python test_converter.py`
5. **API Integration**: See `api_usage.py` for code examples

---

## 📚 Quick Reference

### Command Summary
```bash
# CLI mode
python text_to_sql.py

# Web UI
streamlit run app.py

# Run tests
python test_converter.py

# API examples
python api_usage.py
```

### File Reference
- `text_to_sql.py` - Core engine
- `app.py` - Web interface
- `schema.json` - Database config
- `requirements.txt` - Dependencies
- `test_converter.py` - Unit tests
- `api_usage.py` - Integration examples

---

## ❓ Getting Help

1. **Check README.md** - Comprehensive documentation
2. **Review examples** - `api_usage.py` has 10+ examples
3. **Run tests** - `test_converter.py` shows usage patterns
4. **Try web UI** - Streamlit app has built-in help

---

## 🎊 You're All Set!

You now have a working Text-to-SQL converter. Start converting natural language to SQL queries instantly!

**Happy Querying! 🚀**

---

*Text-to-SQL Converter v1.0 - Built with Python, Transformers, and Streamlit*