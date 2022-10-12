from src.limiter import Limit
from hypothesis import given
from hypothesis.strategies import integers

class TestInit:
    def test_init(self):
        limiter = Limit(max_calls=1,period=2)
        assert isinstance(limiter, Limit)

    @given(integers(min_value=1, max_value=100), integers(min_value=1))
    def test_correct_fields(self, i, j):
        limiter = Limit(max_calls=i, period=j)

        assert limiter.max_calls == i
        assert limiter.period == j
        assert len(limiter._times_released) == i
        assert limiter._current_available == i
