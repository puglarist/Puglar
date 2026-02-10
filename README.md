# Puglar

## Meta Quest hand tracking

This repository now includes a production-ready hand tracking configuration schema for Meta Quest, plus a baseline config and runtime helper.

### Added files

- `meta-quest-hand-tracking.schema.json`: Complete JSON schema for platform/runtime/tracking/gesture/debug settings.
- `meta-quest-hand-tracking.config.json`: Validated default config targeting Quest + OpenXR hand tracking.
- `src/metaQuestHandTracking.js`: Runtime helper for confidence gating, gesture cooldown handling, and debug metrics.
- `scripts/validate_hand_tracking_config.py`: Local validator to ensure config conforms to schema.

### Validate configuration

```bash
python scripts/validate_hand_tracking_config.py
```

### Debug checklist (Quest device)

1. Enable hand tracking in headset settings.
2. Ensure app uses OpenXR (`XR_EXT_hand_tracking`) or OVR hand APIs.
3. Set `debug.overlay=true` and `debug.logLevel="debug"` in config.
4. Verify confidence values exceed `tracking.confidenceThreshold` during use.
5. Tune `enterThreshold`/`exitThreshold` per gesture if false positives occur.
