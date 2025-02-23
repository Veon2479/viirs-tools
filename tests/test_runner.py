import pytest

from viirs_tools.runner import AlgsCloud, AlgsIndex, AlgsLST, AlgsNight, AlgsUtils, AlgsWater, Runner


class TestRunner:
    @pytest.mark.parametrize(
        "algs",
        [
            AlgsCloud,
            AlgsIndex,
            AlgsLST,
            AlgsNight,
            AlgsWater,
            AlgsUtils,
        ],
    )
    def test_integrity(self, algs):
        runner = Runner()
        impls = runner._IMPLS[algs]
        for alg in algs:
            assert alg in impls
        assert len(algs) == len(impls)
