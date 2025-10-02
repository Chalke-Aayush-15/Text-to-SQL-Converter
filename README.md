# 🗄️ Text-to-SQL Converter

A powerful Python application that converts natural language questions into SQL queries using state-of-the-art transformer models.

## 📋 Features

- **AI-Powered Conversion**: Uses pre-trained T5/BERT models from HuggingFace
- **Flexible Schema**: Easy-to-configure database schema via JSON
- **Multiple Interfaces**:
  - Command-line interface (CLI)
  - Streamlit web interface
  - Programmatic API
- **Batch Processing**: Convert multiple questions at once
- **Rule-Based Fallback**: Works even without internet/model access
- **Extensible Architecture**: Easy to add new models and features

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster inference

### Installation

1. **Clone or download the project**

```bash
# Create project directory
mkdir text-to-sql-converter
cd text-to-sql-converter
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Verify installation**

```bash
python text_to_sql.py
```

## 📁 Project Structure

```
text-to-sql-converter/
├── text_to_sql.py          # Main converter engine
├── app.py                  # Streamlit web interface
├── schema.json             # Database schema configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── test_converter.py      # Unit tests
└── examples/              # Example usage scripts
    └── api_usage.py       # API usage examples
```

## 🎯 Usage

### 1. Command-Line Interface (CLI)

Run the main script directly:

```bash
python text_to_sql.py
```

This will:
- Load the database schema
- Run 5 example queries
- Start an interactive mode where you can type questions

**Example:**
```
Enter your question: Show me all customers from California
Generated SQL: SELECT * FROM customers WHERE state = 'California'
```

### 2. Streamlit Web Interface

Launch the beautiful web UI:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Visual schema browser
- Interactive query builder
- Example query templates
- Batch processing
- SQL download

### 3. Programmatic API

Use in your own Python code:

```python
from text_to_sql import TextToSQLConverter, DatabaseSchema

# Initialize
schema = DatabaseSchema()
converter = TextToSQLConverter(schema=schema)

# Convert single query
question = "Show me all customers who ordered in January"
sql = converter.convert(question)
print(sql)

# Batch convert
questions = [
    "List top 10 products",
    "Show pending orders",
    "Get customer emails"
]
results = converter.batch_convert(questions)
for q, sql in results:
    print(f"{q} -> {sql}")
```

## ⚙️ Configuration

### Database Schema

Edit `schema.json` to match your database structure:

```json
{
  "database_name": "your_database",
  "tables": {
    "your_table": {
      "columns": [
        {
          "name": "column_name",
          "type": "INT",
          "primary_key": true
        }
      ]
    }
  }
}
```

### Changing Models

Modify the model in `text_to_sql.py`:

```python
# Use different HuggingFace models
converter = TextToSQLConverter(
    model_name="tscholak/improved-text-to-sql"
    # or "google/flan-t5-large"
    # or "NumbersStation/nsql-350M"
)
```

**Recommended Models:**
- `cssupport/t5-small-awesome-text-to-sql` (lightweight, fast)
- `tscholak/improved-text-to-sql` (better accuracy)
- `NumbersStation/nsql-350M` (specialized for SQL)
- `google/flan-t5-base` (general purpose)

## 📝 Example Queries

Here are 5+ example queries with expected outputs:

### Example 1: Customer Orders in Specific Month
**Question:** "Show me all customers who ordered in January"

**Generated SQL:**
```sql
SELECT DISTINCT c.* 
FROM customers c 
JOIN orders o ON c.customer_id = o.customer_id 
WHERE MONTH(o.order_date) = 1
```

### Example 2: Top Products by Price
**Question:** "What are the top 5 products by price?"

**Generated SQL:**
```sql
SELECT * 
FROM products 
ORDER BY price DESC 
LIMIT 5
```

### Example 3: Filtered Customer Search
**Question:** "Find customers from New York with orders over $1000"

**Generated SQL:**
```sql
SELECT DISTINCT c.* 
FROM customers c 
JOIN orders o ON c.customer_id = o.customer_id 
WHERE c.city = 'New York' AND o.total_amount > 1000
```

### Example 4: Orders with Customer Details
**Question:** "List all pending orders with customer names"

**Generated SQL:**
```sql
SELECT o.*, c.name 
FROM orders o 
JOIN customers c ON o.customer_id = c.customer_id 
WHERE o.status = 'pending'
```

### Example 5: Aggregate Sales Analysis
**Question:** "Show total sales by product category"

**Generated SQL:**
```sql
SELECT p.category, SUM(oi.price * oi.quantity) as total_sales 
FROM products p 
JOIN order_items oi ON p.product_id = oi.product_id 
GROUP BY p.category
```

### Example 6: Count Queries
**Question:** "How many customers are from each country?"

**Generated SQL:**
```sql
SELECT country, COUNT(*) as customer_count 
FROM customers 
GROUP BY country
```

### Example 7: Date Range Queries
**Question:** "Show orders placed in the last 30 days"

**Generated SQL:**
```sql
SELECT * 
FROM orders 
WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
```

## 🔧 Advanced Features

### Custom Model Fine-tuning

To fine-tune on your own data:

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import Trainer, TrainingArguments

# Load your training data
# train_dataset = ...

# Fine-tune
training_args = TrainingArguments(
    output_dir="./fine-tuned-model",
    num_train_epochs=3,
    per_device_train_batch_size=8,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

trainer.train()
```

