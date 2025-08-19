import re
from typing import Dict, List, Optional


def _extract_title(text: str) -> Optional[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for i, line in enumerate(lines[:20]):
        if re.search(r"\bH\s*Ợ\s*P\s*\s*Đ\s*Ồ\s*N\s*G\b|HOP DONG|HỢP ĐỒNG", line, flags=re.IGNORECASE):
            return line
    return None


def _detect_type(text: str) -> Dict[str, Optional[str]]:
    candidates = [l.upper() for l in text.splitlines()[:60] if l.strip()]
    head = "\n".join(candidates)
    patterns = [
        ("mua_ban", "MUA\s*BÁN|MUA BAN"),
        ("lao_dong", "LAO\s*ĐỘNG|LAO DONG"),
        ("dich_vu", "DỊCH\s*VỤ|DICH VU"),
        ("thue", "THUÊ|THUE|CHO\s*THUÊ|CHO THUE"),
        ("hop_tac", "HỢP\s*TÁC|HOP TAC|LIÊN\s*KẾT|LIEN KET"),
        ("bao_mat", "BẢO\s*MẬT|BAO MAT|NDA|NON-DISCLOSURE"),
        ("nguyen_tac", "NGUYÊN\s*TẮC|NGUYEN TAC|KHUNG HỢP ĐỒNG|KHUNG HOP DONG"),
    ]
    for slug, pat in patterns:
        if re.search(pat, head, flags=re.IGNORECASE):
            return {"type": slug, "type_label": slug.replace("_", " ").title()}
    return {"type": "khac", "type_label": "Khác"}


def _extract_parties(text: str) -> Dict[str, str]:
    parties = {}
    patterns = [
        ("ben_a", r"B\s*Ê\s*N\s*A\b|Bên\s*A\b|Ben\s*A\b", 200),
        ("ben_b", r"B\s*Ê\s*N\s*B\b|Bên\s*B\b|Ben\s*B\b", 200),
        ("ben_mua", r"Bên\s*Mua\b|Ben\s*Mua\b", 200),
        ("ben_ban", r"Bên\s*Bán\b|Ben\s*Ban\b", 200),
    ]
    for key, pat, window in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            start = m.start()
            snippet = text[start:start + 1000]
            block = snippet.split("\n\n")[0]
            parties[key] = block.strip()
    return parties


def _extract_effective_date(text: str) -> Optional[str]:
    m = re.search(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", text, flags=re.IGNORECASE)
    if m:
        return m.group(0)
    m = re.search(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b", text)
    if m:
        return m.group(1)
    return None


def _extract_amount(text: str) -> Optional[str]:
    lines = text.splitlines()
    for line in lines:
        if re.search(r"Giá\s*trị\s*hợp\s*đồng|Tổng\s*giá\s*trị", line, flags=re.IGNORECASE):
            m = re.search(r"([0-9]{1,3}(?:[\.,][0-9]{3})*(?:[\.,][0-9]+)?)(\s*(VNĐ|VND|đ|đồng))?", line)
            if m:
                return m.group(0)
    candidates = re.findall(r"[0-9]{1,3}(?:[\.,][0-9]{3})+(?:[\.,][0-9]+)?\s*(?:VNĐ|VND|đ|đồng)?", text)
    if candidates:
        return sorted(candidates, key=lambda s: len(re.sub(r"\D", "", s)), reverse=True)[0]
    return None


def _extract_clauses(text: str) -> List[str]:
    clause_heads = re.findall(r"(Điều\s+\d+[^\n]*)", text, flags=re.IGNORECASE)
    return clause_heads[:50]


def _extract_signatures(text: str) -> Dict[str, bool]:
    sign = r"(Đại\s*diện|Dai\s*dien|Ký\s*tên|Ky\s*ten|Chữ\s*ký|Chu\s*ky|Đóng\s*dấu|Dong\s*dau)"
    ben_a = r"(BÊN\s*A|Bên\s*A|Ben\s*A)"
    ben_b = r"(BÊN\s*B|Bên\s*B|Ben\s*B)"
    window = 120
    pat_a = rf"({sign}).{{0,{window}}}{ben_a}|{ben_a}.{{0,{window}}}({sign})"
    pat_b = rf"({sign}).{{0,{window}}}{ben_b}|{ben_b}.{{0,{window}}}({sign})"
    return {
        "ben_a_present": bool(re.search(pat_a, text, flags=re.IGNORECASE | re.DOTALL)),
        "ben_b_present": bool(re.search(pat_b, text, flags=re.IGNORECASE | re.DOTALL)),
        "chu_ky_mention": bool(re.search(sign, text, flags=re.IGNORECASE)),
    }


def parse_contract_text(text: str) -> Dict:
    detected_type = _detect_type(text)
    return {
        "title": _extract_title(text),
        "type": detected_type.get("type"),
        "type_label": detected_type.get("type_label"),
        "parties": _extract_parties(text),
        "effective_date": _extract_effective_date(text),
        "amount": _extract_amount(text),
        "clauses": _extract_clauses(text),
        "signatures": _extract_signatures(text),
    } 