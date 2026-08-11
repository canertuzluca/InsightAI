
"""
SQL Safety Guard

Bu modül, LLM tarafından üretilen SQL sorgularını çalıştırmadan önce
güvenlik kontrolünden geçirir.

Şimdilik yalnızca SELECT sorgularına izin veriyoruz.
"""

FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
}


def validate_sql(sql: str) -> bool:
    """
    SQL sorgusunun güvenli olup olmadığını kontrol eder.

    Kurallar:
    - Sadece SELECT sorgularına izin verilir.
    - Yasak anahtar kelimeler içeremez.
    """

    if not sql:
        return False

    normalized = sql.strip().upper()

    if not normalized.startswith("SELECT"):
        return False

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in normalized:
            return False

    return True
