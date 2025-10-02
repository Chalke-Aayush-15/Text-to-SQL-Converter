# ==========================================
# TEXT-TO-SQL CONVERTER - MAIN APPLICATION
# ==========================================

"""
Text-to-SQL Converter System
Converts natural language questions into SQL queries using transformer models.

Author: Aayush Chalke
Version: 1.0
"""

import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


# Ensure we're not in a circular import
if __name__ != "__main__":
    # This file is being imported, not run directly
    pass


class DatabaseSchema:
    """Manages database schema configuration."""
    
    def __init__(self, schema_file: str = "schema.json"):
        """
        Initialize database schema.
        
        Args:
            schema_file: Path to JSON file containing schema definition
        """
        self.schema_file = schema_file
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict:
        """Load schema from JSON file or create default."""
        if os.path.exists(self.schema_file):
            with open(self.schema_file, 'r') as f:
                return json.load(f)
        else:
            # Default schema
            default_schema = {
                "database_name": "ecommerce",
                "tables": {
                    "customers": {
                        "columns": [
                            {"name": "customer_id", "type": "INT", "primary_key": True},
                            {"name": "name", "type": "VARCHAR(255)"},
                            {"name": "email", "type": "VARCHAR(255)"},
                            {"name": "city", "type": "VARCHAR(100)"},
                            {"name": "country", "type": "VARCHAR(100)"},
                            {"name": "created_at", "type": "DATETIME"}
                        ]
                    },
                    "orders": {
                        "columns": [
                            {"name": "order_id", "type": "INT", "primary_key": True},
                            {"name": "customer_id", "type": "INT", "foreign_key": "customers.customer_id"},
                            {"name": "order_date", "type": "DATE"},
                            {"name": "total_amount", "type": "DECIMAL(10,2)"},
                            {"name": "status", "type": "VARCHAR(50)"}
                        ]
                    },
                    "products": {
                        "columns": [
                            {"name": "product_id", "type": "INT", "primary_key": True},
                            {"name": "name", "type": "VARCHAR(255)"},
                            {"name": "price", "type": "DECIMAL(10,2)"},
                            {"name": "category", "type": "VARCHAR(100)"},
                            {"name": "stock_quantity", "type": "INT"}
                        ]
                    },
                    "order_items": {
                        "columns": [
                            {"name": "item_id", "type": "INT", "primary_key": True},
                            {"name": "order_id", "type": "INT", "foreign_key": "orders.order_id"},
                            {"name": "product_id", "type": "INT", "foreign_key": "products.product_id"},
                            {"name": "quantity", "type": "INT"},
                            {"name": "price", "type": "DECIMAL(10,2)"}
                        ]
                    }
                }
            }
            self._save_schema(default_schema)
            return default_schema
    
    def _save_schema(self, schema: Dict):
        """Save schema to JSON file."""
        with open(self.schema_file, 'w') as f:
            json.dump(schema, f, indent=2)
    
    def get_schema_string(self) -> str:
        """Get formatted schema string for model input."""
        schema_str = f"Database: {self.schema['database_name']}\n\n"
        
        for table_name, table_info in self.schema['tables'].items():
            schema_str += f"Table: {table_name}\n"
            schema_str += "Columns:\n"
            for col in table_info['columns']:
                col_str = f"  - {col['name']} ({col['type']}"
                if col.get('primary_key'):
                    col_str += ", PRIMARY KEY"
                if col.get('foreign_key'):
                    col_str += f", FOREIGN KEY -> {col['foreign_key']}"
                col_str += ")"
                schema_str += col_str + "\n"
            schema_str += "\n"
        
        return schema_str
    
    def get_table_names(self) -> List[str]:
        """Get list of all table names."""
        return list(self.schema['tables'].keys())
    
    def get_columns(self, table_name: str) -> List[str]:
        """Get list of column names for a specific table."""
        if table_name in self.schema['tables']:
            return [col['name'] for col in self.schema['tables'][table_name]['columns']]
        return []


