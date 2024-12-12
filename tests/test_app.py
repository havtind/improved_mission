"""test_app.py"""
from streamlit.testing.v1 import AppTest


def test_home_page():
    """tester startsiden til appen"""
    at = AppTest.from_file("app/Home.py", default_timeout=30).run()
    assert not at.exception

def test_data_page():
    """tester å laste inn datasettet"""
    at = AppTest.from_file("app/pages/1_Raw_data.py", default_timeout=30).run()
    assert not at.exception

def test_analysis_page():
    """tester den mest omfattende siden, inkluderer generering av plots"""
    at = AppTest.from_file("app/pages/2_Exploratory_analysis.py", default_timeout=30).run()
    assert not at.exception



 