import json
import mimetypes
import os
import smtplib
import sys
from pathlib import Path
from email.message import EmailMessage
from html import escape
from urllib.parse import parse_qs


BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
CONTACT_EMAIL = "office@global-consult.ro"

# Load GEO-SEO optimizations
def load_geo_optimizations():
    report_path = BASE_DIR / 'geo_seo_report.json'
    if report_path.exists():
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading geo_seo_report.json: {e}", file=sys.stderr)
    return None

GEO_DATA = load_geo_optimizations()

# SMTP settings for the contact form.
# Replace SMTP_PASSWORD with the real mailbox password before uploading to the server.
SMTP_HOST = "mail.global-consult.ro"
SMTP_PORT = 465
SMTP_USER = "office@global-consult.ro"
SMTP_PASSWORD = "_1R=}^GCOnq7j0-."
SMTP_SECURITY = "ssl"  # Use "starttls" with port 587 if your hosting provider requires it.


def _text(value):
    return value[0].strip() if value and value[0].strip() else ""


def _response(start_response, status, content_type, body, extra_headers=None):
    headers = [("Content-Type", content_type), ("Cache-Control", "no-store")]
    if extra_headers:
        headers.extend(extra_headers)
    start_response(status, headers)
    return [body]


def _is_secure(environ):
    return (
        environ.get("wsgi.url_scheme") == "https"
        or environ.get("HTTPS", "").lower() in {"on", "1", "true"}
        or environ.get("HTTP_X_FORWARDED_PROTO", "").split(",")[0].strip() == "https"
    )


def _should_force_https(environ):
    host = environ.get("HTTP_HOST", "").split(":")[0].lower()
    return host in {"global-consult.ro", "www.global-consult.ro"} and not _is_secure(environ)


def _redirect_to_https(environ, start_response):
    host = environ.get("HTTP_HOST", "global-consult.ro")
    path = environ.get("PATH_INFO", "/")
    query = environ.get("QUERY_STRING", "")
    location = f"https://{host}{path}"
    if query:
        location = f"{location}?{query}"

    status = "307 Temporary Redirect" if environ.get("REQUEST_METHOD") == "POST" else "301 Moved Permanently"
    start_response(status, [("Location", location), ("Cache-Control", "no-store")])
    return [b""]


def _page(title, message, status="200 OK"):
    html = f"""<!doctype html>
<html lang="ro">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(title)} | Global Consult</title>
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <main class="result-page">
      <section class="result-card">
        <p class="eyebrow">Global Consult</p>
        <h1>{escape(title)}</h1>
        <p>{escape(message)}</p>
        <a class="button primary" href="/#contact">Back to contact</a>
      </section>
    </main>
  </body>
</html>"""
    return status, html.encode("utf-8")


def _send_contact_email(fields):
    smtp_host = os.environ.get("SMTP_HOST", SMTP_HOST)
    smtp_port = int(os.environ.get("SMTP_PORT", str(SMTP_PORT)))
    smtp_user = os.environ.get("SMTP_USER", SMTP_USER)
    smtp_password = os.environ.get("SMTP_PASSWORD", SMTP_PASSWORD)
    smtp_security = os.environ.get("SMTP_SECURITY", SMTP_SECURITY).lower()

    if not smtp_host or not smtp_password or smtp_password.startswith("CHANGE_ME"):
        raise RuntimeError("SMTP details must be configured in passenger_wsgi.py.")

    name = fields["name"]
    email = fields["email"]
    company = fields["company"] or "Not provided"
    topic = fields["topic"] or "Not selected"
    message = fields["message"]

    body = f"""New inquiry from global-consult.ro

Name: {name}
Email: {email}
Company: {company}
Topic: {topic}

Message:
{message}
"""

    email_message = EmailMessage()
    email_message["Subject"] = f"Global Consult inquiry: {topic}"
    email_message["From"] = CONTACT_EMAIL
    email_message["To"] = CONTACT_EMAIL
    email_message["Reply-To"] = email
    email_message.set_content(body)

    if smtp_security == "ssl":
        smtp_client = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20)
    else:
        smtp_client = smtplib.SMTP(smtp_host, smtp_port, timeout=20)

    with smtp_client as smtp:
        if smtp_security == "starttls":
            smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(email_message)


