#!/usr/bin/env python3
# ==========================================
# MAIN ENTRY POINT - Run this file
# ==========================================

"""
Main entry point for Text-to-SQL Converter CLI.
Run this file instead of text_to_sql.py to avoid circular imports.

Usage: python run_converter.py
"""

from text_to_sql import TextToSQLConverter, DatabaseSchema


def main():
    """Main function for CLI interface."""
    print("=" * 60)
    print("TEXT-TO-SQL CONVERTER")
    print("=" * 60)
    print()
    
    # Initialize schema and converter
    schema = DatabaseSchema()
    print("Database Schema Loaded:")
    print(schema.get_schema_string())
    
    converter = TextToSQLConverter(schema=schema)
    print()
    
    # Example queries
    example_queries = [
        "Show me all customers who ordered in January",
        "What are the top 5 products by price?",
        "Find customers from New York with orders over $1000",
        "List all pending orders with customer names",
        "Show total sales by product category"
    ]
    
    print("Running Example Queries:")
    print("-" * 60)
    
    for i, question in enumerate(example_queries, 1):
        print(f"\n{i}. Question: {question}")
        sql = converter.convert(question)
        print(f"   SQL: {sql}")
    
    print("\n" + "=" * 60)
    print("Interactive Mode (type 'quit' to exit)")
    print("=" * 60)
    
    # Interactive mode
    while True:
        try:
            question = input("\nEnter your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not question:
                continue
            
            sql = converter.convert(question)
            print(f"\nGenerated SQL:")
            print(f"  {sql}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()