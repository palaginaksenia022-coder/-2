from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def index(request):
    # Настройки безопасности
    dangerous_syscalls = {
        "ptrace": 40,
        "execve": 35,
        "mmap": 25,
        "mprotect": 30,
        "kexec_load": 50,
    }
    allow_threshold = 30
    limit_threshhold = 60
    SUSPICIOUS_HOURS = {2, 3, 4, 5}
    TRUSTED_IPS = {"10.10.10.1", "10.10.10.2", "192.168.1.5"}

    # Входные данные (системные вызовы от ВМ к гипервизору)
    syscalls_data = [
        {
            "vm_id": "vm-payment-01",
            "syscall": "read",
            "user": "payment_system",
            "ip": "10.10.10.50",
            "hour": 14,
            "auth_ok": True,
        },
        {
            "vm_id": "vm-payment-01",
            "syscall": "write",
            "user": "payment_system",
            "ip": "10.10.10.50",
            "hour": 14,
            "auth_ok": True,
        },
        {
            "vm_id": "vm-db-01",
            "syscall": "read",
            "user": "db_user",
            "ip": "10.10.10.60",
            "hour": 11,
            "auth_ok": True,
        },
        {
            "vm_id": "vm-attacker",
            "syscall": "ptrace",
            "user": "unknown",
            "ip": "172.16.9.13",
            "hour": 3,
            "auth_ok": True,
        },
        {
            "vm_id": "vm-attacker",
            "syscall": "execve",
            "user": "unknown",
            "ip": "172.16.9.13",
            "hour": 3,
            "auth_ok": False,
        },
        {
            "vm_id": "vm-payment-01",
            "syscall": "mmap",
            "user": "payment_system",
            "ip": "10.10.10.50",
            "hour": 2,
            "auth_ok": True,
        },
        {
            "vm_id": "vm-db-01",
            "syscall": "kexec_load",
            "user": "db_user",
            "ip": "10.10.10.60",
            "hour": 4,
            "auth_ok": True,
        },
        {
            "vm_id": "vm-new-02",
            "syscall": "ptrace",
            "user": "attacker2",
            "ip": "10.20.30.40",
            "hour": 1,
            "auth_ok": False,
        },
        {
            "vm_id": "vm-payment-01",
            "syscall": "mprotect",
            "user": "payment_system",
            "ip": "10.10.10.50",
            "hour": 3,
            "auth_ok": False,
        },
    ]

    # Контейнер расчета
    results = []
    for syscall in syscalls_data:
        risk = 0
        if syscall["syscall"] in dangerous_syscalls:
            risk += dangerous_syscalls[syscall["syscall"]]
        if not syscall["auth_ok"]:
            risk += 35
        if syscall["hour"] in SUSPICIOUS_HOURS:
            risk += 15
        if syscall["ip"] not in TRUSTED_IPS:
            risk += 10

        if risk >= limit_threshhold:
            decision = "BLOCK"
        elif risk >= allow_threshold:
            decision = "LIMIT"
        else:
            decision = "ALLOW"

        results.append(
            {
                "vm_id": syscall["vm_id"],
                "syscall": syscall["syscall"],
                "user": syscall["user"],
                "ip": syscall["ip"],
                "hour": syscall["hour"],
                "risk": risk,
                "decision": decision,
                "auth_ok": syscall["auth_ok"],
            }
        )

    # Создание таблицы
    df = pd.DataFrame(results)

    # График 1: риск по ВМ
    vm_risk = df.groupby("vm_id")["risk"].sum()
    colors = ["red" if x >= 60 else "orange" if x >= 30 else "green" for x in vm_risk]
    plt.figure(figsize=(10, 6))
    plt.bar(vm_risk.index, vm_risk.values, color=colors)
    plt.axhline(y=60, color="red", linestyle="--", label="Блокировка (60)")
    plt.axhline(y=30, color="orange", linestyle="--", label="Предупреждение (30)")
    plt.title("Уровень риска по виртуальным машинам")
    plt.xlabel("Виртуальная машина")
    plt.ylabel("Суммарный риск")
    plt.legend()
    plt.tight_layout()

    buffer1 = BytesIO()
    plt.savefig(buffer1, format="png")
    buffer1.seek(0)
    image1_base64 = base64.b64encode(buffer1.getvalue()).decode()
    plt.close()

    # График 2: распределение решений
    decision_counts = df["decision"].value_counts()
    colors_pie = [
        "red" if d == "BLOCK" else "orange" if d == "LIMIT" else "green"
        for d in decision_counts.index
    ]
    plt.figure(figsize=(8, 8))
    plt.pie(
        decision_counts.values,
        labels=decision_counts.index,
        autopct="%1.1f%%",
        colors=colors_pie,
        shadow=True,
    )
    plt.title("Распределение решений контейнера безопасности")
    plt.tight_layout()

    buffer2 = BytesIO()
    plt.savefig(buffer2, format="png")
    buffer2.seek(0)
    image2_base64 = base64.b64encode(buffer2.getvalue()).decode()
    plt.close()

    # График 3: опасные вызовы
    dangerous_df = df[df["syscall"].isin(dangerous_syscalls.keys())]
    if not dangerous_df.empty:
        syscall_counts = dangerous_df["syscall"].value_counts()
        plt.figure(figsize=(10, 6))
        plt.bar(syscall_counts.index, syscall_counts.values, color="red")
        plt.title("Обнаруженные опасные системные вызовы")
        plt.xlabel("Системный вызов")
        plt.ylabel("Количество")
        plt.tight_layout()

        buffer3 = BytesIO()
        plt.savefig(buffer3, format="png")
        buffer3.seek(0)
        image3_base64 = base64.b64encode(buffer3.getvalue()).decode()
        plt.close()
    else:
        image3_base64 = None

    # Статистика
    stats = {
        "total": len(df),
        "allow": len(df[df["decision"] == "ALLOW"]),
        "limit": len(df[df["decision"] == "LIMIT"]),
        "block": len(df[df["decision"] == "BLOCK"]),
    }

    # Таблица в HTML
    table_html = df.to_html(classes="table table-striped", index=False)

    context = {
        "stats": stats,
        "table_html": table_html,
        "image1_base64": image1_base64,
        "image2_base64": image2_base64,
        "image3_base64": image3_base64,
    }

    return render(request, "monitor/index.html", context)
