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
[ ]  use htmx, tailwind
[ ]  select courses for each day, add #bags?
[ ]  add leaflet with animation of home to bandon and back