def _handle_contact(environ, start_response):
    try:
        size = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        size = 0

    raw_body = environ["wsgi.input"].read(size).decode("utf-8", errors="replace")
    parsed = parse_qs(raw_body)
    fields = {
        "name": _text(parsed.get("name")),
        "email": _text(parsed.get("email")),
        "company": _text(parsed.get("company")),
        "topic": _text(parsed.get("topic")),
        "message": _text(parsed.get("message")),
    }

    if not fields["name"] or not fields["email"] or not fields["message"]:
        status, body = _page("Missing details", "Please complete your name, email, and message.", "400 Bad Request")
        return _response(start_response, status, "text/html; charset=utf-8", body)

    try:
        _send_contact_email(fields)
    except Exception as exc:
        print(f"Contact email failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        status, body = _page(
            "Message not sent",
            "The form is working, but the mail server is not configured correctly yet. Please email office@global-consult.ro directly.",
            "500 Internal Server Error",
        )
        return _response(start_response, status, "text/html; charset=utf-8", body)

    status, body = _page("Message sent", "Thank you. We received your inquiry and will reply from office@global-consult.ro.")
    return _response(start_response, status, "text/html; charset=utf-8", body)


def application(environ, start_response):
    if _should_force_https(environ):
        return _redirect_to_https(environ, start_response)

    if environ.get("REQUEST_METHOD") == "POST" and environ.get("PATH_INFO") == "/contact":
        return _handle_contact(environ, start_response)

    path = environ.get("PATH_INFO", "/").lstrip("/")
    if not path:
        path = "index.html"

    target = (PUBLIC_DIR / path).resolve()
    if not str(target).startswith(str(PUBLIC_DIR.resolve())) or not target.is_file():
        target = PUBLIC_DIR / "index.html"

    content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
    body_bytes = target.read_bytes()

    if target.name == "index.html":
        content_type = "text/html; charset=utf-8"
        html_content = body_bytes.decode('utf-8')
        
        # 1. Dynamic JSON-LD Schema Engine (Task 2.1)
        json_ld_markup = ""
        faq_html = ""

        if GEO_DATA:
            metrics = GEO_DATA.get("visibilityMetrics", {})
            brand_name = GEO_DATA.get('brandName', 'Global Consult')
            scanned_url = GEO_DATA.get('scannedUrl', 'https://global-consult.ro/')
            
            json_ld_markup = f"""
    <!-- Automated JSON-LD Injection -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "{brand_name}",
      "url": "{scanned_url}",
      "description": "Optimized presence with a GEO Score of {metrics.get('geoScore', 0)}%"
    }}
    </script>
    <!-- End Automated JSON-LD Injection -->"""

            faq_items = GEO_DATA.get("targetQueriesToOptimize", [])
            if faq_items:
                faq_html = "<section id='faq' style='padding: 4rem 2rem; max-width: 800px; margin: 0 auto;'><h2>Întrebări Frecvente</h2><div class='faq-container'>"
                for item in faq_items:
                    faq_html += f"""
                    <div class="faq-item" style="margin-bottom: 1.5rem;" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
                        <strong itemprop="name">Q: {item.get('query')}</strong>
                        <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
                            <p itemprop="text" style="margin-top: 0.5rem; color: #4a5568;">A: {item.get('recommendation')}</p>
                        </div>
                    </div>
                    """
                faq_html += "</div></section>"
        
        # Inject into HTML
        if "<!-- GEO_JSON_LD_PLACEHOLDER -->" in html_content:
            html_content = html_content.replace("<!-- GEO_JSON_LD_PLACEHOLDER -->", json_ld_markup)
        
        if "<!-- GEO_FAQ_PLACEHOLDER -->" in html_content:
            html_content = html_content.replace("<!-- GEO_FAQ_PLACEHOLDER -->", faq_html)
            
        body_bytes = html_content.encode('utf-8')

    elif target.suffix == ".css":
        content_type = "text/css; charset=utf-8"
    elif target.suffix == ".js":
        content_type = "application/javascript; charset=utf-8"

    return _response(start_response, "200 OK", content_type, body_bytes)
