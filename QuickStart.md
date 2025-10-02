# 🚀 Quick Start Guide - Text-to-SQL Converter

Get up and running with the Text-to-SQL converter in 5 minutes!

## ⚡ Installation (2 minutes)

### Step 1: Download the Project Files

Create a directory and save these files:

```
text-to-sql-converter/
├── text_to_sql.py          # Core engine (don't run directly)
├── run_converter.py        # ⭐ CLI entry point
├── app.py                  # Streamlit web interface
├── schema.json             # Database schema
├── requirements.txt        # Dependencies
├── test_converter.py       # Tests (optional)
├── api_usage.py           # Examples (optional)
├── README.md              # Documentation
└── QUICKSTART.md          # This file
```

### Step 2: Install Dependencies

Open terminal/command prompt in your project directory:

```bash
cd text-to-sql-converter
pip install -r requirements.txt
```

**Installation takes ~2 minutes.** You'll see:
```
Installing torch...
Installing transformers...
Installing streamlit...
✓ Done!
```

### Step 3: First Run (Model Download)

**IMPORTANT:** First run downloads the AI model (~500MB). This is ONE-TIME only!

```bash
python run_converter.py
```

You'll see:
```
Loading model: cssupport/t5-small-awesome-text-to-sql
Using device: cpu
Downloading model... (this may take 2-3 minutes)
Model loaded successfully!
```

**After first run:** All subsequent runs are INSTANT (model is cached).

---

## 🎯 Three Ways to Use

### Option 1: Web Interface (EASIEST!) ⭐

**Launch:**
```bash
streamlit run app.py
```

**Browser opens automatically at:** `http://localhost:8501`

**What you get:**
- 🎨 Beautiful visual interface
- 💡 Click example queries to try them
- 📊 Browse database schema
- 🔄 Batch process multiple queries
- 📥 Download SQL as files
- 📋 Copy SQL with one click

**Perfect for:** Beginners, testing, demonstrations

---

### Option 2: Command Line (QUICK!)

**Launch:**
```bash
python run_converter.py
```

**What happens:**
1. Loads database schema
2. Shows 5 example queries with SQL outputs
3. Enters interactive mode

**Example interaction:**
```
Enter your question: Show me customers from California
Generated SQL: SELECT * FROM customers WHERE state = 'California'

Enter your question: quit
Goodbye!
```

**Commands:**
- Type any question in plain English
- Type `quit`, `exit`, or `q` to exit
- Press `Ctrl+C` to stop anytime

**Perfect for:** Quick queries, automation, scripting

---

### Option 3: Python Code (DEVELOPERS)

**Create a script:**
```python
from text_to_sql import TextToSQLConverter

# Initialize (one-time)
converter = TextToSQLConverter()

# Convert questions to SQL
sql = converter.convert("Show me all customers")
print(sql)
# Output: SELECT * FROM customers
```

**Perfect for:** Integration, web apps, APIs

---

## 📚 Try These Examples

Copy-paste these into the interface:

### ✅ Basic Queries (Start Here!)
```
Show me all customers
List all products
Get all orders
```

### 🔍 Filtered Queries
```
Show me customers from California
Find products under $50
Get orders from last month
List customers in New York
```

### 🔗 Join Queries (More Complex)
```
Show me all customers who ordered in January
List all pending orders with customer names
Find customers from New York with orders over $1000
Get products with their categories
```

### 📊 Aggregations
```
Show total sales by product category
Count customers by country
Calculate average order value
What are the top 5 products by price?
```

### 🎯 Advanced Queries
```
Show customers with more than 5 orders
Which products are out of stock?
Get customer emails for orders above $500
List orders that haven't been shipped yet
```

---

## 🎨 Customizing for Your Database

### Edit schema.json

Replace the default schema with your database structure:

```json
{
  "database_name": "my_database",
  "tables": {
    "users": {
      "columns": [
        {
          "name": "id",
          "type": "INT",
          "primary_key": true
        },
        {
          "name": "username",
          "type": "VARCHAR(50)"
        },
        {
          "name": "email",
          "type": "VARCHAR(100)"
        }
      ]
    },
    "posts": {
      "columns": [
        {
          "name": "id",
          "type": "INT",
          "primary_key": true
        },
        {
          "name": "user_id",
          "type": "INT",
          "foreign_key": "users.id"
        },
        {
          "name": "title",
          "type": "VARCHAR(255)"
        },
        {
          "name": "content",
          "type": "TEXT"
        },
        {
          "name": "created_at",
          "type": "DATETIME"
        }
      ]
    }
  }
}
```

**After editing:**
1. Save `schema.json`
2. Restart the application
3. Your database structure is now active!

---

## 🔧 Common Issues & Quick Fixes

### ❌ Issue: "Module not found"
```bash
# Fix: Install dependencies
pip install -r requirements.txt
```

### ❌ Issue: "Cannot import TextToSQLConverter"
```bash
# Fix: Don't run text_to_sql.py directly. Use:
python run_converter.py      # For CLI
streamlit run app.py         # For Web
```

### ❌ Issue: First run is slow
**This is normal!** First run downloads the model (~500MB).
- Takes: 2-5 minutes depending on internet speed
- After first run: Everything is INSTANT ⚡
- Model is cached at: `~/.cache/huggingface/`

