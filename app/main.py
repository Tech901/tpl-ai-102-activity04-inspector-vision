"""
Activity 4 - Inspector Vision
AI-102: Azure AI Vision + GPT-4o Multimodal + Document Intelligence

Memphis 311 facilities inspectors photograph violations and fill out forms.
Your task is to build an AI-powered inspection pipeline that:
  1. Analyzes inspection photos with Azure AI Vision (tags, objects, captions)
  2. Classifies violation types with GPT-4o multimodal prompts
  3. Extracts text from inspection forms with Document Intelligence (OCR)
  4. Combines everything into a structured inspection report
  5. Evaluates three classification approaches (tag heuristic vs zero-shot
     GPT-4o vs few-shot GPT-4o) with cost analysis
  6. Validates inputs and redacts PII from OCR output

Categories: pothole, graffiti, broken_streetlight, illegal_dumping, water_damage

Output: result.json + eval_report.json
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

from dotenv import load_dotenv

# Support running as either `python -m app.main` or `python app/main.py`.
if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import CONFIDENCE_THRESHOLD, VALID_CATEGORIES

load_dotenv(override=True)


def _get_sdk_version() -> str:
    """Return the azure-ai-vision-imageanalysis SDK version."""
    try:
        from importlib.metadata import version

        return version("azure-ai-vision-imageanalysis")
    except Exception:
        return "unknown"


# ═══════════════════════════════════════════════════════════════════════════════
# Step 1: Image Analysis with Azure AI Vision
# ═══════════════════════════════════════════════════════════════════════════════

def run_vision_analysis(photo_paths: list[str]) -> list[dict]:
    """Analyze inspection photos using Azure AI Vision 4.0.

    For each photo:
      - Call analyze_image() from app/vision.py
      - Call extract_visual_features() for a simplified summary
      - Collect results with image_path attached

    Args:
        photo_paths: List of paths to inspection photo files.

    Returns:
        List of dicts, each with keys:
            image_path, tags, objects, caption, dense_captions,
            read_text, features (simplified summary)
    """
    from app.vision import analyze_image, extract_visual_features

    results = []
    for path in photo_paths:
        print(f"  Analyzing: {os.path.basename(path)} ...")

        # TODO: Step 1 - Call analyze_image(path)
        # TODO: Attach the image_path to the analysis dict
        # TODO: Call extract_visual_features() and add as "features" key
        # TODO: Append to results
        raise NotImplementedError("Step 1: Implement run_vision_analysis")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# Step 2: Photo Classification with GPT-4o Multimodal
# ═══════════════════════════════════════════════════════════════════════════════

def run_classifications(
    photo_paths: list[str],
    vision_analyses: list[dict],
    temperature: float = 0.0,
) -> list[dict]:
    """Classify inspection photos using GPT-4o multimodal.

    For each photo, sends the image + optional Vision API tags to GPT-4o
    for structured classification into one of the 5 violation categories.
    Each classification includes a needs_review flag based on the
    confidence threshold.

    Args:
        photo_paths: List of paths to inspection photo files.
        vision_analyses: Vision API results from Step 1 (for tag context).
        temperature: LLM sampling temperature (default 0.0 for consistency).

    Returns:
        List of dicts, each with keys:
            image_path, category, confidence, reasoning, severity,
            needs_review, prompt_tokens, completion_tokens
    """
    from app.classifier import classify_photo

    results = []
    for i, path in enumerate(photo_paths):
        print(f"  Classifying: {os.path.basename(path)} ...")

        # Get Vision API tags for this photo (if available from Step 1)
        vision_tags = None
        if i < len(vision_analyses):
            tags_data = vision_analyses[i].get("tags", [])
            vision_tags = [t["name"] for t in tags_data if isinstance(t, dict)]

        # TODO: Step 2 - Call classify_photo(path, vision_tags, temperature)
        # TODO: Add "image_path" to the result
        # TODO: Append to results
        raise NotImplementedError("Step 2: Implement run_classifications")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# Step 3: Document Extraction with Document Intelligence
# ═══════════════════════════════════════════════════════════════════════════════

def run_ocr_pipeline(form_paths: list[str]) -> list[dict]:
    """Extract text and key-value pairs from inspection form PDFs.

    For each form:
      - Call extract_form_data() from app/doc_intel.py
      - Attach the form_path to the result

    Args:
        form_paths: List of paths to inspection form PDFs.

    Returns:
        List of dicts, each with keys:
            form_path, pages, key_value_pairs, tables
    """
    from app.doc_intel import extract_form_data

    results = []
    for path in form_paths:
        print(f"  Extracting: {os.path.basename(path)} ...")

        # TODO: Step 3 - Call extract_form_data(path)
        # TODO: Attach the form_path to the result
        # TODO: Append to results
        raise NotImplementedError("Step 3: Implement run_ocr_pipeline")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# Step 4: Build the Inspection Report
# ═══════════════════════════════════════════════════════════════════════════════

def run_report_builder(
    vision_analyses: list[dict],
    classifications: list[dict],
    ocr_results: list[dict],
    photo_paths: list[str],
    form_paths: list[str],
) -> dict:
    """Combine all pipeline outputs into a unified inspection report.

    Calls build_inspection_report() from app/report.py to merge
    Vision API analysis, GPT-4o classifications, and OCR extractions.

    Returns:
        dict with keys: total_photos, total_forms, findings,
                        auto_approved, needs_human_review,
                        category_counts, severity_distribution, summary
    """
    from app.report import build_inspection_report

    # TODO: Step 4 - Call build_inspection_report() with all collected data
    # TODO: Return the report dict
    raise NotImplementedError("Step 4: Implement run_report_builder")


# ═══════════════════════════════════════════════════════════════════════════════
# Step 5: Evaluation Harness — 3-Way Classifier Comparison
# ═══════════════════════════════════════════════════════════════════════════════

def run_evaluation() -> dict:
    """Run the evaluation harness comparing three classification approaches.

    Loads the eval set (data/eval_set.json), runs all three classifiers,
    computes metrics and cost analysis, and generates eval_report.json.

    Three-way comparison:
      1. Vision API tag heuristic (~$0.001/call)
      2. Zero-shot GPT-4o (~$0.02/call)
      3. Few-shot GPT-4o (~$0.05/call)

    Returns:
        dict with keys: vision_accuracy, gpt4o_accuracy, fewshot_accuracy,
                        agreement_rate, total_evaluated, cost_analysis
    """
    from app.eval import load_eval_set, run_eval, compare_classifiers
    from app.metrics import accuracy, precision_per_category, recall_per_category

    # TODO: Step 5.1 - Load the evaluation set
    # TODO: Step 5.2 - Run run_eval() to classify all cases with all three methods
    # TODO: Step 5.3 - Run compare_classifiers() to compute comparison metrics
    # TODO: Step 5.4 - Build the eval_report dict with:
    #   - vision_api section: accuracy, per_category_precision, per_category_recall
    #   - gpt4o_multimodal section: accuracy, per_category_precision,
    #     per_category_recall, total_cost, avg_latency
    #   - fewshot_gpt4o section: accuracy, per_category_precision,
    #     per_category_recall, total_cost, avg_latency, total_cached_tokens
    #   - comparison section: accuracy_delta, agreement_rate, disagreements,
    #     cost_analysis (include both cached and uncached cost per method)
    #   - recommendations list (human-readable strings)
    # TODO: Step 5.5 - Write eval_report.json
    raise NotImplementedError("Step 5: Implement run_evaluation")


def build_recommendations(comparison: dict) -> list[str]:
    """Generate human-readable recommendations from the classifier comparison.

    Args:
        comparison: Dict from compare_classifiers() with accuracy and cost data.

    Returns:
        List of recommendation strings.
    """
    recommendations = []

    # TODO: Step 5.6 - Generate 3-5 recommendations based on:
    #   - Which classifier is more accurate overall
    #   - Which categories each classifier handles better
    #   - Cost vs accuracy tradeoff (cost_per_correct comparison)
    #   - Whether few-shot improves over zero-shot enough to justify cost
    #   - How prompt caching affects the cost comparison at scale
    #   - Suggestions for production deployment
    raise NotImplementedError("Step 5.6: Implement build_recommendations")

    return recommendations


# ═══════════════════════════════════════════════════════════════════════════════
# Step 6: Input Safety and Validation
# ═══════════════════════════════════════════════════════════════════════════════

def validate_and_collect_files(
    photo_dir: str = "data/photos",
    form_dir: str = "data/forms",
) -> tuple[list[str], list[str]]:
    """Validate and collect all input files for the pipeline.

    Uses validate_image_file() and validate_pdf_file() from app/utils.py
    to ensure all files are valid before processing.

    Args:
        photo_dir: Directory containing inspection photos.
        form_dir: Directory containing inspection form PDFs.

    Returns:
        Tuple of (photo_paths, form_paths) — only valid files included.
    """
    from app.utils import validate_image_file, validate_pdf_file

    photo_paths = []
    form_paths = []

    # TODO: Step 6 - Scan photo_dir for image files
    #   For each file, call validate_image_file() — if valid, append to photo_paths
    #   If invalid (ValueError), print a warning and skip
    # TODO: Scan form_dir for PDF files
    #   For each file, call validate_pdf_file() — if valid, append to form_paths
    #   If invalid (ValueError), print a warning and skip
    raise NotImplementedError("Step 6: Implement validate_and_collect_files")

    return photo_paths, form_paths


def apply_pii_redaction(ocr_results: list[dict]) -> list[dict]:
    """Apply PII redaction to all OCR-extracted text.

    Uses redact_pii() from app/utils.py to replace phone numbers
    and SSN patterns with [REDACTED] in extracted text.

    Args:
        ocr_results: List of OCR result dicts from Step 3.

    Returns:
        The same list with text fields redacted in-place.
    """
    from app.utils import redact_pii

    # TODO: Step 6 - Iterate through each OCR result
    #   For each page, apply redact_pii() to the "text" field
    #   For each line in "lines", apply redact_pii()
    #   For each key_value_pair, apply redact_pii() to the "value" field
    raise NotImplementedError("Step 6: Implement apply_pii_redaction")

    return ocr_results


# ═══════════════════════════════════════════════════════════════════════════════
# Pipeline Orchestrator
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the full Inspector Vision pipeline.

    Steps:
      1. Validate and collect input files (Step 6)
      2. Analyze photos with Azure AI Vision (Step 1)
      3. Classify photos with GPT-4o multimodal (Step 2)
      4. Extract text from forms with Document Intelligence (Step 3)
      5. Apply PII redaction to OCR output (Step 6)
      6. Build the inspection report (Step 4)
      7. Run evaluation harness (Step 5)
      8. Write result.json with latency metadata
    """
    from app.utils import write_json

    print("=" * 60)
    print("Activity 4 - Inspector Vision Pipeline")
    print("=" * 60)

    # Latency tracking
    latency_ms = {}
    pipeline_start = time.time()

    # ── Collect and validate input files ──────────────────────────────────
    print("\n[1/6] Validating input files...")
    try:
        photo_paths, form_paths = validate_and_collect_files()
        print(f"   Found {len(photo_paths)} photos, {len(form_paths)} forms")
    except NotImplementedError:
        # Fallback: use hardcoded paths if validation not yet implemented
        photo_paths = []
        form_paths = []
        photo_dir = os.path.join("data", "photos")
        form_dir = os.path.join("data", "forms")
        if os.path.isdir(photo_dir):
            photo_paths = sorted(
                os.path.join(photo_dir, f)
                for f in os.listdir(photo_dir)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            )
        if os.path.isdir(form_dir):
            form_paths = sorted(
                os.path.join(form_dir, f)
                for f in os.listdir(form_dir)
                if f.lower().endswith(".pdf")
            )
        print(f"   (fallback) Found {len(photo_paths)} photos, {len(form_paths)} forms")

    # ── Step 1: Vision Analysis ───────────────────────────────────────────
    print("\n[Step 1] Analyzing photos with Azure AI Vision...")
    vision_analyses = []
    t0 = time.time()
    try:
        vision_analyses = run_vision_analysis(photo_paths)
        print(f"   [OK] Analyzed {len(vision_analyses)} photos")
    except NotImplementedError as e:
        print(f"   [SKIP] Not yet implemented: {e}")
    except Exception as e:
        print(f"   [ERR] {e}")
    latency_ms["vision"] = round((time.time() - t0) * 1000)

    # ── Step 2: GPT-4o Classification ─────────────────────────────────────
    print("\n[Step 2] Classifying photos with GPT-4o multimodal...")
    classifications = []
    t0 = time.time()
    try:
        classifications = run_classifications(photo_paths, vision_analyses)
        print(f"   [OK] Classified {len(classifications)} photos")
    except NotImplementedError as e:
        print(f"   [SKIP] Not yet implemented: {e}")
    except Exception as e:
        print(f"   [ERR] {e}")
    latency_ms["classification"] = round((time.time() - t0) * 1000)

    # Print classification summary with review flags
    if classifications:
        review_count = sum(1 for c in classifications if c.get("needs_review"))
        print(f"\n   Classification Results ({review_count} flagged for review):")
        print(f"   {'Photo':<30} {'Category':<22} {'Confidence':<12} {'Severity':<10} {'Review'}")
        print("   " + "-" * 84)
        for c in classifications:
            name = os.path.basename(c.get("image_path", "?"))
            cat = c.get("category", "?")
            conf = c.get("confidence", 0)
            sev = c.get("severity", "?")
            review = "YES" if c.get("needs_review") else "-"
            print(f"   {name:<30} {cat:<22} {conf:<12.2f} {sev:<10} {review}")

    # ── Step 3: Document Intelligence OCR ─────────────────────────────────
    print("\n[Step 3] Extracting text from inspection forms...")
    ocr_results = []
    t0 = time.time()
    try:
        ocr_results = run_ocr_pipeline(form_paths)
        print(f"   [OK] Extracted text from {len(ocr_results)} forms")
    except NotImplementedError as e:
        print(f"   [SKIP] Not yet implemented: {e}")
    except Exception as e:
        print(f"   [ERR] {e}")
    latency_ms["ocr"] = round((time.time() - t0) * 1000)

    # Print OCR summary
    if ocr_results:
        print("\n   OCR Results:")
        for ocr in ocr_results:
            name = os.path.basename(ocr.get("form_path", "?"))
            pages = len(ocr.get("pages", []))
            kvps = len(ocr.get("key_value_pairs", []))
            print(f"   {name}: {pages} page(s), {kvps} key-value pair(s)")

    # ── Step 6 (cont.): PII Redaction ─────────────────────────────────────
    if ocr_results:
        print("\n[Step 6] Applying PII redaction to OCR output...")
        try:
            ocr_results = apply_pii_redaction(ocr_results)
            print("   [OK] PII redaction applied")
        except NotImplementedError as e:
            print(f"   [SKIP] Not yet implemented: {e}")
        except Exception as e:
            print(f"   [ERR] {e}")

    # ── Step 4: Build Inspection Report ───────────────────────────────────
    print("\n[Step 4] Building inspection report...")
    report = {}
    try:
        report = run_report_builder(
            vision_analyses, classifications, ocr_results,
            photo_paths, form_paths,
        )
        auto = len(report.get("auto_approved", []))
        review = len(report.get("needs_human_review", []))
        print(f"   [OK] Report: {report.get('total_photos', 0)} photos, "
              f"{report.get('total_forms', 0)} forms, "
              f"{len(report.get('findings', []))} findings")
        print(f"   [OK] Auto-approved: {auto}, Needs human review: {review}")
    except NotImplementedError as e:
        print(f"   [SKIP] Not yet implemented: {e}")
    except Exception as e:
        print(f"   [ERR] {e}")

    # Print report summary
    if report.get("summary"):
        print(f"\n   Summary: {report['summary']}")

    # ── Step 5: Evaluation Harness (3-way comparison) ─────────────────────
    print("\n[Step 5] Running evaluation harness (Tag Heuristic vs Zero-shot GPT-4o vs Few-shot GPT-4o)...")
    evaluation = {}
    eval_report = {}
    t0 = time.time()
    try:
        eval_report = run_evaluation()
        evaluation = {
            "vision_accuracy": eval_report.get("vision_api", {}).get("accuracy", 0),
            "gpt4o_accuracy": eval_report.get("gpt4o_multimodal", {}).get("accuracy", 0),
            "fewshot_accuracy": eval_report.get("fewshot_gpt4o", {}).get("accuracy", 0),
            "agreement_rate": eval_report.get("comparison", {}).get("agreement_rate", 0),
            "total_evaluated": eval_report.get("eval_set_size", 0),
        }
        print(f"   [OK] Vision API accuracy:  {evaluation['vision_accuracy']:.1%}")
        print(f"   [OK] GPT-4o (zero-shot):   {evaluation['gpt4o_accuracy']:.1%}")
        print(f"   [OK] GPT-4o (few-shot):    {evaluation['fewshot_accuracy']:.1%}")
        print(f"   [OK] Agreement rate:       {evaluation['agreement_rate']:.1%}")
        # Print cost analysis if available
        cost = eval_report.get("comparison", {}).get("cost_analysis", {})
        if cost:
            print(f"\n   Cost Analysis (cache-aware):")
            for method, data in cost.items():
                if isinstance(data, dict) and "total_cost" in data:
                    cached = data.get("total_cached_tokens", 0)
                    cache_info = f", {cached:,} cached tokens" if cached else ""
                    print(f"     {method}: ${data['total_cost']:.4f} total, "
                          f"${data.get('cost_per_correct', 0):.4f}/correct"
                          f"{cache_info}")
    except NotImplementedError as e:
        print(f"   [SKIP] Not yet implemented: {e}")
    except Exception as e:
        print(f"   [ERR] {e}")
    latency_ms["evaluation"] = round((time.time() - t0) * 1000)

    # ── Total latency ─────────────────────────────────────────────────────
    latency_ms["total"] = round((time.time() - pipeline_start) * 1000)

    # ── Determine status ──────────────────────────────────────────────────
    has_vision = len(vision_analyses) > 0
    has_classifications = len(classifications) > 0
    has_ocr = len(ocr_results) > 0
    has_report = bool(report.get("findings"))
    has_eval = bool(evaluation.get("total_evaluated"))

    if has_vision and has_classifications and has_ocr and has_report and has_eval:
        status = "success"
    elif has_vision or has_classifications or has_ocr:
        status = "partial"
    else:
        status = "error"

    # ── Build result.json ─────────────────────────────────────────────────
    result = {
        "task": "inspector_vision",
        "status": status,
        "outputs": {
            "vision_analyses": vision_analyses,
            "classifications": classifications,
            "ocr_results": ocr_results,
            "inspection_report": report,
            "evaluation": evaluation,
        },
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": "gpt-4o",
            "vision_model": "image-analysis-4.0",
            "doc_intel_model": "prebuilt-document",
            "sdk_version": _get_sdk_version(),
            "latency_ms": latency_ms,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
        },
    }

    write_json("result.json", result)

    # ── Final summary ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"Pipeline complete - status: {status}")
    print("=" * 60)
    print(f"  Vision analyses:   {len(vision_analyses)}")
    print(f"  Classifications:   {len(classifications)}")
    print(f"  OCR extractions:   {len(ocr_results)}")
    print(f"  Report findings:   {len(report.get('findings', []))}")
    print(f"  Eval cases:        {evaluation.get('total_evaluated', 0)}")
    if report.get("needs_human_review"):
        print(f"  Flagged for review: {len(report['needs_human_review'])}")
    print(f"  Total latency:     {latency_ms.get('total', 0)}ms")
    print(f"\nResult written to result.json")
    if eval_report:
        print(f"Eval report written to eval_report.json")


if __name__ == "__main__":
    main()
