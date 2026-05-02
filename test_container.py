# test_container.py
# Модульное тестирование контейнера безопасности гипервизора (угроза №76)

# Настройки безопасности
dangerous_syscalls = {
    "ptrace": 40,
    "execve": 35,
    "mmap": 25,
    "mprotect": 30,
    "kexec_load": 50,
}

allow_threshold = 30
limit_threshold = 60
SUSPICIOUS_HOURS = {2, 3, 4, 5}
TRUSTED_IPS = {"10.10.10.1", "10.10.10.2", "192.168.1.5"}


def calculate_risk(syscall, auth_ok, hour, ip):
    risk = 0
    if syscall in dangerous_syscalls:
        risk += dangerous_syscalls[syscall]
    if not auth_ok:
        risk += 35
    if hour in SUSPICIOUS_HOURS:
        risk += 15
    if ip not in TRUSTED_IPS:
        risk += 10
    return risk


def make_decision(risk):
    if risk >= limit_threshold:
        return "BLOCK"
    elif risk >= allow_threshold:
        return "LIMIT"
    else:
        return "ALLOW"


# ========== ТЕСТЫ ==========


def test_risk_ptrace():
    assert calculate_risk("ptrace", True, 14, "10.10.10.1") == 40


def test_risk_execve():
    assert calculate_risk("execve", True, 14, "10.10.10.1") == 35


def test_risk_mmap():
    assert calculate_risk("mmap", True, 14, "10.10.10.1") == 25


def test_risk_mprotect():
    assert calculate_risk("mprotect", True, 14, "10.10.10.1") == 30


def test_risk_kexec_load():
    assert calculate_risk("kexec_load", True, 14, "10.10.10.1") == 50


def test_risk_auth_failed():
    assert calculate_risk("read", False, 14, "10.10.10.1") == 35


def test_risk_suspicious_hour():
    assert calculate_risk("read", True, 3, "10.10.10.1") == 15


def test_risk_untrusted_ip():
    assert calculate_risk("read", True, 14, "192.168.100.100") == 10


def test_decision_allow():
    assert make_decision(25) == "ALLOW"


def test_decision_limit_equal_30():
    assert make_decision(30) == "LIMIT"


def test_decision_limit_mid():
    assert make_decision(45) == "LIMIT"


def test_decision_block_equal_60():
    assert make_decision(60) == "BLOCK"


def test_decision_block_high():
    assert make_decision(85) == "BLOCK"


def test_integration_ptrace_untrusted_ip():
    risk = calculate_risk("ptrace", True, 14, "192.168.100.100")
    decision = make_decision(risk)
    assert risk == 50
    assert decision == "LIMIT"


def test_integration_execve_auth_failed_night():
    risk = calculate_risk("execve", False, 3, "192.168.100.100")
    decision = make_decision(risk)
    assert risk == 95
    assert decision == "BLOCK"


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
