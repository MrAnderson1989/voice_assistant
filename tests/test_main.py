
import sys
sys.path.append("..")

from main import Jarvis

def test_jarvis():
    jarvis = Jarvis()
    assert jarvis is not None
