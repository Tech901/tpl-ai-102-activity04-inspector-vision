---
title: "Activity 4 Reflection - Inspector Vision"
type: reflection
version: "1.0.0"
---

# Activity 4 Reflection

Answer each question in 3-5 sentences. Thoughtful, specific responses earn full credit.

## 1. Vision API vs GPT-4o

How did the accuracy of the Vision API tag-based heuristic compare to GPT-4o multimodal classification? What types of images did each approach handle well or poorly? Which would you recommend for a production Memphis 311 system and why?

## 2. Feature Selection

Which Azure AI Vision visual features (tags, objects, captions, dense captions, read/OCR) were most useful for the inspection pipeline? Were any features less useful than expected? How would you adjust your feature selection for a different domain (e.g., retail inventory or healthcare)?

## 3. Document Intelligence

What challenges did you encounter extracting key-value pairs from the inspection forms? How might variations in form layout, handwriting, or scan quality affect OCR accuracy in a real-world deployment?

## 4. Multimodal Prompting

How did you design your GPT-4o classification system message and prompt? Did including Vision API tags alongside the image change the classification results? What prompt engineering techniques helped most?

## 5. Production Readiness

If Memphis deployed this inspection pipeline citywide processing hundreds of photos daily, what accuracy threshold would you set before trusting automated classifications? What safety considerations should be in place for automated violation reporting (false positives, PII exposure, bias)?
