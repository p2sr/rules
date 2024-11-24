### Commands

<span style="color:#ff8888;font-weight:bold;">
IF YOU ARE UNSURE WHETHER A COMMAND IS ALLOWED, CHECK WITH A MODERATOR FOR YOUR
CATEGORY BEFORE USING IT.
</span>

The game contains a wide array of commands and variables (cvars) which can be used to
achieve various effects. Commands are banned or allowed considering several criteria.
All commands accessible in normal gameplay (e.g. common movement commands, save/load)
are allowed. Other commands receive rulings based on their interaction with the rest
of the game, their similarity to other commands, and how they fit in with other rules.
If you're not sure whether a command is allowed, you should speak to a moderator for
the category you are running.

Allowed commands can be categorised as "action commands", "functional commands", and
"non-functional commands" (note that all action commands are also functional
commands). Any allowed command may be manually executed by typing it into the console
at any point, including executing such commands indirectly through `exec` or aliases.

#### HUDs

SAR and the game itself provide various HUDs to the user, accessible through console
commands. In general, a HUD provided by SAR is allowed only if there is an equivalent
HUD allowed which the base game provides. The command list below exhaustively lists
all known allowed HUDs.

HUDs containing unchanging, predetermined user-provided text or content - such as
through `sar_hud_set_text` or `sar_toast_create` - are always allowed, even if they
are giving information about the run, such as dialogue fades or lineups.

#### Graphics

Most commands affecting the game's graphics are allowed to be used, and are not
classed as functional commands. This is because using these commands is sometimes
required for good performance on lower-end hardware. This includes most commands
starting `r_` provided they do not make parts of the world invisible or cause other
major differences to default behaviour.

#### Crosshairs

The game's default crosshair size (including quickhud) has a fixed pixel size.
Custom crosshairs via `sar_crosshair` and `sar_quickhud` are permitted only with
specific assets and parameters, to get a crosshair equivalent to the default on
a different resolution. The crosshair used must not change throughout the run.
If you wish to use a custom crosshair, ask a moderator for your category for an
allowed configuration.

#### Command List

This list details the allowed values for every SAR command as well as a lot of base
game commands. Please note that any category can override any of these rulings.
An allowed value of `-` means that any value is permitted.

{{COMMAND_LIST}}
