import os
import sys
from unittest.mock import Mock

from pytest import fixture

from app import app, db



cwd = os.getcwd()
sys.path.insert(0, cwd)


@fixture
def mock_db():
    db = Mock()
    db.session.execute.return_value = ["happy-dog-bog", "soft-slimey-tractor"]
    return db
