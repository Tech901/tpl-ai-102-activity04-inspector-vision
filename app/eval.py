"""Evaluation harness comparing three classification approaches.

Step 5: Run all classifiers against a labeled eval set, compute metrics,
and generate eval_report.json with accuracy comparison, cost analysis,
and recommendations.

Three-way comparison:
  1. Vision API Tag Heuristic — keyword matching on Vision API tags
  2. Zero-shot GPT-4o — image + classification prompt (no examples)
  3. Few-shot GPT-4o — image + example images per category
"""
import json
import os


def load_eval_set(path: str | None = None) -> list[dict]:
    """Load the labeled evaluation dataset.

    Each case has: id, case_id, image_path, expected_category, description,
    neighborhood.

    Args:
        path: Path to eval_set.json. Defaults to data/eval_set.json
              relative to the activity root.

    Returns:
        List of eval case dicts.
    """
    if path is None:
        # Resolve relative to this file's location (app/ -> parent -> data/)
        app_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(os.path.dirname(app_dir), "data", "eval_set.json")
    with open(path) as f:
        return json.load(f)


def load_pricing(path: str | None = None) -> dict:
    """Load API pricing data for cost calculations.

    Args:
        path: Path to pricing.json. Defaults to data/pricing.json
              relative to the activity root.

    Returns:
        Dict with pricing info per classifier method.
    """
    if path is None:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(os.path.dirname(app_dir), "data", "pricing.json")
    with open(path) as f:
        return json.load(f)


def run_eval(eval_cases: list[dict] | None = None) -> dict:
    """Run all three classifiers against the eval set.

    For each case in the eval set:
      1. Run Vision API analysis + tag-based heuristic classification
      2. Run GPT-4o zero-shot multimodal classification
      3. Run GPT-4o few-shot multimodal classification (with example images)
      4. Record predictions, expected labels, and token usage

    Args:
        eval_cases: List of eval case dicts. If None, loads from
                    data/eval_set.json.

    Returns:
        dict with keys:
            vision_results: list of dicts, each with:
                id, image_path, expected, predicted, confidence, method
            gpt4o_results: list of dicts, each with:
                id, image_path, expected, predicted, confidence, method,
                prompt_tokens, completion_tokens, cached_tokens
            fewshot_results: list of dicts, each with:
                id, image_path, expected, predicted, confidence, method,
                prompt_tokens, completion_tokens, cached_tokens
    """
    # TODO: Step 5.1 - Load eval cases if not provided
    #   if eval_cases is None:
    #       eval_cases = load_eval_set()

    # TODO: Step 5.2 - Run Vision API + tag heuristic for each case
    #   from app.vision import analyze_image
    #   from app.classifier import classify_with_tags
    #   vision_results = []
    #   for case in eval_cases:
    #       analysis = analyze_image(case["image_path"])
    #       prediction = classify_with_tags(case["image_path"], analysis["tags"])
    #       vision_results.append({
    #           "id": case["id"],
    #           "image_path": case["image_path"],
    #           "expected": case["expected_category"],
    #           "predicted": prediction["category"],
    #           "confidence": prediction["confidence"],
    #           "method": "tag_heuristic",
    #       })

    # TODO: Step 5.3 - Run GPT-4o zero-shot for each case
    #   from app.classifier import classify_photo
    #   gpt4o_results = []
    #   for case in eval_cases:
    #       prediction = classify_photo(case["image_path"])
    #       gpt4o_results.append({
    #           "id": case["id"],
    #           "image_path": case["image_path"],
    #           "expected": case["expected_category"],
    #           "predicted": prediction["category"],
    #           "confidence": prediction["confidence"],
    #           "method": "gpt4o_multimodal",
    #           "prompt_tokens": prediction.get("prompt_tokens", 0),
    #           "completion_tokens": prediction.get("completion_tokens", 0),
    #           "cached_tokens": prediction.get("cached_tokens", 0),
    #       })

    # TODO: Step 5.4 - Run GPT-4o few-shot for each case
    #   from app.classifier import classify_photo_fewshot
    #   fewshot_results = []
    #   for case in eval_cases:
    #       prediction = classify_photo_fewshot(case["image_path"])
    #       fewshot_results.append({
    #           "id": case["id"],
    #           "image_path": case["image_path"],
    #           "expected": case["expected_category"],
    #           "predicted": prediction["category"],
    #           "confidence": prediction["confidence"],
    #           "method": "fewshot_gpt4o",
    #           "prompt_tokens": prediction.get("prompt_tokens", 0),
    #           "completion_tokens": prediction.get("completion_tokens", 0),
    #           "cached_tokens": prediction.get("cached_tokens", 0),
    #       })

    # TODO: Step 5.5 - Return all three result sets
    #   return {
    #       "vision_results": vision_results,
    #       "gpt4o_results": gpt4o_results,
    #       "fewshot_results": fewshot_results,
    #   }

    raise NotImplementedError("Step 5.1-5.5: Implement run_eval")