class TextToSQLConverter:
    """Main Text-to-SQL conversion engine."""
    
    def __init__(self, model_name: str = "cssupport/t5-small-awesome-text-to-sql", 
                 schema: DatabaseSchema = None):
        """
        Initialize the Text-to-SQL converter.
        
        Args:
            model_name: HuggingFace model identifier
            schema: DatabaseSchema object
        """
        self.model_name = model_name
        self.schema = schema or DatabaseSchema()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        print(f"Loading model: {model_name}")
        print(f"Using device: {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to rule-based system...")
            self.model = None
            self.tokenizer = None
    
    def _prepare_input(self, question: str) -> str:
        """
        Prepare input text with schema context.
        
        Args:
            question: Natural language question
            
        Returns:
            Formatted input string
        """
        # Create a simplified schema representation
        tables = self.schema.get_table_names()
        table_info = []
        
        for table in tables:
            columns = self.schema.get_columns(table)
            table_info.append(f"{table} ( {', '.join(columns)} )")
        
        # Format: "question | tables"
        schema_context = " | ".join(table_info)
        input_text = f"{question} | {schema_context}"
        
        return input_text
    
    def convert(self, question: str, max_length: int = 512) -> str:
        """
        Convert natural language question to SQL query.
        
        Args:
            question: Natural language question
            max_length: Maximum length of generated SQL
            
        Returns:
            SQL query string
        """
        if self.model is None:
            return self._rule_based_conversion(question)
        
        try:
            # Prepare input
            input_text = self._prepare_input(question)
            
            # Tokenize
            inputs = self.tokenizer(
                input_text,
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate SQL
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=5,
                    early_stopping=True
                )
            
            # Decode
            sql_query = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return self._clean_sql(sql_query)
            
        except Exception as e:
            print(f"Error during conversion: {e}")
            return self._rule_based_conversion(question)
    
    def _clean_sql(self, sql: str) -> str:
        """Clean and format SQL query."""
        sql = sql.strip()
        
        # Remove extra spaces
        sql = ' '.join(sql.split())
        
        # Ensure proper capitalization of SQL keywords
        keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'GROUP BY', 
                   'ORDER BY', 'LIMIT', 'AND', 'OR', 'HAVING', 'AS']
        
        for keyword in keywords:
            sql = sql.replace(keyword.lower(), keyword)
            sql = sql.replace(keyword.capitalize(), keyword)
        
        return sql
    
    def _rule_based_conversion(self, question: str) -> str:
        """
        Fallback rule-based conversion for basic queries.
        
        Args:
            question: Natural language question
            
        Returns:
            SQL query string
        """
        question_lower = question.lower()
        
        # Simple pattern matching
        if "all customers" in question_lower or "show customers" in question_lower:
            if "january" in question_lower:
                return "SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE MONTH(o.order_date) = 1"
            return "SELECT * FROM customers"
        
        elif "top" in question_lower and "products" in question_lower:
            if "price" in question_lower:
                return "SELECT * FROM products ORDER BY price DESC LIMIT 5"
            return "SELECT * FROM products LIMIT 5"
        
        elif "pending orders" in question_lower:
            if "customer" in question_lower:
                return "SELECT o.*, c.name FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.status = 'pending'"
            return "SELECT * FROM orders WHERE status = 'pending'"
        
        elif "total sales" in question_lower and "category" in question_lower:
            return "SELECT p.category, SUM(oi.price * oi.quantity) as total_sales FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.category"
        
        elif "new york" in question_lower and "1000" in question_lower:
            return "SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE c.city = 'New York' AND o.total_amount > 1000"
        
        else:
            # Generic fallback
            return "SELECT * FROM customers LIMIT 10"
    
    def batch_convert(self, questions: List[str]) -> List[Tuple[str, str]]:
        """
        Convert multiple questions to SQL.
        
        Args:
            questions: List of natural language questions
            
        Returns:
            List of (question, sql) tuples
        """
        results = []
        for question in questions:
            sql = self.convert(question)
            results.append((question, sql))
        return results


def main():
    """Main function for CLI interface - DO NOT USE, use run_converter.py instead."""
    print("Please run 'python run_converter.py' instead to avoid circular imports.")
    print("Or use 'streamlit run app.py' for the web interface.")


if __name__ == "__main__":
    print("=" * 60)
    print("WARNING: Do not run this file directly!")
    print("=" * 60)
    print("\nThis file contains the converter classes and should be imported.")
    print("\nTo use the Text-to-SQL converter, please run:")
    print("  python run_converter.py       # For CLI interface")
    print("  streamlit run app.py          # For Web interface")
    print("  python api_usage.py           # For API examples")
    print("=" * 60)