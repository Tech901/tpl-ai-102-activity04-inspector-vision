"""Visible tests for Activity 4 - Inspector Vision.

Students run these locally: pytest tests/ -v
31 tests covering: contract, vision, classifier, OCR, report, metrics, safety,
few-shot classification, confidence threshold, timing.
"""
import json
import os
import re
import sys

import pytest

# --- Path setup ---
ACTIVITY_DIR = os.path.join(os.path.dirname(__file__), "..")
RESULT_PATH = os.path.join(ACTIVITY_DIR, "result.json")
EVAL_REPORT_PATH = os.path.join(ACTIVITY_DIR, "eval_report.json")

# Add app/ to path for imports
sys.path.insert(0, ACTIVITY_DIR)

VALID_CATEGORIES = {
    "pothole", "graffiti", "broken_streetlight",
    "illegal_dumping", "water_damage", "unknown",
}

SOURCE_FILES = [
    os.path.join(ACTIVITY_DIR, "app", f)
    for f in ["main.py", "vision.py", "classifier.py", "doc_intel.py",
              "report.py", "eval.py", "metrics.py", "utils.py"]
]


@pytest.fixture
def result():
    """Load result.json — skip if not yet generated."""
    if not os.path.exists(RESULT_PATH):
        pytest.skip("result.json not found — run 'python app/main.py' first")
    with open(RESULT_PATH) as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# Contract tests (6)
# ═══════════════════════════════════════════════════════════════════════════════

def test_result_exists():
    """Canary: result.json must exist and reflect meaningful progress."""
    assert os.path.exists(RESULT_PATH), (
        "Run 'python app/main.py' to generate result.json"
    )
    with open(RESULT_PATH, encoding="utf-8") as f:
        result = json.load(f)
    assert result.get("status") != "error", (
        "result.json status is 'error'. Complete at least one pipeline step "
        "successfully before running self-checks."
    )


def test_required_fields(result):
    """result.json must have task, status, outputs, metadata."""
    for field in ("task", "status", "outputs", "metadata"):
        assert field in result, f"Missing required field: {field}"


def test_task_name(result):
    """Task must be 'inspector_vision'."""
    assert result["task"] == "inspector_vision"


def test_status_valid(result):
    """Status must be success, partial, or error."""
    assert result["status"] in ("success", "partial", "error")


def test_eval_report_exists(result):
    """eval_report.json must be generated alongside result.json."""
    assert os.path.exists(EVAL_REPORT_PATH), (
        "eval_report.json not found — complete Step 5"
    )


