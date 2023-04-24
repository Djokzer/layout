---
title: Simple
author: John Doe
date: 2018-01-01
font: fonts/Economica-Bold.ttf
font-size-text: 50
font-size-title: 150
---

# This, is GRAHAM !
## The most awesome thing you'll ever see
As much as we like to think we're invincible, we're not. But what if we were to change? What if our bodies were built to survive a low impact crash? What might we look like? The result of these questions is Graham, a reminder of just how vulnerable our bodies really are.

--- 

# The definition of handsomeness
## What a charismatic gentleman
![This is graham](examples/assets/graham1.jpg)

---

# Main features
1. Bigger brain with more fluid and more ligaments
2. Bigger skull wiht inbuilt crumple zones absorb impact
3. A lot of fatty tissue on the face to absorb energy of an impact
4. An extra joint on the lower leg to give him a spring loaded jump

---

# Visit graham
-  SEPTEMBER 12 - NOVEMBER 4, 2018
-  UNIVERSITY OF MELBOURNE, MASSON RD, PARKVILLE VIC 3010
-  TUESDAY - SATURDAY from 12PM to 6PM
-  MELBOURNE SCHOOL OF DESIGN, UNIVERSITY OF MELBOURNE
---

# This is just some random code
### It's ugly for now but it still in dev
```rust
async fn main() {
    let mut emitter = Emitter::new(EmitterConfig {
        lifetime: 0.5,
        amount: 5,
        initial_direction_spread: 0.0,
        initial_velocity: -50.0,
        size: 2.0,
        size_curve: Some(Curve {
            points: vec![(0.0, 0.5), (0.5, 1.0), (1.0, 0.0)],
            ..Default::default()
        }),

        blend_mode: BlendMode::Additive,
        ..Default::default()
    });

    loop {
        clear_background(BLACK);

        let camera = Camera2D::from_display_rect(Rect::new(0.0, 0.0, 100.0, 100.0));

        set_camera(&camera);

        emitter.draw(vec2(50., 50.));

        next_frame().await
    }
}
```