def compare_classifiers(
    vision_results: list[dict],
    gpt4o_results: list[dict],
    eval_cases: list[dict],
    fewshot_results: list[dict] | None = None,
) -> dict:
    """Compare classifier performance on the eval set with cost analysis.

    Computes accuracy, per-category metrics, agreement rate, cost-per-correct,
    and identifies cases where the classifiers disagree.

    Args:
        vision_results: Results from Vision API tag-based classifier.
        gpt4o_results: Results from GPT-4o zero-shot multimodal classifier.
        eval_cases: Original eval cases with ground truth labels.
        fewshot_results: Optional results from GPT-4o few-shot classifier.

    Returns:
        dict with keys:
            vision_accuracy: float (0.0-1.0)
            gpt4o_accuracy: float (0.0-1.0)
            fewshot_accuracy: float (0.0-1.0) (if fewshot_results provided)
            vision_metrics: dict with per_category_precision, per_category_recall
            gpt4o_metrics: dict with per_category_precision, per_category_recall
            fewshot_metrics: dict (if fewshot_results provided)
            agreement_rate: float (fraction where all classifiers agree)
            disagreements: list of dicts, each with:
                id, image_path, expected, vision_predicted, gpt4o_predicted,
                fewshot_predicted (if available)
            cost_analysis: dict with per-classifier cost breakdown and
                cost_per_correct for each approach
    """
    # TODO: Step 5.6 - Compute comparison metrics
    #   from app.metrics import accuracy, precision_per_category, recall_per_category
    #
    #   vision_accuracy = accuracy(vision_results)
    #   gpt4o_accuracy = accuracy(gpt4o_results)
    #
    #   # Cost analysis (cache-aware)
    #   # Azure OpenAI automatically caches the longest common prefix across
    #   # requests. Cached input tokens are billed at 50% of the normal rate.
    #   # For few-shot prompts, the system message + example images (~15K tokens)
    #   # are identical across calls, so most input tokens are cached after the
    #   # first request.
    #   pricing = load_pricing()
    #   vision_total_cost = len(vision_results) * pricing["vision_api"]["per_call"]
    #
    #   def _compute_llm_cost(results, pricing_key):
    #       """Compute total cost accounting for cached vs uncached input tokens."""
    #       p = pricing[pricing_key]
    #       total = 0.0
    #       for r in results:
    #           cached = r.get("cached_tokens", 0)
    #           uncached = r.get("prompt_tokens", 0) - cached
    #           total += (
    #               uncached / 1000 * p["input_per_1k_tokens"]
    #               + cached / 1000 * p["cached_input_per_1k_tokens"]
    #               + r.get("completion_tokens", 0) / 1000 * p["output_per_1k_tokens"]
    #           )
    #       return total
    #
    #   gpt4o_total_cost = _compute_llm_cost(gpt4o_results, "gpt4o")
    #
    #   # Cost per correct prediction
    #   vision_correct = sum(1 for r in vision_results if r["expected"] == r["predicted"])
    #   gpt4o_correct = sum(1 for r in gpt4o_results if r["expected"] == r["predicted"])
    #   vision_cost_per_correct = vision_total_cost / vision_correct if vision_correct else float("inf")
    #   gpt4o_cost_per_correct = gpt4o_total_cost / gpt4o_correct if gpt4o_correct else float("inf")
    #
    #   # Agreement: count cases where all classifiers predicted the same category
    #   agreements = sum(1 for v, g in zip(vision_results, gpt4o_results)
    #                    if v["predicted"] == g["predicted"])
    #   agreement_rate = agreements / len(eval_cases) if eval_cases else 0.0
    #
    #   # Disagreements: list cases where they differ
    #   disagreements = []
    #   for v, g, case in zip(vision_results, gpt4o_results, eval_cases):
    #       if v["predicted"] != g["predicted"]:
    #           d = {
    #               "id": case["id"],
    #               "image_path": case["image_path"],
    #               "expected": case["expected_category"],
    #               "vision_predicted": v["predicted"],
    #               "gpt4o_predicted": g["predicted"],
    #           }
    #           disagreements.append(d)
    #
    #   # If fewshot results provided, include in comparison
    #   if fewshot_results:
    #       fewshot_accuracy = accuracy(fewshot_results)
    #       fewshot_total_cost = _compute_llm_cost(fewshot_results, "gpt4o_fewshot")
    #       fewshot_correct = sum(1 for r in fewshot_results
    #                            if r["expected"] == r["predicted"])
    #       fewshot_cost_per_correct = (fewshot_total_cost / fewshot_correct
    #                                  if fewshot_correct else float("inf"))
    #       # Total cached tokens across all few-shot calls shows how much
    #       # prompt caching saved — the system message + example images are
    #       # cached after the first request.
    #       fewshot_cached_total = sum(r.get("cached_tokens", 0)
    #                                 for r in fewshot_results)
    #       # ... add to cost_analysis, disagreements, etc.

    raise NotImplementedError("Step 5.6: Implement compare_classifiers")
