"""Classification metrics for the evaluation harness.

Step 5: Accuracy, precision, recall, and confusion matrix calculations
for comparing Vision API tag-based and GPT-4o multimodal classifiers.
"""
from app import VALID_CATEGORIES


def accuracy(results: list[dict]) -> float:
    """Calculate overall classification accuracy.

    Args:
        results: List of result dicts, each with "expected" (or "actual")
                 and "predicted" keys.

    Returns:
        float between 0.0 and 1.0. Returns 0.0 for an empty list.
    """
    # TODO: Step 5 - Implement accuracy calculation
    #   if not results:
    #       return 0.0
    #   correct = sum(1 for r in results
    #                 if r.get("expected", r.get("actual")) == r["predicted"])
    #   return correct / len(results)

    raise NotImplementedError("Step 5: Implement accuracy()")


def precision_per_category(results: list[dict]) -> dict[str, float]:
    """Calculate precision for each category.

    Precision = TP / (TP + FP) for each category.
    Of all predictions for category X, how many were actually category X?

    Args:
        results: List of result dicts with "expected" (or "actual")
                 and "predicted" keys.

    Returns:
        Dict mapping category name -> precision float (0.0-1.0).
        Categories with no predictions get precision 0.0.
    """
    # TODO: Step 5 - Implement per-category precision
    #   Use r.get("expected", r.get("actual")) to read the ground-truth label
    #   (visible tests use "actual", hidden tests use "expected").
    #   For each category in VALID_CATEGORIES:
    #     TP = count where expected == category AND predicted == category
    #     FP = count where expected != category AND predicted == category
    #     precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0

    raise NotImplementedError("Step 5: Implement precision_per_category()")


def recall_per_category(results: list[dict]) -> dict[str, float]:
    """Calculate recall for each category.

    Recall = TP / (TP + FN) for each category.
    Of all actual instances of category X, how many did the model catch?

    Args:
        results: List of result dicts with "expected" (or "actual")
                 and "predicted" keys.

    Returns:
        Dict mapping category name -> recall float (0.0-1.0).
        Categories with no actual instances get recall 0.0.
    """
    # TODO: Step 5 - Implement per-category recall
    #   Use r.get("expected", r.get("actual")) to read the ground-truth label.
    #   For each category in VALID_CATEGORIES:
    #     TP = count where expected == category AND predicted == category
    #     FN = count where expected == category AND predicted != category
    #     recall = TP / (TP + FN) if (TP + FN) > 0 else 0.0

    raise NotImplementedError("Step 5: Implement recall_per_category()")


def confusion_matrix(results: list[dict]) -> dict:
    """Build a confusion matrix from classification results.

    Args:
        results: List of result dicts with "expected" (or "actual")
                 and "predicted" keys.

    Returns:
        Dict mapping "expected|predicted" strings to counts.
        Example: {"pothole|pothole": 4, "pothole|graffiti": 1, ...}
    """
    # TODO: Step 5 - Build confusion matrix
    #   matrix = {}
    #   for r in results:
    #       expected = r.get("expected", r.get("actual"))
    #       key = f"{expected}|{r['predicted']}"
    #       matrix[key] = matrix.get(key, 0) + 1
    #   return matrix

    raise NotImplementedError("Step 5: Implement confusion_matrix()")