### ❌ Issue: Out of memory
```bash
# Fix: Use the smaller model (edit text_to_sql.py)
# Change model_name to: "t5-small"
```

### ❌ Issue: Poor SQL quality
**Solutions:**
1. Add more details to `schema.json` (descriptions, foreign keys)
2. Be more specific in your questions
3. Include table/column names in questions
4. Try the example queries first to see expected format

### ❌ Issue: Streamlit port already in use
```bash
# Fix: Use a different port
streamlit run app.py --server.port 8502
```

---

## 📊 Web Interface Guide

### Main Screen

1. **Left Side: Input**
   - Type your question
   - Click "Convert to SQL" button
   - Click "Clear" to reset

2. **Right Side: Output**
   - See generated SQL
   - Copy with code block button
   - Download as .sql file

3. **Example Queries (Bottom)**
   - Click any example to load it
   - Instant conversion
   - Learn from examples

4. **Sidebar**
   - View database schema
   - Adjust settings
   - Change model parameters

### Batch Processing

1. Click "Process Multiple Questions" expander
2. Enter questions (one per line):
   ```
   Show all customers
   List top 10 products
   Get pending orders
   ```
3. Click "Process Batch"
4. Download all SQL queries at once

---

## 🎓 Learning Path

### Beginner (5 minutes)
1. ✅ Install with `pip install -r requirements.txt`
2. ✅ Run `streamlit run app.py`
3. ✅ Click 3 example queries
4. ✅ Type your own question
5. ✅ Success! You're using AI for SQL! 🎉

### Intermediate (15 minutes)
1. Try all example queries
2. Edit `schema.json` with one custom table
3. Run `python run_converter.py` for CLI
4. Test batch processing
5. Review generated SQL for accuracy

### Advanced (30 minutes)
1. Read through `api_usage.py`
2. Integrate converter into your Python project
3. Run tests: `python test_converter.py`
4. Customize the converter class
5. Try different models

---

## 💡 Pro Tips

### Tip 1: Be Specific
❌ Bad: "Show me data"
✅ Good: "Show me all customers from California"

### Tip 2: Use Example Queries
The pre-built examples show the best question formats. Try them first!

### Tip 3: Include Table Names
❌ Vague: "Show me the data"
✅ Clear: "Show me all rows from customers table"

### Tip 4: Test on Safe Database
Always test generated SQL on non-production databases first!

### Tip 5: Review Before Executing
Generated SQL is not automatically executed. Always review it first.

### Tip 6: Use Web Interface for Learning
The Streamlit interface is perfect for understanding what works best.

### Tip 7: Start Simple, Then Complex
Begin with basic SELECT queries, then try JOINs and aggregations.

---

## 🚀 Next Steps

Now that you're up and running:

### Immediate (Next 5 minutes)
- [ ] Try all 8 example queries in web interface
- [ ] Type 3 of your own questions
- [ ] Browse the database schema

### Soon (Next Hour)
- [ ] Edit `schema.json` with your database structure
- [ ] Test 10 different query types
- [ ] Try batch processing
- [ ] Review README.md for advanced features

### Later (Next Day)
- [ ] Integrate into your Python project
- [ ] Run `python test_converter.py`
- [ ] Read `api_usage.py` examples
- [ ] Try different models
- [ ] Fine-tune for your use case

---

## 📱 Quick Reference Card

### 🏃 Running the App
```bash
# Web Interface (Recommended)
streamlit run app.py

# Command Line
python run_converter.py

# Run Tests
python test_converter.py
```

### 📝 File Guide
- `run_converter.py` - Run this for CLI
- `app.py` - Run this for web UI
- `text_to_sql.py` - Import this in code (don't run)
- `schema.json` - Edit this for your database
- `requirements.txt` - Install with pip

### 🔥 Hotkeys (Web Interface)
- `Ctrl + Enter` in text box = Convert
- Click example = Load query
- `Ctrl + C` in terminal = Stop server

---

## 🎉 You're Ready!

Congratulations! You now have a working Text-to-SQL converter.

### What You Can Do:
✅ Convert natural language to SQL instantly
✅ Handle complex joins and aggregations  
✅ Batch process multiple queries
✅ Customize for any database schema
✅ Integrate into your projects

### Remember:
- First run downloads model (one-time, ~2-3 min)
- Subsequent runs are instant ⚡
- Web interface is easiest for beginners
- Always review SQL before executing
- Start with example queries

---

## 🆘 Need Help?

1. **Check README.md** - Comprehensive docs
2. **Try examples first** - Web interface has 8 examples
3. **Review schema** - Make sure it matches your database
4. **Run tests** - `python test_converter.py`
5. **Start simple** - Basic queries before complex ones

---

## 🎊 Success Checklist

After 5 minutes, you should be able to:
- [ ] Run the web interface
- [ ] Click and try example queries
- [ ] Type your own question
- [ ] See generated SQL
- [ ] Copy/download the SQL

**If you can do all of above: You're all set! 🎉**

---

**Happy Querying! Start with the web interface:**
```bash
streamlit run app.py
```

*Text-to-SQL Converter v1.0 | Built with Python, Transformers & Streamlit*