### Adding New SQL Dialects

Extend the converter to support different SQL dialects (PostgreSQL, MySQL, etc.):

```python
class PostgreSQLConverter(TextToSQLConverter):
    def _clean_sql(self, sql: str) -> str:
        sql = super()._clean_sql(sql)
        # Add PostgreSQL-specific formatting
        sql = sql.replace("LIMIT", "FETCH FIRST ... ROWS ONLY")
        return sql
```

## 🧪 Testing

Run unit tests:

```bash
python test_converter.py
```

Or with pytest:

```bash
pytest test_converter.py -v
```

## 📊 Performance Tips

1. **Use GPU**: Install CUDA version of PyTorch for 10-50x speedup
2. **Batch Processing**: Process multiple queries together
3. **Model Size**: Start with smaller models (t5-small) for faster inference
4. **Caching**: Results are cached in Streamlit automatically

## 🐛 Troubleshooting

### Issue: Model download fails
**Solution:** Check internet connection or use cached models:
```python
converter = TextToSQLConverter(
    model_name="cssupport/t5-small-awesome-text-to-sql",
    cache_dir="./models"
)
```

### Issue: Out of memory
**Solution:** Use smaller model or reduce batch size:
```python
# Use t5-small instead of t5-base
converter = TextToSQLConverter(model_name="t5-small")
```

### Issue: Poor SQL quality
**Solution:** 
1. Provide more detailed schema information
2. Use a larger/better model
3. Fine-tune on your specific domain

## 🔒 Security Considerations

⚠️ **Important**: This tool generates SQL queries but does NOT execute them.

**Best Practices:**
- Always review generated SQL before execution
- Use parameterized queries to prevent SQL injection
- Test on non-production databases first
- Implement proper access controls
- Sanitize user inputs

## 🤝 Contributing

To extend this project:

1. **Add new models**: Update `model_name` in initialization
2. **Enhance schema**: Add more metadata to `schema.json`
3. **Improve UI**: Customize Streamlit interface in `app.py`
4. **Add features**: Create new methods in `TextToSQLConverter` class

## 📚 Resources

- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Spider Dataset](https://yale-lily.github.io/spider) - Text-to-SQL benchmark
- [WikiSQL](https://github.com/salesforce/WikiSQL) - Training data

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 👥 Support

For issues or questions:
1. Check the troubleshooting section
2. Review example usage
3. Consult HuggingFace model documentation

## 🎓 Learn More

This project demonstrates:
- NLP with transformer models
- Sequence-to-sequence generation
- Web application development with Streamlit
- Database schema modeling
- Production-ready Python architecture

Perfect for learning or building production SQL generation systems!

---

**Built with ❤️ using Python, Transformers, and Streamlit**