from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


Joint = Tuple[float, float, float]


@dataclass
class HandPose:
    """Simple 3D hand pose data from 21 landmark points."""

    landmarks: List[Joint]

    def grip_strength(self) -> float:
        if not self.landmarks:
            return 0.0
        thumb_tip = self.landmarks[4]
        index_tip = self.landmarks[8]
        distance = sum((a - b) ** 2 for a, b in zip(thumb_tip, index_tip)) ** 0.5
        return max(0.0, min(1.0, 1.0 - distance * 3.5))


class HandTrackingEngine:
    """Tracks hand states and emits game-friendly gesture events."""

    def __init__(self, smoothing: float = 0.65):
        self.smoothing = smoothing
        self._previous: Dict[str, HandPose] = {}

    def smooth_pose(self, hand_id: str, pose: HandPose) -> HandPose:
        previous = self._previous.get(hand_id)
        if previous is None or not previous.landmarks:
            self._previous[hand_id] = pose
            return pose

        blended = []
        for p_joint, c_joint in zip(previous.landmarks, pose.landmarks):
            blended.append(
                tuple(
                    (self.smoothing * p) + ((1 - self.smoothing) * c)
                    for p, c in zip(p_joint, c_joint)
                )
            )
        smoothed = HandPose(landmarks=blended)
        self._previous[hand_id] = smoothed
        return smoothed

    def classify_gesture(self, pose: HandPose) -> str:
        grip = pose.grip_strength()
        if grip > 0.75:
            return "fist"
        if grip > 0.45:
            return "weapon_ready"
        return "open_hand"
