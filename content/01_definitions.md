## Definitions

### Commands

In the game's console, you can execute commands, as well as bind keys to execute
commands. We define several classes of command.

"Functional Commands" are commands which have some effect on the run or the runner's
ability to perform it. The vast majority of commands fit into this category -
effectively the only ones that don't are ones which impact timing, such as
`sar_speedrun_result`, and purely cosmetic ones, such as `sar_hud_set_text`.

"Action Commands" are a subset of functional commands defined as any command which has
a direct effect on the game world. This includes all player movement commands
(`+forward`, `-forward`, `+duck`, etc), as well as commands such as `load`.

### Pause Abuse

Pause Abuse is defined as using game pauses (via the ESC key, `gameui` commands, or
opening the developer console) to affect the chance of some event occurring, make an
event possible, or otherwise contribute to the run. For instance, the Betsrighter jump
in `sp_a1_wakeup` can be done far more consistently by console pausing as you land -
as such, pausing at this moment in the run is considered pause abuse, as it affects
your chances of getting the jump. More subtly, pausing while lining up a precise shot
is also pause abuse, since the time you are paused can allow you time to read your
coordinates and prepare to move your mouse correctly.

### Save/Load Abuse (SLA)

Save/Load Abuse (SLA) is defined as using any unnatural load or level transition (i.e.
anything other than touching a changelevel trigger in the map) in order to affect the
chance of some event occurring or make an event possible. For instance, saveload
clipping is considered SLA, since it achieves an effect which would otherwise be
impossible. Similarly, loading saves to retry lucky door skip in
`sp_a2_bridge_the_gap` is SLA, as it affects the overall chance of successfully
getting through the door. Exceptions are made to this rule for physics RNG
specifically, so that loading saves and getting different physics RNG is not
considered SLA, since this RNG is prevalent to the point of being unavoidable.

### Out of Bounds (OOB)

The Source Engine has a strict technical definition of whether a point is "out of
bounds" based on its BSP world system (a point is out of bounds if it is in a
`CONTENTS_SOLID` leaf and not within a brush). We define the player themselves as being
out of bounds if a) the player's eye position goes out of bounds or b) all 8 vertices
of the player's bounding box go out of bounds.
