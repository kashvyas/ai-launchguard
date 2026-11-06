from src.ai_launchguard.agent import LaunchGuard


def test_clean_release_ships():
    r = LaunchGuard().assess("campaign-copilot-v17", 100)
    assert r.decision == "SHIP"
    assert r.rollout_pct == 100


def test_conditional_rai_caps_rollout():
    r = LaunchGuard().assess("cx-agent-v9", 100)
    assert r.decision == "LIMITED_ROLLOUT"
    assert r.rollout_pct == 10


def test_quality_failure_holds():
    r = LaunchGuard().assess("internal-dev-agent-v3", 25)
    assert r.decision == "HOLD"
    assert "task_success" in r.failed_gates
    assert "rollback_readiness" in r.failed_gates
