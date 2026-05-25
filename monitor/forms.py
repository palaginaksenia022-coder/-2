from django import forms


class SyscallForm(forms.Form):
    vm_id = forms.CharField(label="VM ID", max_length=50, initial="vm-new")
    syscall = forms.ChoiceField(
        label="Системный вызов",
        choices=[
            ("read", "read"),
            ("write", "write"),
            ("ptrace", "ptrace"),
            ("execve", "execve"),
            ("mmap", "mmap"),
            ("mprotect", "mprotect"),
            ("kexec_load", "kexec_load"),
        ],
    )
    user = forms.CharField(label="Пользователь", max_length=50, initial="user")
    ip = forms.CharField(label="IP-адрес", max_length=50, initial="10.10.10.100")
    hour = forms.IntegerField(label="Час (0-23)", min_value=0, max_value=23, initial=12)
    auth_ok = forms.BooleanField(
        label="Аутентификация успешна", required=False, initial=True
    )
