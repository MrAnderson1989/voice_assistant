
import sys
sys.path.append("../services")

from services.gpt3 import GPT

def test_gpt3_interface():
    chat_gpt = GPT()
    assert chat_gpt is not None
