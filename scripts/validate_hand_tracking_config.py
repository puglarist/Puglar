#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def fail(msg: str) -> None:
    raise ValueError(msg)


def require_keys(obj, keys, path):
    for k in keys:
        if k not in obj:
            fail(f"Missing key {path}.{k}")


def validate() -> None:
    cfg = json.loads(Path('meta-quest-hand-tracking.config.json').read_text())

    require_keys(cfg, ['platform', 'runtime', 'tracking', 'gestures', 'debug'], 'root')

    platform = cfg['platform']
    require_keys(platform, ['target', 'minOsVersion'], 'platform')
    if platform['target'] != 'meta-quest':
        fail('platform.target must be meta-quest')
    if platform['minOsVersion'] < 49:
        fail('platform.minOsVersion must be >= 49')

    runtime = cfg['runtime']
    require_keys(runtime, ['xrBackend', 'handTrackingApi'], 'runtime')
    if runtime['xrBackend'] not in ('OpenXR', 'OVRPlugin'):
        fail('runtime.xrBackend invalid')

    tracking = cfg['tracking']
    require_keys(tracking, ['enabled', 'trackingFrequencyHz', 'confidenceThreshold'], 'tracking')
    if tracking['enabled'] is not True:
        fail('tracking.enabled must be true')
    if not (30 <= tracking['trackingFrequencyHz'] <= 120):
        fail('tracking.trackingFrequencyHz out of range')
    if not (0 <= tracking['confidenceThreshold'] <= 1):
        fail('tracking.confidenceThreshold out of range')

    gestures = cfg['gestures']
    for gesture_name in ['pinch', 'grab']:
        if gesture_name not in gestures:
            fail(f'gestures.{gesture_name} missing')
        g = gestures[gesture_name]
        require_keys(g, ['enabled', 'enterThreshold', 'exitThreshold', 'cooldownMs'], f'gestures.{gesture_name}')
        if g['enterThreshold'] <= g['exitThreshold']:
            fail(f'gestures.{gesture_name} enterThreshold should be > exitThreshold')

    debug = cfg['debug']
    require_keys(debug, ['enabled', 'overlay', 'logLevel', 'telemetry'], 'debug')
    if debug['logLevel'] not in ('error', 'warn', 'info', 'debug', 'trace'):
        fail('debug.logLevel invalid')

    telemetry = debug['telemetry']
    require_keys(
        telemetry,
        ['emitJointConfidence', 'emitFrameTiming', 'emitGestureTransitions'],
        'debug.telemetry',
    )


if __name__ == '__main__':
    try:
        validate()
        print('Meta Quest hand tracking config is valid ✅')
        sys.exit(0)
    except Exception as exc:
        print(f'Validation failed: {exc}')
        sys.exit(1)
