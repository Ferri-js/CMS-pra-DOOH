"""
Small helper utilities to execute parameterized SQL safely using Django's DB API.
Use these helpers instead of composing SQL strings by concatenation.

Examples:
    from core.utils.db import execute_fetchall, execute_commit

    # example using parameterized queries - intentional example
    rows = execute_fetchall("SELECT * FROM my_table WHERE id = %s", [some_id])  # sql-scan: ignore

    # example using parameterized queries - intentional example
    execute_commit("UPDATE my_table SET name = %s WHERE id = %s", [name, some_id])  # sql-scan: ignore

These functions ensure parameters are passed to the DB driver rather than interpolated into the SQL string,
reducing SQL injection risk.
"""
from django.db import connection
from typing import List, Any, Tuple, Optional


def execute_fetchall(query: str, params: Optional[List[Any]] = None) -> List[Tuple]:
    """Execute a parameterized read query and return all rows.

    Args:
        query: SQL query with placeholders (use %s for params).
        params: list/tuple of parameters.

    Returns:
        List of tuples (rows) returned by the query.
    """
    params = params or []
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def execute_fetchone(query: str, params: Optional[List[Any]] = None) -> Optional[Tuple]:
    """Execute a parameterized read query and return a single row or None."""
    params = params or []
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()


def execute_commit(query: str, params: Optional[List[Any]] = None) -> None:
    """Execute a parameterized write query (INSERT/UPDATE/DELETE) and commit.

    Use sparingly; prefer the Django ORM for most operations.
    """
    params = params or []
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        # commit is handled by Django transaction management; if you need manual commit,
        # wrap calls in transaction.atomic() in your view/logic.
