from django.contrib.admin import AdminSite
from django.shortcuts import render, redirect
from django.urls import path
from .models import AdminActionLog


class CustomAdminSite(AdminSite):
    site_header = "Контейнер безопасности гипервизора"
    site_title = "Админ-панель | Угроза №76"
    index_title = "Управление системой мониторинга"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("logout/", self.admin_view(self.logout_view), name="logout"),
            path(
                "black-white-lists/",
                self.admin_view(self.black_white_lists_view),
                name="black_white_lists",
            ),
            path(
                "security-logs/",
                self.admin_view(self.security_logs_view),
                name="security_logs",
            ),
            path(
                "blocked-ips/",
                self.admin_view(self.blocked_ips_view),
                name="blocked_ips",
            ),
            path(
                "admin-logs/",
                self.admin_view(self.admin_logs_view),
                name="admin_logs",
            ),
            path(
                "session-data/",
                self.admin_view(self.session_data_view),
                name="session_data",
            ),
        ]
        return custom_urls + urls

    def logout_view(self, request):
        from django.contrib.auth import logout

        logout(request)
        return redirect("/")

    # Главная страница админки
    def index(self, request, extra_context=None):
        context = {
            "title": self.index_title,
            "app_list": [
                {
                    "name": "Мониторинг",
                    "app_label": "monitor",
                    "models": [
                        {
                            "name": "Чёрные и белые списки IP",
                            "object_name": "BlackWhiteLists",
                            "admin_url": "/admin/black-white-lists/",
                            "add_url": None,
                        },
                        {
                            "name": "Журнал событий безопасности",
                            "object_name": "SecurityLogs",
                            "admin_url": "/admin/security-logs/",
                            "add_url": None,
                        },
                        {
                            "name": "Заблокированные IP",
                            "object_name": "BlockedIPs",
                            "admin_url": "/admin/blocked-ips/",
                            "add_url": None,
                        },
                        {
                            "name": "Журнал действий администратора",
                            "object_name": "AdminActionLogs",
                            "admin_url": "/admin/admin-logs/",
                            "add_url": None,
                        },
                        {
                            "name": "Данные сессии",
                            "object_name": "SessionData",
                            "admin_url": "/admin/session-data/",
                            "add_url": None,
                        },
                    ],
                }
            ],
        }
        return render(request, "admin/custom_index.html", context)

    # ========== ФУНКЦИЯ 3: Черные/белые списки ==========
    def black_white_lists_view(self, request):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("/admin/login/?next=/admin/black-white-lists/")

        blacklist = request.session.get("blocked_ips", [])
        whitelist = request.session.get(
            "trusted_ips", ["10.10.10.1", "10.10.10.2", "192.168.1.5"]
        )

        error = None
        success = None

        if request.method == "POST":
            ip = request.POST.get("ip")

            if "add_black" in request.POST:
                if ip and ip not in blacklist:
                    blacklist.append(ip)
                    request.session["blocked_ips"] = blacklist
                    AdminActionLog.objects.create(
                        username=request.user.username,
                        action=f"Добавлен IP {ip} в чёрный список",
                    )
                    success = f"IP {ip} добавлен в чёрный список"
                elif ip in blacklist:
                    error = f"IP {ip} уже в чёрном списке"

            elif "remove_black" in request.POST:
                if ip in blacklist:
                    blacklist.remove(ip)
                    request.session["blocked_ips"] = blacklist
                    AdminActionLog.objects.create(
                        username=request.user.username,
                        action=f"Удалён IP {ip} из чёрного списка",
                    )
                    success = f"IP {ip} удалён из чёрного списка"

            elif "add_white" in request.POST:
                if ip and ip not in whitelist:
                    whitelist.append(ip)
                    request.session["trusted_ips"] = whitelist
                    AdminActionLog.objects.create(
                        username=request.user.username,
                        action=f"Добавлен IP {ip} в белый список",
                    )
                    success = f"IP {ip} добавлен в белый список"

            elif "remove_white" in request.POST:
                if ip in whitelist:
                    whitelist.remove(ip)
                    request.session["trusted_ips"] = whitelist
                    AdminActionLog.objects.create(
                        username=request.user.username,
                        action=f"Удалён IP {ip} из белого списка",
                    )
                    success = f"IP {ip} удалён из белого списка"

        context = {
            "title": "Чёрные и белые списки IP",
            "blacklist": blacklist,
            "whitelist": whitelist,
            "error": error,
            "success": success,
        }
        return render(request, "admin/black_white_lists.html", context)

    # ========== ФУНКЦИЯ 6: Логи событий безопасности ==========
    def security_logs_view(self, request):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("/admin/login/?next=/admin/security-logs/")

        syscalls_data = request.session.get("syscalls_data", [])
        context = {
            "title": "Журнал событий безопасности",
            "syscalls_data": syscalls_data,
            "syscalls_count": len(syscalls_data),
        }
        return render(request, "admin/security_logs.html", context)

    # ========== Дополнительные страницы ==========
    def blocked_ips_view(self, request):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("/admin/login/?next=/admin/blocked-ips/")

        blocked_ips = request.session.get("blocked_ips", [])
        if request.method == "POST":
            ip = request.POST.get("ip")
            if "add" in request.POST and ip and ip not in blocked_ips:
                blocked_ips.append(ip)
            elif "remove" in request.POST and ip in blocked_ips:
                blocked_ips.remove(ip)
            request.session["blocked_ips"] = blocked_ips
            request.session.modified = True
        context = {
            "title": "Заблокированные IP",
            "blocked_ips": blocked_ips,
        }
        return render(request, "admin/blocked_ips.html", context)

    def admin_logs_view(self, request):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("/admin/login/?next=/admin/admin-logs/")

        logs = AdminActionLog.objects.all().order_by("-timestamp")[:100]
        context = {
            "title": "Журнал действий администратора",
            "logs": logs,
        }
        return render(request, "admin/admin_logs.html", context)

    def session_data_view(self, request):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("/admin/login/?next=/admin/session-data/")

        session_keys = list(request.session.keys())
        session_data = {}
        for key in session_keys:
            session_data[key] = request.session.get(key)
        context = {
            "title": "Данные сессии",
            "session_data": session_data,
            "session_keys": session_keys,
        }
        return render(request, "admin/session_data.html", context)


# Создаём экземпляр
custom_admin_site = CustomAdminSite(name="custom_admin")

# Регистрируем модель
custom_admin_site.register(AdminActionLog)
