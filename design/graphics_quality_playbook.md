# Graphics Quality Playbook (MW2 Promo Style)

This repository did not contain a running graphics pipeline, so this playbook defines a practical production standard to reach the visual quality shown in your examples.

## 1) Target Look

- **Cinematic military vibe**: high-contrast, gritty steel/blues, controlled haze, dramatic sunlight.
- **Readable ad hierarchy**: big title, short subtitle, one-line value prop, footer strip for feature bullets.
- **Premium finish**: film grain, vignette, atmospheric fog, selective glow/rim highlights.
- **Consistent palette**:
  - Primary: `#5E87B8`, `#86A6D2`, `#1F2D46`
  - Accent: `#BFD6F0`
  - Neutral shadows: `#0D1420`, `#101827`

## 2) Composition Rules

- Subject should occupy **35–45%** of frame area.
- Leave an intentional “text lane” with reduced texture/noise behind title.
- Use a strong depth stack:
  - Foreground dust/fog (soft)
  - Mid-ground subject
  - Background skyline/facilities/clouds
- Horizon should sit around lower third for stronger hero framing.

## 3) Typography Rules

- Headline font style: condensed bold, military/sport sans.
- Title size target: **12–18%** of image height.
- Subtitle size target: **4–6%** of image height.
- Add subtle bevel/inner highlight to headline only.
- Keep feature bullets in a footer bar with separator dots.

## 4) Local Photo Upgrade Workflow (for ATV photos)

Use these steps on your own photos like the quad images:

1. **Lens + perspective cleanup**
   - Correct verticals and crop to 16:9 or 4:5 deliverable.
2. **Subject separation**
   - Mask ATV/rider and boost local contrast + clarity.
3. **Background treatment**
   - Darken and cool the background by ~10–20% luminance.
4. **Cinematic relight**
   - Add directional top-right key light + soft rim on vehicle edges.
5. **Atmospherics**
   - Add controlled fog bands near the floor and corners.
6. **Texture pass**
   - Fine grain (not noisy), slight halation on highlights.
7. **Brand overlay**
   - Add title/subtitle in a safe text region with glow/underline.

## 5) AI Prompt Templates

### A) Base scene generation prompt

```text
Cinematic modern military promo banner, ultra-detailed tactical environment, dramatic storm clouds, volumetric sunlight, realistic dust and fog layers, high dynamic range, gritty steel-blue color grade, sharp subject silhouette, premium commercial ad composition, space for text on left, hero subject on right, clean readability, 8k detail, photorealistic, professional lighting, subtle film grain
```

### B) Image-to-image enhancement prompt (for your ATV pictures)

```text
Enhance this real ATV garage photo into a premium cinematic promotional image while preserving the exact vehicle identity and geometry. Improve lighting realism, add controlled atmospheric haze, deepen shadows, increase material definition on tires/metal/plastics, remove clutter distractions, keep natural textures, create ad-grade contrast and color depth, blue-gray cinematic grade, high detail, no cartoon look, no over-smoothing.
```

### C) Negative prompt

```text
cartoon, anime, overprocessed HDR, plastic skin, fake reflections, warped wheels, melted geometry, extra limbs, text artifacts, watermark, blurry edges, oversaturated neon, muddy details
```

## 6) Export Standards

- Master: PNG (lossless), 3840x2160 or 2560x1440.
- Social: 1080x1350, 1080x1920, 1200x628.
- Sharpening: apply at output size only.
- Keep title-safe margins at 6–8%.

## 7) Quick Quality Checklist

A graphic is “ship-ready” only if all are true:

- [ ] Subject reads instantly at thumbnail size.
- [ ] Headline legible in <1 second.
- [ ] Atmosphere adds depth but does not hide details.
- [ ] No obvious AI defects (hands, geometry, text warping).
- [ ] Palette and typography match the brand system.
