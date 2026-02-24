#!/usr/bin/env python3
"""Compat module for legacy tests.
Re-exports public API from narrator.py and exposes subprocess for mocking.
"""
import subprocess  # noqa: F401
from narrator import *  # noqa: F401,F403
