
import sys
sys.path.append("../services")

from services.tencent import TencentASR

def test_tencent_asr():
    tencent_asr = TencentASR()
    assert tencent_asr is not None
