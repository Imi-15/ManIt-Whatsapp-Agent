"""
workflows/__init__.py - Workflows Package
Exports workflow graphs for easy importing.
"""

from workflows.research_flow import create_workflow, run_workflow, app_graph

__all__ = ["create_workflow", "run_workflow", "app_graph"]
