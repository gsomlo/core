from typing import Any

from core import utils
from core.config import Configuration
from core.services.base import CoreService, ServiceMode

GROUP: str = "ProtoSvc"


class MgenSinkService(CoreService):
    name: str = "MGEN_Sink"
    group: str = GROUP
    directories: list[str] = []
    files: list[str] = ["mgensink.sh", "sink.mgen"]
    executables: list[str] = ["mgen"]
    dependencies: list[str] = []
    startup: list[str] = ["bash mgensink.sh"]
    validate: list[str] = ["pidof mgen"]
    shutdown: list[str] = ["killall mgen"]
    validation_mode: ServiceMode = ServiceMode.BLOCKING
    default_configs: list[Configuration] = []
    modes: dict[str, dict[str, str]] = {}

    def data(self) -> dict[str, Any]:
        ifnames = []
        for iface in self.node.get_ifaces():
            name = utils.sysctl_devname(iface.name)
            ifnames.append(name)
        return dict(ifnames=ifnames)


class NrlNhdp(CoreService):
    name: str = "NHDP"
    group: str = GROUP
    directories: list[str] = []
    files: list[str] = ["nrlnhdp.sh"]
    executables: list[str] = ["nrlnhdp"]
    dependencies: list[str] = []
    startup: list[str] = ["bash nrlnhdp.sh"]
    validate: list[str] = ["pidof nrlnhdp"]
    shutdown: list[str] = ["killall nrlnhdp"]
    validation_mode: ServiceMode = ServiceMode.BLOCKING
    default_configs: list[Configuration] = []
    modes: dict[str, dict[str, str]] = {}

    def data(self) -> dict[str, Any]:
        has_smf = "SMF" in self.node.services
        ifnames = []
        for iface in self.node.get_ifaces(control=False):
            ifnames.append(iface.name)
        return dict(has_smf=has_smf, ifnames=ifnames)


class NrlSmf(CoreService):
    name: str = "SMF"
    group: str = GROUP
    directories: list[str] = []
    files: list[str] = ["startsmf.sh"]
    executables: list[str] = ["nrlsmf", "killall"]
    dependencies: list[str] = []
    startup: list[str] = ["bash startsmf.sh"]
    validate: list[str] = ["pidof nrlsmf"]
    shutdown: list[str] = ["killall nrlsmf"]
    validation_mode: ServiceMode = ServiceMode.BLOCKING
    default_configs: list[Configuration] = []
    modes: dict[str, dict[str, str]] = {}

    def data(self) -> dict[str, Any]:
        has_nhdp = "NHDP" in self.node.services
        has_olsr = "OLSR" in self.node.services
        ifnames = []
        ip4_prefix = None
        for iface in self.node.get_ifaces(control=False):
            ifnames.append(iface.name)
            ip4 = iface.get_ip4()
            if ip4:
                ip4_prefix = f"{ip4.ip}/{24}"
                break
        return dict(
            has_nhdp=has_nhdp, has_olsr=has_olsr, ifnames=ifnames, ip4_prefix=ip4_prefix
        )


class NrlOlsr(CoreService):
    name: str = "OLSR"
    group: str = GROUP
    directories: list[str] = []
    files: list[str] = ["nrlolsrd.sh"]
    executables: list[str] = ["nrlolsrd"]
    dependencies: list[str] = []
    startup: list[str] = ["bash nrlolsrd.sh"]
    validate: list[str] = ["pidof nrlolsrd"]
    shutdown: list[str] = ["killall nrlolsrd"]
    validation_mode: ServiceMode = ServiceMode.BLOCKING
    default_configs: list[Configuration] = []
    modes: dict[str, dict[str, str]] = {}

    def data(self) -> dict[str, Any]:
        has_smf = "SMF" in self.node.services
        has_zebra = "zebra" in self.node.services
        ifname = None
        for iface in self.node.get_ifaces(control=False):
            ifname = iface.name
            break
        return dict(has_smf=has_smf, has_zebra=has_zebra, ifname=ifname)


class NrlOlsrv2(CoreService):
    name: str = "OLSRv2"
    group: str = GROUP
    directories: list[str] = []
    files: list[str] = ["nrlolsrv2.sh"]
    executables: list[str] = ["nrlolsrv2"]
    dependencies: list[str] = []
    startup: list[str] = ["bash nrlolsrv2.sh"]
    validate: list[str] = ["pidof nrlolsrv2"]
    shutdown: list[str] = ["killall nrlolsrv2"]
    validation_mode: ServiceMode = ServiceMode.BLOCKING
    default_configs: list[Configuration] = []
    modes: dict[str, dict[str, str]] = {}

    def data(self) -> dict[str, Any]:
        has_smf = "SMF" in self.node.services
        ifnames = []
        for iface in self.node.get_ifaces(control=False):
            ifnames.append(iface.name)
        return dict(has_smf=has_smf, ifnames=ifnames)


class OlsrOrg(CoreService):
    name: str = "OLSRORG"
    group: str = GROUP
    directories: list[str] = ["/etc/olsrd"]
    files: list[str] = ["olsrd.sh", "/etc/olsrd/olsrd.conf"]
    executables: list[str] = ["olsrd"]
    dependencies: list[str] = []
    startup: list[str] = ["bash olsrd.sh"]
    validate: list[str] = ["pidof olsrd"]
    shutdown: list[str] = ["killall olsrd"]
    validation_mode: ServiceMode = ServiceMode.BLOCKING
    default_configs: list[Configuration] = []
    modes: dict[str, dict[str, str]] = {}

    def data(self) -> dict[str, Any]:
        has_smf = "SMF" in self.node.services
        ifnames = []
        for iface in self.node.get_ifaces(control=False):
            ifnames.append(iface.name)
        return dict(has_smf=has_smf, ifnames=ifnames)


class MgenActor(CoreService):
    name: str = "MgenActor"
    group: str = GROUP
    directories: list[str] = []
    files: list[str] = ["start_mgen_actor.sh"]
    executables: list[str] = ["mgen"]
    dependencies: list[str] = []
    startup: list[str] = ["bash start_mgen_actor.sh"]
    validate: list[str] = ["pidof mgen"]
    shutdown: list[str] = ["killall mgen"]
    validation_mode: ServiceMode = ServiceMode.BLOCKING
    default_configs: list[Configuration] = []
    modes: dict[str, dict[str, str]] = {}
