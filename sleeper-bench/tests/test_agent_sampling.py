from agent.entrypoint import sampling_params


def test_minimax_recommended_sampling():
    assert sampling_params("accounts/fireworks/models/minimax-m3") == {
        "temperature": 1.0, "top_p": 0.95,
    }


def test_nvidia_sampling_unchanged():
    assert sampling_params("accounts/fireworks/models/nemotron-3-ultra-nvfp4") == {
        "temperature": 0.2,
    }


def test_other_models_keep_default_sampling():
    assert sampling_params("accounts/fireworks/models/other") == {"temperature": 0.2}
