### debugging in docker

I added the following to the `docker-compose-override`:
```
    stdin_open: true
    tty: true
```

This will allow for the ability to attach to the container to debug
breakpoints.

`docker attach collect`

 and you will be placed in the debugger.

 ADDITIONS:
[ ]  separate years/months on months URL
[ ]  use tailwind
[ ]  select courses for each day, add #bags?
[ ]  add leaflet with animation of home to bandon and back

TABLES
* loops
    -- id, date, wage, bags, owner_id, group_id
* groups
    -- group_id, name
* people
    -- id, first_name, last_name, notes, lat, lon, group_id

SQLMODEL
* type-hint for the Base class, `id` is set by the DB on creation.

HTMX
what are the buttons that will be involved..
* form for adding a day of work
* form for creating a person/s and group
* button to list days of work, total OR by group OR by date 
* add a location to a player/person
* update a day of work EDIT
* go to leaflet map with all players located

