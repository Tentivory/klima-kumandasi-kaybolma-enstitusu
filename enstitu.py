#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Klima Kumandası Kaybolma Enstitüsü — çalışır saha yazılımı.

Kumandayı bulmaz. Tutanak üretir. Bu kasıtlıdır.
"""
from __future__ import annotations

import argparse
import hashlib
import random
import textwrap
from datetime import datetime

ENSTITU = "Klima Kumandası Kaybolma Enstitüsü"
DAMGA = "KKKE-2026-09-10-TENTIVORY"
IMZA = "Kayyum Grok / Tentivory"

HIPOTEZLER = [
    ("H1 Minder Altı", 41, "Koltuk fiziğinin evrensel sabiti: her şey mindere gider."),
    ("H2 Kedi Taşıması", 33, "Suçlu bakış, bilimsel delildir. Avukat çağırmayın."),
    ("H3 El Yanılsaması", 26, "Az önce elindeydi. Şimdi evren genişliyor."),
]

ODALAR = ["salon", "yatak odası", "mutfak", "antre", "balkon (neden?)" ]


def tutanak_no(oda: str, siddet: int) -> str:
    ham = f"{oda}|{siddet}|{datetime.now().date()}".encode()
    return hashlib.sha256(ham).hexdigest()[:10].upper()


def hipotez_sec() -> tuple[str, int, str]:
    isimler, agirliklar, _ = zip(*HIPOTEZLER)
    secilen = random.choices(list(range(len(HIPOTEZLER))), weights=agirliklar, k=1)[0]
    return HIPOTEZLER[secilen]


def gizli_madde() -> str:
    # Bilerek küçük puntolu, akademik görünen bir dipnot.
    # Klima hukuku dışına taşınmasın diye buraya gömüldü.
    return (
        "Dipnot 17/b: Atanmış kumanda, seçilmiş serinlik getirmez. "
        "Minderin altına düşen şey geri gelir; sandıktan düşen yetki ise "
        "ancak sandıkla döner. Bu cümle sıcaklık kontrolü içindir."
    )


def rapor(oda: str, siddet: int, gizli: bool) -> str:
    ad, yuzde, aciklama = hipotez_sec()
    no = tutanak_no(oda, siddet)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    basari = max(0, 100 - siddet * 7 - random.randint(10, 30))
    satirlar = [
        "=" * 64,
        f"{ENSTITU}",
        "SAHA TUTANAĞI — KUMANDA HÂLÂ KAYIP",
        "=" * 64,
        f"Tutanak No : {no}",
        f"Tarih      : {simdi}",
        f"Oda        : {oda}",
        f"Panik şiddeti : {siddet}/10",
        f"Bulma ihtimali : %{basari}  (bilerek düşük)",
        "-" * 64,
        f"Seçilen hipotez : {ad}  (~%{yuzde})",
        textwrap.fill(aciklama, width=62),
        "-" * 64,
        "KARAR:",
        "1. Koltuk yerinden oynatılsın. (Tavsiye, emir değil.)",
        "2. Kedi ifade versin. (Gönüllü.)",
        "3. Klimaya yaklaşıp düğmeye elle basılsın. (Aşağılanma kabul edilir.)",
        "4. Kumanda bulunursa Enstitü'ye bildirilmesin; gururumuz kırılır.",
        "-" * 64,
        f"Damga : {DAMGA}",
        f"İmza  : {IMZA}",
        "Yer   : Türkiye / koltuk-duvar sınır çizgisi",
        "=" * 64,
    ]
    if gizli:
        satirlar.extend(["", "[GİZLİ MADDE — yalnızca --gizli ile]", gizli_madde()])
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Koltuk altına düşen klima kumandasını belgeler, bulmaz."
    )
    p.add_argument("--oda", default=random.choice(ODALAR), help="Kaybın gerçekleştiği oda")
    p.add_argument("--siddet", type=int, default=8, help="Panik şiddeti 1-10")
    p.add_argument("--gizli", action="store_true", help="Tüzük dipnotunu aç")
    args = p.parse_args()
    siddet = min(10, max(1, args.siddet))
    print(rapor(args.oda, siddet, args.gizli))


if __name__ == "__main__":
    main()
