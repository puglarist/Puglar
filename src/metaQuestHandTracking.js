/**
 * Meta Quest hand tracking runtime helper.
 * Designed for WebXR/OpenXR style joint updates.
 */
export class MetaQuestHandTracking {
  constructor(config) {
    this.config = config;
    this.lastGestureAt = new Map();
  }

  shouldTrack(handConfidence) {
    if (!this.config.tracking.enabled) return false;
    return handConfidence >= this.config.tracking.confidenceThreshold;
  }

  evaluateGesture(score, gestureName, nowMs) {
    const gesture = this.config.gestures[gestureName];
    if (!gesture || !gesture.enabled) return false;

    const lastAt = this.lastGestureAt.get(gestureName) || 0;
    if (nowMs - lastAt < gesture.cooldownMs) return false;

    const active = score >= gesture.enterThreshold;
    if (active) this.lastGestureAt.set(gestureName, nowMs);
    return active;
  }

  frameToDebugMetrics(frameTimingMs, jointConfidence) {
    return {
      frameTimingMs,
      avgJointConfidence: Number(jointConfidence.toFixed(3)),
      trackingStable:
        frameTimingMs <= (1000 / this.config.tracking.trackingFrequencyHz) * 1.25 &&
        jointConfidence >= this.config.tracking.confidenceThreshold,
    };
  }
}
