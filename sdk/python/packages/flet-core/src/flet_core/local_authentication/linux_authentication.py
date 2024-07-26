class LinuxLocalAuth:
    def __init__(self) -> None:
        import dbus

        self.dbus = dbus

        bus = dbus.SystemBus()
        proxy = bus.get_object(
            "org.freedesktop.PolicyKit1", "/org/freedesktop/PolicyKit1/Authority"
        )
        self.authority = dbus.Interface(
            proxy, dbus_interface="org.freedesktop.PolicyKit1.Authority"
        )

        system_bus_name = bus.get_unique_name()

        self.subject = ("system-bus-name", {"name": system_bus_name})
        self.action_id = "org.freedesktop.policykit.exec"
        self.details = {}
        self.flags = 1  # AllowUserInteraction flag
        self.cancellation_id = ""  # No cancellation id

    def authenticate_linux(self):
        result = self.authority.CheckAuthorization(
            self.subject, self.action_id, self.details, self.flags, self.cancellation_id
        )

        return result[0]
