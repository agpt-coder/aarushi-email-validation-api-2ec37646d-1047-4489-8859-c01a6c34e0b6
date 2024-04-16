from typing import List

from dns.exception import DNSException
from dns.resolver import resolve
from email_validator import EmailNotValidError
from email_validator import validate_email as ve
from pydantic import BaseModel


class ValidateEmailResponse(BaseModel):
    """
    A detailed report indicating the validity of the email address, with specific checks and their outcomes.
    """

    isValid: bool
    isValidSyntax: bool
    hasValidDomainAndMX: bool
    isDisposable: bool
    isRoleBased: bool
    detectedIssues: List[str]


def validate_email(email: str) -> ValidateEmailResponse:
    """
    Receives an email address and performs a series of validation checks, returning a detailed report.

    Args:
        email (str): The email address to be validated.

    Returns:
        ValidateEmailResponse: A detailed report indicating the validity of the email address, with specific checks and their outcomes.
    """
    response = ValidateEmailResponse(
        isValid=False,
        isValidSyntax=False,
        hasValidDomainAndMX=False,
        isDisposable=False,
        isRoleBased=False,
        detectedIssues=[],
    )
    try:
        v = ve(email)
        response.isValidSyntax = True
    except EmailNotValidError as e:
        response.detectedIssues.append(f"Invalid syntax: {str(e)}")
        return response
    domain = email.split("@")[1]
    try:
        answers = resolve(domain, "MX")
        if answers:
            response.hasValidDomainAndMX = True
    except DNSException:
        response.detectedIssues.append("Domain does not exist or no MX records found.")
    response.isDisposable = False
    role_based_keywords = ["info", "support", "admin"]
    local_part = email.split("@")[0]
    if any((keyword in local_part for keyword in role_based_keywords)):
        response.isRoleBased = True
        response.detectedIssues.append("Email is role-based.")
    response.isValid = (
        response.isValidSyntax
        and response.hasValidDomainAndMX
        and (not response.isDisposable)
        and (not response.isRoleBased)
    )
    if response.isValid:
        response.detectedIssues.clear()
    return response
