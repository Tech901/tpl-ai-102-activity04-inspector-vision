"""Activity 4 -- Inspector Vision shared constants."""

VALID_CATEGORIES = ("pothole", "graffiti", "broken_streetlight", "illegal_dumping", "water_damage", "unknown")

# Classifications below this confidence threshold are flagged for human review.
# Students configure this value in Step 2 (D2.2 — responsible AI, human oversight).
CONFIDENCE_THRESHOLD = 0.7
