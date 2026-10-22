# Legacy scripts (not used)

These built the first version of the datasets (commit cff8803) from batch summaries. That version mapped
topics to the wrong scan pages, so it was replaced by the page-by-page pipeline in `scripts/`
(`agy_transcribe.py` → `agy_segment.py` → `agy_enrich.py` → `agy_lessons.py` → `build_from_pages.py`).
They are kept for reference only. Nothing imports them.
