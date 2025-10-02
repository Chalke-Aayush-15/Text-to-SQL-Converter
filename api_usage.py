# ==========================================
# API USAGE EXAMPLES
# ==========================================

"""
Examples of using the Text-to-SQL Converter as an API/library.
This demonstrates various use cases and integration patterns.
"""

from text_to_sql import TextToSQLConverter, DatabaseSchema
import json


def example_1_basic_usage():
    """Example 1: Basic conversion of a single query."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Initialize converter
    converter = TextToSQLConverter()
    
    # Convert a question
    question = "Show me all customers from California"
    sql = converter.convert(question)
    
    print(f"Question: {question}")
    print(f"SQL: {sql}")
    print()


def example_2_custom_schema():
    """Example 2: Using a custom database schema."""
    print("=" * 60)
    print("EXAMPLE 2: Custom Schema")
    print("=" * 60)
    
    # Define custom schema
    custom_schema = {
        "database_name": "library",
        "tables": {
            "books": {
                "columns": [
                    {"name": "book_id", "type": "INT", "primary_key": True},
                    {"name": "title", "type": "VARCHAR(255)"},
                    {"name": "author", "type": "VARCHAR(255)"},
                    {"name": "isbn", "type": "VARCHAR(20)"},
                    {"name": "published_year", "type": "INT"}
                ]
            },
            "members": {
                "columns": [
                    {"name": "member_id", "type": "INT", "primary_key": True},
                    {"name": "name", "type": "VARCHAR(255)"},
                    {"name": "email", "type": "VARCHAR(255)"},
                    {"name": "join_date", "type": "DATE"}
                ]
            },
            "loans": {
                "columns": [
                    {"name": "loan_id", "type": "INT", "primary_key": True},
                    {"name": "book_id", "type": "INT", "foreign_key": "books.book_id"},
                    {"name": "member_id", "type": "INT", "foreign_key": "members.member_id"},
                    {"name": "loan_date", "type": "DATE"},
                    {"name": "return_date", "type": "DATE"}
                ]
            }
        }
    }
    
    # Save custom schema
    with open("library_schema.json", "w") as f:
        json.dump(custom_schema, f, indent=2)
    
    # Use custom schema
    schema = DatabaseSchema("library_schema.json")
    converter = TextToSQLConverter(schema=schema)
    
    # Convert library-specific questions
    questions = [
        "Show all books published after 2020",
        "List members who joined this year",
        "Find all overdue loans"
    ]
    
    for question in questions:
        sql = converter.convert(question)
        print(f"Q: {question}")
        print(f"SQL: {sql}\n")


def example_3_batch_processing():
    """Example 3: Batch processing multiple queries."""
    print("=" * 60)
    print("EXAMPLE 3: Batch Processing")
    print("=" * 60)
    
    converter = TextToSQLConverter()
    
    # Multiple questions
    questions = [
        "Show all customers",
        "List top 10 products by price",
        "Get pending orders",
        "Show customers with more than 5 orders",
        "Calculate average order value"
    ]
    
    # Batch convert
    results = converter.batch_convert(questions)
    
    print(f"Converted {len(results)} queries:\n")
    for i, (question, sql) in enumerate(results, 1):
        print(f"{i}. {question}")
        print(f"   → {sql}\n")


def example_4_integration_pattern():
    """Example 4: Integration pattern for web applications."""
    print("=" * 60)
    print("EXAMPLE 4: Web Application Integration")
    print("=" * 60)
    
    class QueryService:
        """Service class for handling text-to-SQL in web apps."""
        
        def __init__(self):
            self.converter = TextToSQLConverter()
            self.query_cache = {}
        
        def process_query(self, user_question: str) -> dict:
            """
            Process user question and return structured response.
            
            Returns:
                dict with status, sql, and metadata
            """
            # Check cache
            if user_question in self.query_cache:
                return self.query_cache[user_question]
            
            try:
                sql = self.converter.convert(user_question)
                
                response = {
                    "status": "success",
                    "question": user_question,
                    "sql": sql,
                    "timestamp": "2025-10-01T12:00:00Z",
                    "cached": False
                }
                
                # Cache result
                self.query_cache[user_question] = response
                
                return response
                
            except Exception as e:
                return {
                    "status": "error",
                    "question": user_question,
                    "error": str(e),
                    "timestamp": "2025-10-01T12:00:00Z"
                }
    
    # Use the service
    service = QueryService()
    
    # Simulate API calls
    user_inputs = [
        "Show me recent orders",
        "Find high-value customers",
        "Show me recent orders"  # Duplicate - will use cache
    ]
    
    for user_input in user_inputs:
        result = service.process_query(user_input)
        print(f"Input: {user_input}")
        print(f"Response: {json.dumps(result, indent=2)}\n")


def example_5_error_handling():
    """Example 5: Proper error handling."""
    print("=" * 60)
    print("EXAMPLE 5: Error Handling")
    print("=" * 60)
    
    converter = TextToSQLConverter()
    
    # Test various edge cases
    test_cases = [
        ("", "Empty string"),
        ("   ", "Whitespace only"),
        ("Show me customers", "Normal query"),
        ("This is a very long question with lots of irrelevant information about weather and sports and politics", "Very long query"),
        ("SELECT * FROM users", "Already SQL query"),
    ]
    
    for query, description in test_cases:
        print(f"Test: {description}")
        print(f"Input: '{query}'")
        
        try:
            sql = converter.convert(query)
            print(f"Output: {sql}")
            print("Status: ✓ Success\n")
        except Exception as e:
            print(f"Error: {e}")
            print("Status: ✗ Failed\n")


def example_6_model_comparison():
    """Example 6: Comparing different models."""
    print("=" * 60)
    print("EXAMPLE 6: Model Comparison")
    print("=" * 60)
    
    schema = DatabaseSchema()
    
    # Different models to try
    models = [
        "cssupport/t5-small-awesome-text-to-sql",
        # Add more models as needed
    ]
    
    question = "Show top 5 customers by total purchases"
    
    print(f"Question: {question}\n")
    
    for model_name in models:
        print(f"Model: {model_name}")
        try:
            converter = TextToSQLConverter(model_name=model_name, schema=schema)
            sql = converter.convert(question)
            print(f"SQL: {sql}\n")
        except Exception as e:
            print(f"Error: {e}\n")


def example_7_streaming_queries():
    """Example 7: Processing queries from a file or stream."""
    print("=" * 60)
    print("EXAMPLE 7: Streaming/File Processing")
    print("=" * 60)
    
    # Create sample queries file
    sample_queries = """Show all customers
