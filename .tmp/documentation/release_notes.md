# Release Notes

## v0.4.0 (Pending)
## Changes
- Removed messaging.records from the public API (`N/A`).
- Removed Record.queue_name attribute (`N/A`).

## v0.3.0 (2017-07-04)
##### Features
- Added room list watcher component.
- Added download bot component.

## v0.2.0 (2017-05-15)
##### Changes
- Changed morpha package name to "clare".

##### Fixes
- Fixed parsing Pokemon log messages with multiple details (`ME-647`).
- Fixed parsing null log messages (`ME-648`).

##### Features
- Added Scraper (`ME-637`).
- Added logging Event (`ME-637`).
- Added messaging Broker (`ME-659`).
- Added retry PolicyBuilder (`ME-659`).
- Added stopping after a number of attempt (`ME-659`).
- Added stopping after a duration (`ME-659`).
- Added stopping after never (`ME-659`).
- Added stopping after multiple conditions (`ME-659`).
- Added waiting for fixed duration (`ME-659`).
- Added continuing on exceptions (`ME-659`).
- Added continuing on results (`ME-659`).
- Added event-driven hooks (`ME-659`).

## v0.1.0 (2017-04-20)
##### Features
- Added logging.
- Added BattleMetricsService with damage dealt metric (`ME-630`).
- Added Battle, Player, and Pokemon (`ME-630`).
- Added BattleLog (`ME-630`).
- Added IRecord and concrete Record (`ME-630`).
