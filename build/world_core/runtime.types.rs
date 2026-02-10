// Generated from World.Core v0.1
#[derive(Debug, Clone)]
pub struct Vec3 {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

#[derive(Debug, Clone)]
pub struct ItemRef {
    pub id: String,
    pub qty: u16,
}

#[derive(Debug, Clone)]
pub struct Player {
    pub id: String,
    pub name: String,
    pub level: u16,
    pub position: Vec3,
    pub stamina: f32,
    pub inventory: Vec<ItemRef>,
}

#[derive(Debug, Clone)]
pub struct Input {
    pub playerId: String,
    pub axisX: f32,
    pub axisY: f32,
}
