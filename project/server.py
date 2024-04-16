import logging
from contextlib import asynccontextmanager

import project.validate_email_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="aarushi-email-validation-api-2",
    lifespan=lifespan,
    description="The task involves developing an endpoint that takes an email address as input and performs several validation checks to determine its legitimacy and validity. The validation process consists of the following steps:\n\n1. **Verifying the Format and Syntax:** The endpoint will utilize Python's regular expression (re) module to ensure the email follows a standard format, such as 'example@domain.com'. A pattern will be defined to match valid email structures.\n\n2. **Checking Domain Existence and MX Records:** The `dns.resolver` module from the `dnspython` package will be employed to query the domain of the email address for MX records. This confirms if the domain is active and set up to receive emails.\n\n3. **Detecting Disposable Email Addresses:** The system will integrate functionality to identify disposable or temporary email addresses through the use of libraries like `validate_email_address` or manually curated lists of known disposable domains. This step helps in filtering out emails that are often used for spam or fraudulent activities.\n\n4. **Identifying Role-Based Email Addresses:** A list of common role-based keywords (e.g., 'info', 'support', 'admin') will be utilized to detect if the email address is associated with a generic role rather than an individual. This is important as role-based emails may not be suitable for personal user accounts due to their shared nature.\n\n5. **Return of Validation Results:** Finally, the endpoint will return a comprehensive validation result, indicating whether the email is valid, and if not, specifying the issues detected (e.g., invalid format, nonexistent domain, disposable email, role-based address).\n\nThis system ensures a high level of integrity in user data by verifying email addresses thoroughly before acceptance, enhancing security, and engagement by preventing spam and ensuring communications reach intended recipients.",
)


@app.post(
    "/validate/email",
    response_model=project.validate_email_service.ValidateEmailResponse,
)
async def api_post_validate_email(
    email: str,
) -> project.validate_email_service.ValidateEmailResponse | Response:
    """
    Receives an email address and performs a series of validation checks, returning a detailed report.
    """
    try:
        res = project.validate_email_service.validate_email(email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
