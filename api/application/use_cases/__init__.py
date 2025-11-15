"""
Application Use Cases

This module contains all use cases that orchestrate business operations.
Use cases coordinate between domain entities, domain services, and repositories
to fulfill specific application requirements.

Structure:
- booking_use_cases: Operations related to booking management
- room_use_cases: Operations related to room management
- manager_use_cases: Operations related to manager management
- location_use_cases: Operations related to location management

Each use case follows the pattern:
1. Validate input
2. Apply domain rules via domain services
3. Coordinate repository operations
4. Return results
"""
