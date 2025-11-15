"""
Infrastructure ViewSets

This module contains Django REST Framework ViewSets that handle HTTP requests
and delegate business logic to Use Cases from the application layer.

ViewSets follow these principles:
- No business logic - only request/response handling
- Input validation using DTOs
- Error handling and HTTP status codes
- Delegation to Use Cases for business operations
"""