List products under $50
Get orders from last month
Find customers without orders
Show products by category"""
    
    with open("sample_queries.txt", "w") as f:
        f.write(sample_queries)
    
    # Process queries from file
    converter = TextToSQLConverter()
    
    print("Processing queries from file...\n")
    
    with open("sample_queries.txt", "r") as f:
        for line_num, line in enumerate(f, 1):
            query = line.strip()
            if query:
                sql = converter.convert(query)
                print(f"{line_num}. {query}")
                print(f"   {sql}\n")


def example_8_validation_pipeline():
    """Example 8: SQL validation and safety checks."""
    print("=" * 60)
    print("EXAMPLE 8: Validation Pipeline")
    print("=" * 60)
    
    def validate_sql(sql: str) -> dict:
        """Validate generated SQL for safety."""
        issues = []
        warnings = []
        
        # Check for dangerous operations
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE']
        for keyword in dangerous_keywords:
            if keyword in sql.upper():
                issues.append(f"Contains dangerous keyword: {keyword}")
        
        # Check for missing WHERE clause in DELETE/UPDATE
        if 'DELETE' in sql.upper() and 'WHERE' not in sql.upper():
            warnings.append("DELETE without WHERE clause")
        
        # Check for SELECT *
        if 'SELECT *' in sql.upper():
            warnings.append("Using SELECT * - consider specifying columns")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    converter = TextToSQLConverter()
    
    test_queries = [
        "Show all customers",
        "Delete old records",
        "List all products"
    ]
    
    for query in test_queries:
        sql = converter.convert(query)
        validation = validate_sql(sql)
        
        print(f"Query: {query}")
        print(f"SQL: {sql}")
        print(f"Valid: {'✓' if validation['valid'] else '✗'}")
        
        if validation['issues']:
            print(f"Issues: {', '.join(validation['issues'])}")
        if validation['warnings']:
            print(f"Warnings: {', '.join(validation['warnings'])}")
        print()


def example_9_contextual_conversion():
    """Example 9: Using context for better conversions."""
    print("=" * 60)
    print("EXAMPLE 9: Contextual Conversion")
    print("=" * 60)
    
    class ContextualConverter:
        """Converter that maintains conversation context."""
        
        def __init__(self):
            self.converter = TextToSQLConverter()
            self.context = {
                "last_table": None,
                "last_filters": [],
                "conversation_history": []
            }
        
        def convert_with_context(self, question: str) -> str:
            """Convert using conversation context."""
            # Add simple context awareness
            enhanced_question = question
            
            # If question references "it" or "them", use last table
            if self.context["last_table"] and ("it" in question.lower() or "them" in question.lower()):
                enhanced_question = question.replace("it", self.context["last_table"])
                enhanced_question = enhanced_question.replace("them", self.context["last_table"])
            
            sql = self.converter.convert(enhanced_question)
            
            # Update context
            self.context["conversation_history"].append({
                "question": question,
                "sql": sql
            })
            
            # Extract table name from SQL
            if "FROM" in sql:
                parts = sql.split("FROM")
                if len(parts) > 1:
                    table = parts[1].split()[0].strip()
                    self.context["last_table"] = table
            
            return sql
    
    contextual = ContextualConverter()
    
    # Simulated conversation
    conversation = [
        "Show me all customers",
        "Now show me only the ones from California",
        "Sort them by name"
    ]
    
    print("Conversation with context:\n")
    for turn in conversation:
        sql = contextual.convert_with_context(turn)
        print(f"User: {turn}")
        print(f"SQL: {sql}\n")


def example_10_performance_monitoring():
    """Example 10: Performance monitoring and metrics."""
    print("=" * 60)
    print("EXAMPLE 10: Performance Monitoring")
    print("=" * 60)
    
    import time
    
    class MonitoredConverter:
        """Converter with performance monitoring."""
        
        def __init__(self):
            self.converter = TextToSQLConverter()
            self.metrics = {
                "total_queries": 0,
                "total_time": 0,
                "errors": 0
            }
        
        def convert_with_metrics(self, question: str) -> dict:
            """Convert and collect metrics."""
            start_time = time.time()
            
            try:
                sql = self.converter.convert(question)
                success = True
                error = None
            except Exception as e:
                sql = None
                success = False
                error = str(e)
                self.metrics["errors"] += 1
            
            elapsed = time.time() - start_time
            
            self.metrics["total_queries"] += 1
            self.metrics["total_time"] += elapsed
            
            return {
                "sql": sql,
                "success": success,
                "error": error,
                "time_ms": round(elapsed * 1000, 2)
            }
        
        def get_stats(self) -> dict:
            """Get performance statistics."""
            if self.metrics["total_queries"] > 0:
                avg_time = self.metrics["total_time"] / self.metrics["total_queries"]
            else:
                avg_time = 0
            
            return {
                "total_queries": self.metrics["total_queries"],
                "total_time_sec": round(self.metrics["total_time"], 2),
                "average_time_ms": round(avg_time * 1000, 2),
                "errors": self.metrics["errors"],
                "success_rate": round((self.metrics["total_queries"] - self.metrics["errors"]) / max(1, self.metrics["total_queries"]) * 100, 2)
            }
    
    monitored = MonitoredConverter()
    
    # Process queries
    queries = [
        "Show all customers",
        "List products",
        "Get orders",
        "Find high-value transactions",
        "Show analytics dashboard"
    ]
    
    print("Processing queries with monitoring...\n")
    
    for query in queries:
        result = monitored.convert_with_metrics(query)
        print(f"Query: {query}")
        print(f"Time: {result['time_ms']}ms")
        print(f"Success: {'✓' if result['success'] else '✗'}")
        print()
    
    # Show statistics
    stats = monitored.get_stats()
    print("=" * 40)
    print("PERFORMANCE STATISTICS")
    print("=" * 40)
    for key, value in stats.items():
        print(f"{key}: {value}")


def main():
    """Run all examples."""
    examples = [
        ("Basic Usage", example_1_basic_usage),
        ("Custom Schema", example_2_custom_schema),
        ("Batch Processing", example_3_batch_processing),
        ("Web Integration", example_4_integration_pattern),
        ("Error Handling", example_5_error_handling),
        ("Model Comparison", example_6_model_comparison),
        ("File Processing", example_7_streaming_queries),
        ("Validation Pipeline", example_8_validation_pipeline),
        ("Contextual Conversion", example_9_contextual_conversion),
        ("Performance Monitoring", example_10_performance_monitoring)
    ]
    
    print("\n")
    print("*" * 60)
    print("TEXT-TO-SQL API USAGE EXAMPLES")
    print("*" * 60)
    print("\nSelect an example to run:")
    
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print(f"{len(examples) + 1}. Run All Examples")
    print("0. Exit")
    
    try:
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            print("Goodbye!")
            return
        elif choice == str(len(examples) + 1):
            # Run all examples
            for name, func in examples:
                print(f"\n\nRunning: {name}")
                try:
                    func()
                except Exception as e:
                    print(f"Error in {name}: {e}")
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                examples[idx][1]()
            else:
                print("Invalid choice!")
    
    except KeyboardInterrupt:
        print("\nInterrupted!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()