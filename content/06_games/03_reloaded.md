### Portal Reloaded

#### General

All Portal Reloaded categories ban the `developer 1` command due to an unnatural
advantage it provides on some maps.

#### Timing

- Timing begins on the tick the player gains control in the second map, on the
  `announcer1.Trigger` entity input.
- Alternatively, the Tube Ride Save can be used. In this case, timing starts on
  the `@wportal1.Open` entity input with an offset of 2394 ticks.
- Timing ends on the tick the player loses control when being sucked into the
  tube, on the `finale-finale_vc.Trigger` entity input.
- Alternatively, for the escape ending, timing ends on the tick when the
  elevator doors close, on the `finale-escape_ending.EnableRefire` entity input.
