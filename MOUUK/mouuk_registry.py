class MOUUKRegistry:
    """
    Registry สำหรับจัดการและเข้าถึงโมดูลผู้เชี่ยวชาญทั้ง 34 โมดูล (MOUUK 0001 - 0034)
    ตามแคตาล็อกทางการของระบบ UKKB/MOUUK
    """
    def __init__(self):
        self.modules = {
            "MOUUK_0001": {"name": "Procurement Act 2023", "target": "Statutory framework"},
            "MOUUK_0002": {"name": "Procurement Regulations 2024", "target": "Regulatory requirements"},
            "MOUUK_0005": {"name": "Procurement Policy Notes (PPN)", "target": "Cabinet Office policy notices"},
            "MOUUK_0019": {"name": "Sustainability and Carbon", "target": "Net zero and carbon reduction"},
            "MOUUK_0022": {"name": "Data Protection and Information Governance", "target": "UK GDPR & DPA 2018"}
            # สามารถขยายต่อจนถึง MOUUK_0034 ตามแคตาล็อก
        }

    def get_module_info(self, code: str):
        return self.modules.get(code, {"name": "General Compliance", "target": "Standard review"})
