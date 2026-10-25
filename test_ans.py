from fracshion import add, sub, mult, div
import pytest

@pytest.mark.parametrize('n1, d1, n2, d2, res,'
						[
							 (1, 1, 1, 1, (2, 1))
							(2, 1, 1, 2, (5, 2))
						 ])
def test_add(n1,d1,n2,d2, res):
	assert add(n1,d1,n2,d2)== res
#test_add()