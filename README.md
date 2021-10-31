![test](logo-gray.svg)

# BeCauSe
## The Basic like, Compiled, Stack based language

B basic like<br />
C Compiled<br />
S Simple

Its like forth, its like basic, it has modern syntax. what alse would you ask from a language?

---

## Install
Currently, BeCauSe can only be installed on Linux operating systems due to the fact it uses Nasm and other commands that are only availabe on Linux.

To install BeCauSe, make sure to have ./bcs.py in your path

---

## Quick start
Interpreting
```console
$ python3 ./bcs.py run examples/e006_while_loops.bcs
```

Compiling
```console
$ python3 ./bcs.py com examples/e006_while_loops.bcs
$ ./output
```

Keeping the generated assembly
```console
$ python3 ./bcs.py com examples/e006_while_loops.bcs debug
$ cat ./output.asm
```