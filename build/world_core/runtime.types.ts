// Generated from World.Core v0.1
export interface Vec3 {
  x: number;
  y: number;
  z: number;
}

export interface ItemRef {
  id: string;
  qty: number;
}

export interface Player {
  id: string;
  name: string;
  level: number;
  position: Vec3;
  stamina: number;
  inventory: ItemRef[];
}

export interface Input {
  playerId: string;
  axisX: number;
  axisY: number;
}
