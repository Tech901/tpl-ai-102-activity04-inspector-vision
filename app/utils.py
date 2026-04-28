"""Validation and helper functions for the Inspector Vision pipeline.

Step 6: File validation, PII redaction, safe API calls, and JSON I/O.
"""
import json
import os
import re

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE_MB = 10


def validate_image_file(path: str) -> str:
    """Validate an image file exists, has an allowed extension, and is within size limits.

    Args:
        path: Path to the image file.

    Returns:
        The validated (cleaned) path string.

    Raises:
        ValueError: If the file does not exist, has an invalid extension,
                    or exceeds MAX_FILE_SIZE_MB.
    """
    # TODO: Step 6.1 - Implement file validation
    #   1. Check that the file exists (os.path.isfile)
    #   2. Check the extension is in ALLOWED_IMAGE_EXTENSIONS
    #   3. Check file size: os.path.getsize(path) <= MAX_FILE_SIZE_MB * 1024 * 1024
    #   4. Check for path traversal: reject paths containing ".."
    #   Raise ValueError with a descriptive message for each failure

    raise NotImplementedError("Step 6.1: Implement validate_image_file")


def validate_pdf_file(path: str) -> str:
    """Validate a PDF file exists, has the correct extension, and is within size limits.

    Args:
        path: Path to the PDF file.

    Returns:
        The validated (cleaned) path string.

    Raises:
        ValueError: If the file does not exist, is not a PDF,
                    or exceeds MAX_FILE_SIZE_MB.
    """
    # TODO: Step 6.2 - Implement PDF validation
    #   1. Check that the file exists
    #   2. Check the extension is ".pdf"
    #   3. Check file size
    #   4. Check for path traversal

    raise NotImplementedError("Step 6.2: Implement validate_pdf_file")


def redact_pii(text: str) -> str:
    """Redact phone numbers and SSN patterns from text.

    Replaces matching patterns with [REDACTED].

    Patterns matched:
        Phone: (901) 555-0147, 901-555-0147, 901.555.0147
        SSN:   123-45-6789

    Args:
        text: Input text string (e.g., OCR-extracted content).

    Returns:
        Text with PII patterns replaced by [REDACTED].
    """
    # TODO: Step 6.3 - Implement PII redaction with regex
    #   Phone pattern: r'\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}'
    #   SSN pattern:   r'\d{3}-\d{2}-\d{4}'
    #   Use re.sub() to replace each pattern with "[REDACTED]"
    #   SSN pattern (###-##-####) is more specific than phone; apply first
    #   to prevent the phone regex from partially matching SSN digits.

    raise NotImplementedError("Step 6.3: Implement redact_pii")


def safe_api_call(fn, *args, **kwargs) -> tuple:
    """Wrap an API call with error handling.

    Catches exceptions and returns a tuple of (result, error_message).
    On success, error_message is None. On failure, result is None.

    Args:
        fn: Callable to invoke.
        *args: Positional arguments for fn.
        **kwargs: Keyword arguments for fn.

    Returns:
        Tuple of (result, error_message).
        On success: (result, None)
        On failure: (None, str describing the error)
    """
    # TODO: Step 6.4 - Implement safe API call wrapper
    #   try:
    #       result = fn(*args, **kwargs)
    #       return (result, None)
    #   except Exception as e:
    #       return (None, f"{type(e).__name__}: {e}")

    raise NotImplementedError("Step 6.4: Implement safe_api_call")


# ---------------------------------------------------------------------------
# JSON I/O helpers (provided -- not TODO)
# ---------------------------------------------------------------------------

def write_json(filepath: str, data) -> None:
    """Write data to a JSON file with pretty-printing.

    Args:
        filepath: Output file path.
        data: JSON-serializable data (dict or list).
    """
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_json(filepath: str):
    """Load and parse a JSON file.

    Args:
        filepath: Path to the JSON file.

    Returns:
        Parsed JSON data (dict or list).
    """
    with open(filepath) as f:
        return json.load(f)