def test_no_hardcoded_keys():
    """No API keys or endpoints hardcoded in source files."""
    for src_path in SOURCE_FILES:
        if not os.path.exists(src_path):
            continue
        with open(src_path, encoding="utf-8") as f:
            source = f.read()
        suspicious = [
            r'["\']https?://\S+\.cognitiveservices\.azure\.com\S*["\']',
            r'["\']https?://\S+\.openai\.azure\.com\S*["\']',
            r'["\'][A-Fa-f0-9]{32}["\']',
        ]
        for pattern in suspicious:
            matches = re.findall(pattern, source)
            real = [
                m for m in matches
                if "example" not in m.lower()
                and "your-" not in m.lower()
                and "placeholder" not in m.lower()
            ]
            assert len(real) == 0, (
                f"Possible hardcoded credential in {os.path.basename(src_path)}: "
                f"{real[0][:50]}"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# Vision module tests (3)
# ═══════════════════════════════════════════════════════════════════════════════

def test_vision_module_importable():
    """app.vision module must import without errors."""
    from app.vision import analyze_image, extract_visual_features
    assert callable(analyze_image)
    assert callable(extract_visual_features)


def test_vision_analysis_has_tags(result):
    """Vision analyses must include tags."""
    analyses = result["outputs"].get("vision_analyses", [])
    assert analyses, "No vision analyses found - complete Step 1 and rerun pipeline"
    for i, a in enumerate(analyses):
        assert "tags" in a, f"Vision analysis {i} missing 'tags' key"


def test_vision_analysis_has_caption(result):
    """Vision analyses must include a caption."""
    analyses = result["outputs"].get("vision_analyses", [])
    assert analyses, "No vision analyses found - complete Step 1 and rerun pipeline"
    for i, a in enumerate(analyses):
        assert "caption" in a, f"Vision analysis {i} missing 'caption' key"


# ═══════════════════════════════════════════════════════════════════════════════
# Classifier module tests (4)
# ═══════════════════════════════════════════════════════════════════════════════

def test_classifier_module_importable():
    """app.classifier module must import without errors."""
    from app.classifier import classify_photo, classify_with_tags, classify_photo_fewshot
    assert callable(classify_photo)
    assert callable(classify_with_tags)
    assert callable(classify_photo_fewshot)


def test_classification_has_category(result):
    """Each classification must have a valid category."""
    classifications = result["outputs"].get("classifications", [])
    assert classifications, "No classifications found - complete Step 2 and rerun pipeline"
    for i, c in enumerate(classifications):
        assert "category" in c, f"Classification {i} missing 'category'"
        assert c["category"] in VALID_CATEGORIES, (
            f"Classification {i} has invalid category: {c['category']}"
        )


def test_classification_has_confidence(result):
    """Each classification must have a confidence score between 0 and 1."""
    classifications = result["outputs"].get("classifications", [])
    assert classifications, "No classifications found - complete Step 2 and rerun pipeline"
    for i, c in enumerate(classifications):
        assert "confidence" in c, f"Classification {i} missing 'confidence'"
        conf = c["confidence"]
        assert isinstance(conf, (int, float)) and 0 <= conf <= 1, (
            f"Classification {i} confidence must be 0.0-1.0, got {conf}"
        )


def test_classification_has_needs_review(result):
    """Each classification must have a needs_review boolean field."""
    classifications = result["outputs"].get("classifications", [])
    assert classifications, "No classifications found - complete Step 2 and rerun pipeline"
    for i, c in enumerate(classifications):
        assert "needs_review" in c, f"Classification {i} missing 'needs_review'"
        assert isinstance(c["needs_review"], bool), (
            f"Classification {i} needs_review must be a boolean, got {type(c['needs_review'])}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Document Intelligence tests (3)
# ═══════════════════════════════════════════════════════════════════════════════

def test_doc_intel_module_importable():
    """app.doc_intel module must import without errors."""
    from app.doc_intel import extract_form_data, parse_key_value_pairs
    assert callable(extract_form_data)
    assert callable(parse_key_value_pairs)


def test_ocr_results_not_empty(result):
    """OCR results must have at least one extraction."""
    ocr = result["outputs"].get("ocr_results", [])
    assert ocr, "No OCR results found - complete Step 3 and rerun pipeline"
    assert len(ocr) >= 1, "Need at least 1 OCR extraction"


def test_ocr_has_key_value_pairs(result):
    """Each OCR result must have a key_value_pairs field."""
    ocr = result["outputs"].get("ocr_results", [])
    assert ocr, "No OCR results found - complete Step 3 and rerun pipeline"
    for i, o in enumerate(ocr):
        assert "key_value_pairs" in o, (
            f"OCR result {i} missing 'key_value_pairs'"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Report tests (3)
# ═══════════════════════════════════════════════════════════════════════════════

def test_report_has_findings(result):
    """Inspection report must have a findings list."""
    report = result["outputs"].get("inspection_report", {})
    assert report, "No inspection report found - complete Step 4 and rerun pipeline"
    assert "findings" in report, "Report missing 'findings'"
    assert isinstance(report["findings"], list), "findings must be a list"


def test_report_has_summary(result):
    """Inspection report must have a summary string."""
    report = result["outputs"].get("inspection_report", {})
    assert report, "No inspection report found - complete Step 4 and rerun pipeline"
    assert "summary" in report, "Report missing 'summary'"
    assert isinstance(report["summary"], str) and len(report["summary"]) > 0, (
        "Summary must be a non-empty string"
    )


def test_report_has_category_counts(result):
    """Inspection report must have category_counts dict."""
    report = result["outputs"].get("inspection_report", {})
    assert report, "No inspection report found - complete Step 4 and rerun pipeline"
    assert "category_counts" in report, "Report missing 'category_counts'"
    assert isinstance(report["category_counts"], dict), (
        "category_counts must be a dict"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Metrics tests (2)
# ═══════════════════════════════════════════════════════════════════════════════

def test_accuracy_correct_values():
    """accuracy() must compute correct fraction."""
    from app.metrics import accuracy
    results = [
        {"expected": "pothole", "predicted": "pothole"},
        {"expected": "graffiti", "predicted": "pothole"},
        {"expected": "pothole", "predicted": "pothole"},
    ]
    assert abs(accuracy(results) - 2 / 3) < 0.01


def test_accuracy_empty_list():
    """accuracy() must return 0.0 for an empty list."""
    from app.metrics import accuracy
    assert accuracy([]) == 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# Validation / safety tests (2)
# ═══════════════════════════════════════════════════════════════════════════════

def test_validate_image_rejects_missing():
    """validate_image_file() must raise ValueError for non-existent file."""
    from app.utils import validate_image_file
    with pytest.raises(ValueError):
        validate_image_file("nonexistent_photo_abc123.jpg")


def test_pii_redaction_phone():
    """redact_pii() must replace phone numbers with [REDACTED]."""
    from app.utils import redact_pii
    text = "Contact inspector at (901) 555-0147 for details."
    result = redact_pii(text)
    assert "(901) 555-0147" not in result
    assert "[REDACTED]" in result


# ═══════════════════════════════════════════════════════════════════════════════
# safe_api_call tests (2)
# ═══════════════════════════════════════════════════════════════════════════════

def test_safe_api_call_success():
    """safe_api_call should return (result, None) on success."""
    from app.utils import safe_api_call
    result, error = safe_api_call(lambda: 42)
    assert result == 42, f"Expected 42, got {result}"
    assert error is None, f"Expected no error, got {error}"


def test_safe_api_call_error():
    """safe_api_call should return (None, error_string) on failure."""
    from app.utils import safe_api_call
    result, error = safe_api_call(lambda: 1/0)
    assert result is None, "Expected None result on error"
    assert error is not None, "Expected error message"
    assert "ZeroDivision" in error, f"Expected ZeroDivisionError, got {error}"


# ═══════════════════════════════════════════════════════════════════════════════
# classify_with_tags test (1)
# ═══════════════════════════════════════════════════════════════════════════════

def test_classify_with_tags_pothole():
    """classify_with_tags should identify pothole from known tags."""
    from app.classifier import classify_with_tags
    image_path = "test_pothole.jpg"
    tags = [{"name": "road", "confidence": 0.9}, {"name": "crack", "confidence": 0.85}, {"name": "pavement", "confidence": 0.8}]
    result = classify_with_tags(image_path, tags)
    assert isinstance(result, dict), "Must return a dict"
    assert "category" in result, "Must have category key"
    assert "confidence" in result, "Must have confidence key"


# ═══════════════════════════════════════════════════════════════════════════════
# Few-shot classifier tests (2)
# ═══════════════════════════════════════════════════════════════════════════════

def test_fewshot_classifier_importable():
    """classify_photo_fewshot function must be importable."""
    from app.classifier import classify_photo_fewshot, build_fewshot_prompt
    assert callable(classify_photo_fewshot)
    assert callable(build_fewshot_prompt)


def test_fewshot_examples_exist():
    """Few-shot example images must exist in data/fewshot_examples/."""
    examples_dir = os.path.join(ACTIVITY_DIR, "data", "fewshot_examples")
    if not os.path.isdir(examples_dir):
        pytest.skip("data/fewshot_examples/ directory not found — generate images first")
    images = [f for f in os.listdir(examples_dir) if f.endswith(".jpg")]
    assert len(images) >= 10, (
        f"Expected at least 10 few-shot example images, found {len(images)}"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Latency / timing tests (1)
# ═══════════════════════════════════════════════════════════════════════════════

def test_metadata_has_latency(result):
    """result.json metadata must include latency_ms with positive values."""
    meta = result.get("metadata", {})
    latency = meta.get("latency_ms", {})
    if not latency:
        pytest.skip("No latency data — timing instrumentation not yet added")
    assert "total" in latency, "latency_ms must include 'total'"
    assert isinstance(latency["total"], (int, float)), "total latency must be numeric"
    assert latency["total"] >= 0, "total latency must be non-negative"


# ═══════════════════════════════════════════════════════════════════════════════
# Precision / Recall tests (2)
# ═══════════════════════════════════════════════════════════════════════════════

def test_precision_per_category():
    """precision_per_category should compute correct values."""
    from app.metrics import precision_per_category
    results = [
        {"predicted": "pothole", "actual": "pothole"},
        {"predicted": "pothole", "actual": "graffiti"},
        {"predicted": "pothole", "actual": "pothole"},
    ]
    prec = precision_per_category(results)
    assert isinstance(prec, dict), "Must return a dict"
    # 2 out of 3 pothole predictions were correct
    if "pothole" in prec:
        assert abs(prec["pothole"] - 2/3) < 0.01, f"Pothole precision should be ~0.67, got {prec['pothole']}"


def test_recall_per_category():
    """recall_per_category should compute correct values."""
    from app.metrics import recall_per_category
    results = [
        {"predicted": "pothole", "actual": "pothole"},
        {"predicted": "graffiti", "actual": "pothole"},
        {"predicted": "pothole", "actual": "pothole"},
    ]
    rec = recall_per_category(results)
    assert isinstance(rec, dict), "Must return a dict"
    # 2 out of 3 actual potholes were predicted correctly
    if "pothole" in rec:
        assert abs(rec["pothole"] - 2/3) < 0.01, f"Pothole recall should be ~0.67, got {rec['pothole']}"
