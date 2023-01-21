### Portal 2

#### General

When running a non-splitscreen cooperative category, progress must be entirely reset
before every run. It is recommended to do this using `sar_coop_reset_progress`.
Alternatively, it can be achieved by running `mp_coop_mark_all_maps_incomplete` and
`mp_coop_lock_all_taunts`, followed by returning to the main menu and re-inviting
your partner.

#### Timing

The singleplayer campaign is timed as follows:

- Timing begins on the tick the player gains control at the start of Container Ride,
  on the `camera_intro.TeleportToView` entity input.
- Alternatively, Vault Save may be used. In this case, timing starts on the
  `@glados.RunScriptCode(GladosRelaxationVaultPowerUp())` entity input with an
  offset of 18980 ticks.
- Alternatively, Container Ride Save may be used. In this case, timing starts on the
  `camera_1.TeleportPlayerToProxy` entity input with an offset of 16868 ticks.
- Timing ends on the tick the player shoots the moon in Finale 4, on the
  `@glados.RunScriptCode(BBPortalPlaced())` entity input.
- Dying during the end cutscene is allowed since the run is over.

The cooperative campaign is timed as follows:

- Each level begins timing when the `ss_force_primary_fullscreen` command is first
  executed after `stop_transition_videos_fadeout`.
- Each level ends timing when the `playvideo_end_level_transition` command is executed.
- Timing for the run begins when the players are teleported to the droppers, on the
  `teleport_start.Enable` entity input.
- Timing for runs ending in Course 5 ends when the cutscene starts playing, on
  the `vault-movie_outro.PlayMovieForAllPlayers` entity input.
- Timing for runs ending in Course 6 ends when the cutscene starts playing, on
  the `movie_outro.PlayMovieForAllPlayers` entity input.

Unless otherwise specified, partial campaign runs (e.g. chapter runs) are timed as a
subset of the relevant campaign, so e.g. Chapter 9 runs begin timing as soon as the
player loads into Finale 1 and end timing when the player shoots the moon.
