from a2a.types import AgentSkill

check_electric_bill = AgentSkill(
    id="check_electric_bill",
    name="Check Electric Bill",
    description="Send the electric utility code, month, and year to check the bill.",
    tags=["electric", "utility", "bill"],
    examples=["Check the bill for electric code E001 for January 2024"],
)

support_customer_issue = AgentSkill(
    id="support_customer_issue",
    name="Support Customer Issue",
    description="Explain the issue to the electric utility and get a response.",
    tags=["electric", "utility", "support"],
    examples=["I have an issue with my electric service at 123 Main St."],
)