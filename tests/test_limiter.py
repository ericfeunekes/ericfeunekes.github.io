from src.limiter import Limit
from hypothesis import given
from hypothesis.strategies import integers
class TestInit:
    @given(integers())