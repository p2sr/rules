### Scripting

Any time a key is pressed or released, an arbitrary amount of allowed commands may be
executed. These may include up to one action command. Any functional commands in the
sequence must be executed without delay. For other commands, delay is permitted, e.g.
through SAR's `hwait` command. Note that scrolling the mouse wheel a single tick
counts as pressing and immediately releasing the "key" of the mouse wheel.

Automation of commands may be achieved through mechanisms like the `sar_on_load`
command. This is limited to non-functional commands during the run; however, note
that in Challenge Mode, automatically running functional commands is allowed provided
the command could have been performed manually prior to the run with the same effect.
Examples of this include changing `sensitivity` or `mat_fullbright`.
