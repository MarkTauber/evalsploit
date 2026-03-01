# File operation modules; imported from cli to register.

from evalsploit.modules.file.ls_mod import LsModule
from evalsploit.modules.file.cat_mod import CatModule
from evalsploit.modules.file.copy_mod import CopyModule
from evalsploit.modules.file.rm_mod import RmModule
from evalsploit.modules.file.dl_mod import DlModule
from evalsploit.modules.file.mkd_mod import MkdModule
from evalsploit.modules.file.mkf_mod import MkfModule
from evalsploit.modules.file.touch_mod import TouchModule
from evalsploit.modules.file.stat_mod import StatModule
from evalsploit.modules.file.ren_mod import RenModule
from evalsploit.modules.file.upl_mod import UplModule
from evalsploit.modules.file.edit_mod import EditModule

__all__ = [
    "LsModule", "CatModule", "CopyModule", "RmModule", "DlModule",
    "MkdModule", "MkfModule", "TouchModule", "StatModule", "RenModule",
    "UplModule", "EditModule",
]
