import pytest
from unittest.mock import patch
from ..monitoring.metrics import collect_metrics

def test_collect_metrics(db_session):
    with patch('psutil.cpu_percent', return_value=50.0), \
         patch('psutil.virtual_memory', return_value(type('obj', (), {'percent': 60.0})())), \
         patch('psutil.disk_usage', return_value(type('obj', (), {'percent': 70.0})())):
        metric = collect_metrics(db_session)
        assert metric.cpu == 50.0
        assert metric.health_score > 0
