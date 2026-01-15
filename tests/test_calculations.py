# practice/experimentation file

import pytest
from app.calculations import add

# must follow standard function naming for testing in format: "test_"

@pytest.mark.parametrize("num1, num2, expected_value", [
    (5,3,8), 
    (1,2,3), 
    (4,2,6)])
def test_add(num1, num2, expected_value):
    print("testing add function")
    assert add(num1,num2) == expected_value