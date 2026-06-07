# -*- coding: utf-8 -*-
# Домашнее задание №13
# Технико-экономическое обоснование проекта
# Программное средство: КБГ-76 (Контейнер безопасности гипервизора)
# Вариант 30

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class HardwareItem:
    name: str
    purpose: str
    quantity: float
    unit_price: float

    def total(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class SoftwareItem:
    name: str
    purpose: str
    quantity: float
    months: float
    monthly_price: float

    def total(self) -> float:
        return self.quantity * self.months * self.monthly_price


@dataclass
class ServiceItem:
    name: str
    content: str
    hours: float
    hourly_rate: float

    def total(self) -> float:
        return self.hours * self.hourly_rate


@dataclass
class PersonnelItem:
    role: str
    salary_per_month: float
    employer_charges_percent: float
    months: float
    workload: float

    def month_cost(self) -> float:
        return self.salary_per_month * (1 + self.employer_charges_percent / 100)

    def person_months(self) -> float:
        return self.months * self.workload

    def total(self) -> float:
        return self.month_cost() * self.person_months()


@dataclass
class ObjectPointItem:
    name: str
    object_type: str
    complexity: str
    weight: float
    quantity: int

    def total(self) -> float:
        return self.weight * self.quantity


@dataclass
class InvestmentOption:
    name: str
    investment_cost: float
    reduction_percent: float


def rub(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ").replace(".", ",") + " руб."


def line(title: str) -> str:
    return "\n" + "=" * 90 + f"\n{title}\n" + "=" * 90 + "\n"


def make_table(headers: List[str], rows: List[List[object]]) -> str:
    widths = [len(str(h)) for h in headers]

    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    result = []
    result.append(" | ".join(str(headers[i]).ljust(widths[i]) for i in range(len(headers))))
    result.append("-+-".join("-" * widths[i] for i in range(len(headers))))

    for row in rows:
        result.append(" | ".join(str(row[i]).ljust(widths[i]) for i in range(len(row))))

    return "\n".join(result)


def calculate_hardware() -> Dict[str, float]:
    """Аппаратные средства для КБГ-76"""
    items = [
        HardwareItem("Рабочая станция разработчика", "Разработка и документация", 1, 150000),
        HardwareItem("Серверная или виртуальная машина x86-64", "Размещение демонстрационного экземпляра", 1, 100000),
        HardwareItem("Оперативная память 32 ГБ", "Работа серверной части, мониторинга и тестов", 1, 12000),
        HardwareItem("SSD-накопитель 2 ТБ", "Хранение кода, журнала, метрик и документации", 1, 18000),
        HardwareItem("Сетевое оборудование", "Доступ к интерфейсам", 1, 20000),
        HardwareItem("Комплект рабочего места", "Работа с интерфейсом и документацией", 1, 30000),
        HardwareItem("Средства резервного хранения (NAS)", "Резервные копии материалов проекта", 1, 25000),
    ]

    total = sum(item.total() for item in items)

    rows = [
        [item.name, item.quantity, rub(item.unit_price), rub(item.total())]
        for item in items
    ]

    return {
        "total": total,
        "text": line("1. Аппаратные средства (КБГ-76)") +
        make_table(["Наименование", "Кол-во", "Цена", "Стоимость"], rows + [["Итого", "", "", rub(total)]])
    }


def calculate_software() -> Dict[str, float]:
    """Программное обеспечение для КБГ-76"""
    usd_rate = 73.3436
    docker_monthly_price = round(15 * usd_rate)

    items = [
        SoftwareItem("Linux с техническим сопровождением", "Серверная среда", 1, 5, 8000),
        SoftwareItem("Python/Django с техническим сопровождением", "Серверная часть и интерфейсы", 1, 5, 12000),
        SoftwareItem("Среда хранения журнала событий", "Журнал событий и административные решения", 1, 5, 8000),
        SoftwareItem("Prometheus и prometheus-client", "Сбор метрик качества", 1, 5, 6000),
        SoftwareItem("Средства визуализации (matplotlib, pandas)", "Графики и показатели качества", 1, 5, 5000),
        SoftwareItem("Административная панель (IP-списки, логи)", "Управление чёрными/белыми списками", 1, 5, 5000),
        SoftwareItem("Docker Team", "Контейнерная среда", 2, 5, docker_monthly_price),
        SoftwareItem("Корпоративный Git-репозиторий", "Контроль версий", 2, 5, 1000),
        SoftwareItem("Средство тестирования (pytest)", "Тестирование и анализ дефектов", 1, 5, 4000),
        SoftwareItem("Офисное ПО", "Подготовка отчёта и документации", 1, 5, 1500),
        SoftwareItem("Резервное копирование", "Хранение копий", 1, 5, 3000),
        SoftwareItem("Мониторинг доступности", "Проверка интерфейсов", 1, 5, 3000),
    ]

    total = sum(item.total() for item in items)

    rows = [
        [item.name, item.quantity, item.months, rub(item.monthly_price), rub(item.total())]
        for item in items
    ]

    return {
        "total": total,
        "docker_monthly_price": docker_monthly_price,
        "text": line("2. Программное обеспечение и программные сервисы (КБГ-76)") +
        f"Курс доллара: {usd_rate} руб.\n" +
        f"Docker Team: 15 долларов × {usd_rate} = {docker_monthly_price} руб./мес.\n\n" +
        make_table(["Наименование", "Кол-во", "Мес.", "Цена/мес.", "Стоимость"], rows + [["Итого", "", "", "", rub(total)]])
    }


def calculate_maintenance() -> Dict[str, float]:
    """Обслуживание для КБГ-76"""
    items = [
        ServiceItem("Первичная настройка серверной среды", "Сервер, сеть, Docker", 8, 1500),
        ServiceItem("Настройка пользовательского и административного контуров", "Проверка интерфейсов", 10, 1500),
        ServiceItem("Настройка журнала событий", "Хранение операций и аномалий", 8, 1500),
        ServiceItem("Настройка Prometheus-метрик", "Проверка метрик качества", 10, 1500),
        ServiceItem("Настройка визуализации", "Графики и анализ событий", 6, 1500),
        ServiceItem("Контроль зависимостей", "Python, Django, Prometheus-client", 10, 1500),
        ServiceItem("Резервное копирование", "Код, тесты, метрики, документация", 6, 1500),
        ServiceItem("Контроль интерфейсов и метрик", "Пользовательский контур, админ-панель", 8, 1500),
        ServiceItem("Проверка защищённости", "IP-списки, журналирование, аномалии", 8, 1500),
    ]

    total = sum(item.total() for item in items)

    rows = [
        [item.name, item.hours, rub(item.hourly_rate), rub(item.total())]
        for item in items
    ]

    return {
        "total": total,
        "text": line("3. Обслуживание аппаратных средств и ПО (КБГ-76)") +
        make_table(["Вид работ", "Часы", "Ставка", "Стоимость"], rows + [["Итого", "", "", rub(total)]])
    }


def calculate_training_and_trips() -> Dict[str, float]:
    """Обучение и командировки для КБГ-76"""
    training = [
        ("Обучение работе с Prometheus и метриками", 2, 1990),
        ("Обучение мониторингу и логированию", 2, 45000),
        ("Обучение DevOps-инфраструктуре", 1, 41990),
        ("Внутреннее обучение тестированию качества", 3, 12000),
        ("Внутреннее обучение администратора ИБ", 2, 10000),
        ("Подготовка к приёмочной демонстрации", 2, 6000),
    ]

    trips = [
        ("Согласование требований", 1, 2, 1500),
        ("Демонстрация промежуточной версии", 1, 2, 1500),
        ("Проверка мониторинга и метрик", 1, 2, 1500),
        ("Приёмочная демонстрация", 1, 4, 1500),
        ("Анализ замечаний и корректирующих действий", 1, 3, 1500),
    ]

    training_total = sum(count * price for _, count, price in training)
    trips_total = sum(trips_count * people * price for _, trips_count, people, price in trips)
    total = training_total + trips_total

    training_rows = [[name, count, rub(price), rub(count * price)] for name, count, price in training]
    trip_rows = [[name, trips_count, people, rub(price), rub(trips_count * people * price)] for name, trips_count, people, price in trips]

    text = line("4. Командировки и обучение (КБГ-76)")
    text += "Обучение:\n"
    text += make_table(["Направление", "Участники", "Цена", "Стоимость"], training_rows + [["Итого", "", "", rub(training_total)]])
    text += "\n\nРабочие выезды:\n"
    text += make_table(["Цель", "Выезды", "Участники", "Цена", "Стоимость"], trip_rows + [["Итого", "", "", "", rub(trips_total)]])
    text += f"\n\nОбщая сумма: {rub(total)}\n"

    return {"total": total, "training_total": training_total, "trips_total": trips_total, "text": text}


def calculate_personnel() -> Dict[str, float]:
    """Расходы на персонал для КБГ-76 (с новыми долями занятости)"""
    personnel = [
        PersonnelItem("Руководитель проекта", 190000, 30, 5, 0.30),
        PersonnelItem("Python/Django-разработчик", 230000, 30, 5, 1.00),
        PersonnelItem("Специалист по качеству", 175000, 30, 4, 0.55),
        PersonnelItem("Тестировщик", 180000, 30, 3, 0.50),
        PersonnelItem("Администратор ИБ", 165000, 30, 4, 0.30),
        PersonnelItem("DevOps-специалист", 260000, 30, 4, 0.30),
    ]

    total = sum(item.total() for item in personnel)
    person_months = sum(item.person_months() for item in personnel)
    average_pm_cost = total / person_months

    rows = [
        [
            item.role,
            rub(item.salary_per_month),
            "30%",
            item.months,
            item.workload,
            f"{item.person_months():.2f}",
            rub(item.total())
        ]
        for item in personnel
    ]

    text = line("5. Персонал (КБГ-76)")
    text += make_table(
        ["Роль", "ЗП/мес.", "Начисления", "Мес.", "Занятость", "Чел.-мес.", "Стоимость"],
        rows + [["Итого", "", "", "", "", f"{person_months:.2f}", rub(total)]]
    )
    text += f"\n\nСредняя стоимость 1 чел.-мес. = {rub(average_pm_cost)}\n"

    return {
        "total": total,
        "person_months": person_months,
        "average_pm_cost": average_pm_cost,
        "text": text
    }


def calculate_object_points() -> Dict[str, float]:
    """Объектные точки для КБГ-76"""
    items = [
        ObjectPointItem("Пользовательский интерфейс (веб-форма)", "Экранная форма", "Сложный", 3, 1),
        ObjectPointItem("Административная панель (управление IP-списками)", "Экранная форма", "Сложный", 3, 1),
        ObjectPointItem("Страница сбора метрик Prometheus", "Технический вывод", "Простой", 1, 1),
        ObjectPointItem("Журнал событий безопасности", "Отчёт / таблица", "Средний", 5, 1),
        ObjectPointItem("Список аномалий и решений (ALLOW/LIMIT/BLOCK)", "Отчёт / таблица", "Средний", 5, 1),
        ObjectPointItem("Графики визуализации (matplotlib)", "Графическое представление", "Средний", 5, 1),
        ObjectPointItem("Метрики качества (Prometheus)", "Технические показатели", "Средний", 5, 1),
        ObjectPointItem("Модуль проверки роли пользователя", "3GL-компонент", "Стандартный", 10, 1),
        ObjectPointItem("Модуль блокирования опасных вызовов", "3GL-компонент", "Стандартный", 10, 1),
        ObjectPointItem("Модуль регистрации событий", "3GL-компонент", "Стандартный", 10, 1),
        ObjectPointItem("Модуль выявления аномалий", "3GL-компонент", "Стандартный", 10, 1),
        ObjectPointItem("Модуль административной обработки", "3GL-компонент", "Стандартный", 10, 1),
        ObjectPointItem("Модуль сбора метрик и мониторинга", "3GL-компонент", "Стандартный", 10, 1),
    ]

    op = sum(item.total() for item in items)
    reuse_percent = 5  # 5% повторного использования (отличается от аналога)
    nop = op * (100 - reuse_percent) / 100
    prod = 7
    pm_op = nop / prod

    rows = [
        [item.name, item.object_type, item.complexity, item.weight, item.quantity, item.total()]
        for item in items
    ]

    text = line("6. Метод объектных точек COCOMO (КБГ-76)")
    text += make_table(["Объект", "Тип", "Сложность", "Вес", "Кол-во", "OP"], rows + [["Итого", "", "", "", "", op]])
    text += f"\n\nNOP = {op:.2f} × (100 - {reuse_percent}) / 100 = {nop:.2f}\n"
    text += f"PM_OP = {nop:.2f} / {prod} = {pm_op:.2f} чел.-мес.\n"

    return {"op": op, "nop": nop, "prod": prod, "pm_op": pm_op, "text": text}


def calculate_cocomo(nop: float, average_pm_cost: float) -> Dict[str, float]:
    """Алгоритмическая модель COCOMO для КБГ-76"""
    sloc_per_op = 40
    sloc = nop * sloc_per_op
    ksloc = sloc / 1000

    a = 2.4
    b = 1.05
    factors = {
        "RELY": 1.39,
        "CPLX": 1.15,
        "DATA": 1.00,
        "TIME": 1.00,
        "STOR": 1.00,
        "ACAP": 1.00,
        "PCAP": 1.00,
        "TOOL": 1.00,
        "SCED": 1.00,
    }

    eaf = 1
    for value in factors.values():
        eaf *= value

    pm = a * (ksloc ** b) * eaf
    development_cost = pm * average_pm_cost

    rows = [[name, value] for name, value in factors.items()]

    text = line("7. Алгоритмическая модель COCOMO (КБГ-76)")
    text += f"SLOC = {nop:.2f} × {sloc_per_op} = {sloc:.2f}\n"
    text += f"KSLOC = {ksloc:.3f}\n"
    text += f"A = {a}\n"
    text += f"B = {b}\n"
    text += make_table(["Множитель", "Значение"], rows)
    text += f"\n\nEAF = {eaf:.4f}\n"
    text += f"PM = {a} × {ksloc:.3f}^{b} × {eaf:.4f} = {pm:.2f} чел.-мес.\n"
    text += f"Стоимость разработки = {pm:.2f} × {rub(average_pm_cost)} = {rub(development_cost)}\n"

    return {
        "sloc": sloc,
        "ksloc": ksloc,
        "eaf": eaf,
        "pm": pm,
        "development_cost": development_cost,
        "text": text,
    }


def compare_models(hardware_software_total: float, training_total: float, personnel_total: float,
                   pm_op: float, average_pm_cost: float, cocomo_cost: float) -> Dict[str, float]:
    """Сравнение моделей для КБГ-76"""
    other_costs = hardware_software_total + training_total
    object_points_cost = pm_op * average_pm_cost
    analog_increase = 9000  # Разница с Zabbix (9 000 руб.)

    rows = [
        ["Прямой расчёт персонала", rub(personnel_total), rub(other_costs), rub(personnel_total + other_costs)],
        ["Метод объектных точек COCOMO", rub(object_points_cost), rub(other_costs), rub(object_points_cost + other_costs)],
        ["Алгоритмическая модель COCOMO", rub(cocomo_cost), rub(other_costs), rub(cocomo_cost + other_costs)],
        ["Расчёт на основе аналога (Zabbix)", rub(cocomo_cost + analog_increase), rub(other_costs), rub(cocomo_cost + analog_increase + other_costs)],
    ]

    total_cocomo = cocomo_cost + other_costs

    text = line("8. Сравнение моделей (КБГ-76)")
    text += make_table(["Модель", "Стоимость разработки", "Прочие затраты", "Полная стоимость"], rows)
    text += f"\n\nДля дальнейшего расчёта принимается COCOMO: {rub(total_cocomo)}\n"

    return {
        "object_points_cost": object_points_cost,
        "total_cocomo": total_cocomo,
        "text": text,
    }


def compare_investments(base_project_cost: float, cocomo_development_cost: float) -> Dict[str, float]:
    """Сравнение инвестиций для КБГ-76"""
    options = [
        InvestmentOption("Автоматизированное тестирование", 60000, 5),
        InvestmentOption("Ранняя настройка Prometheus", 45000, 4),
        InvestmentOption("Повторное использование компонентов Django", 30000, 3),
        InvestmentOption("Дополнительная подготовка участников", 80000, 4),
        InvestmentOption("Комбинированный вариант", 115000, 10),
    ]

    rows = []
    best_name = ""
    best_effect = -10**9

    for option in options:
        reduction = cocomo_development_cost * option.reduction_percent / 100
        effect = reduction - option.investment_cost
        project_after = base_project_cost - effect

        if effect > best_effect:
            best_effect = effect
            best_name = option.name
            best_project_after = project_after

        rows.append([
            option.name,
            rub(option.investment_cost),
            f"{option.reduction_percent}%",
            rub(reduction),
            rub(effect),
            rub(project_after)
        ])

    text = line("9. Сравнение инвестиций (КБГ-76)")
    text += make_table(["Вариант", "Инвестиция", "Снижение", "Снижение затрат", "Эффект", "Стоимость после"], rows)
    text += f"\n\nЛучший вариант: {best_name}\n"
    text += f"Экономический эффект: {rub(best_effect)}\n"
    text += f"Стоимость после лучшей инвестиции: {rub(best_project_after)}\n"

    return {
        "best_name": best_name,
        "best_effect": best_effect,
        "best_project_after": best_project_after,
        "text": text,
    }


def calculate_schedule(pm: float) -> Dict[str, str]:
    """Длительность, график и найм для КБГ-76"""
    months = [
        ("Февраль 2026", 2.10),
        ("Март 2026", 2.80),
        ("Апрель 2026", 3.20),
        ("Май 2026", 3.20),
        ("Июнь 2026", round(pm - 2.10 - 2.80 - 3.20 - 3.20, 2)),
    ]

    project_months = 5
    average_team = pm / project_months

    hiring = [
        ["Руководитель проекта", "Февраль 2026", "Январь 2026"],
        ["Python/Django-разработчик", "Февраль 2026", "Январь 2026"],
        ["DevOps-специалист", "Март 2026", "Февраль 2026"],
        ["Специалист по качеству", "Март 2026", "Февраль 2026"],
        ["Администратор ИБ", "Март 2026", "Февраль 2026"],
        ["Тестировщик", "Апрель 2026", "Март 2026"],
    ]

    text = line("10. Длительность, график и найм (КБГ-76)")
    text += f"Срок проекта: февраль — июнь 2026 года = {project_months} месяцев\n"
    text += f"Средняя численность команды = {pm:.2f} / {project_months} = {average_team:.2f} чел.\n\n"
    text += make_table(["Месяц", "Трудоёмкость, чел.-мес."], [[m, e] for m, e in months] + [["Итого", sum(e for _, e in months)]])
    text += "\n\n"
    text += make_table(["Роль", "Начало работы", "Начало найма"], hiring)

    return {"text": text}


def main() -> None:
    """Основная функция"""
    output = ""

    hardware = calculate_hardware()
    software = calculate_software()
    maintenance = calculate_maintenance()

    hardware_software_total = hardware["total"] + software["total"] + maintenance["total"]

    training = calculate_training_and_trips()
    personnel = calculate_personnel()
    op = calculate_object_points()
    cocomo = calculate_cocomo(op["nop"], personnel["average_pm_cost"])
    models = compare_models(
        hardware_software_total,
        training["total"],
        personnel["total"],
        op["pm_op"],
        personnel["average_pm_cost"],
        cocomo["development_cost"]
    )
    investments = compare_investments(models["total_cocomo"], cocomo["development_cost"])
    schedule = calculate_schedule(cocomo["pm"])

    output += line("АВТОМАТИЗИРОВАННЫЙ РАСЧЁТ ТЭО ПРОЕКТА КБГ-76")
    output += hardware["text"]
    output += software["text"]
    output += maintenance["text"]

    output += line("ИТОГ ПО АППАРАТНЫМ СРЕДСТВАМ И ПО")
    output += f"Саппо = {rub(hardware['total'])} + {rub(software['total'])} + {rub(maintenance['total'])} = {rub(hardware_software_total)}\n"

    output += training["text"]
    output += personnel["text"]
    output += op["text"]
    output += cocomo["text"]
    output += models["text"]
    output += investments["text"]
    output += schedule["text"]

    output += line("ИТОГОВЫЕ РЕЗУЛЬТАТЫ (КБГ-76)")
    output += f"Стоимость аппаратных средств и ПО с обслуживанием: {rub(hardware_software_total)}\n"
    output += f"Расходы на командировки и обучение: {rub(training['total'])}\n"
    output += f"Расходы на персонал: {rub(personnel['total'])}\n"
    output += f"Объектные точки OP: {op['op']:.2f}\n"
    output += f"Новые объектные точки NOP: {op['nop']:.2f}\n"
    output += f"Трудоёмкость по объектным точкам: {op['pm_op']:.2f} чел.-мес.\n"
    output += f"Трудоёмкость по COCOMO: {cocomo['pm']:.2f} чел.-мес.\n"
    output += f"Базовая стоимость проекта по COCOMO: {rub(models['total_cocomo'])}\n"
    output += f"Лучший инвестиционный вариант: {investments['best_name']}\n"
    output += f"Стоимость после лучшей инвестиции: {rub(investments['best_project_after'])}\n"
    output += "Срок проекта: февраль — июнь 2026 года\n"
    output += "Начало найма ключевых специалистов: январь 2026 года\n"

    print(output)

    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(output)

    print("\n✅ Файл result.txt успешно создан. Его можно скачать из Replit и приложить к отчёту.")


if __name__ == "__main__":
    main()