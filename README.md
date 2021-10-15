# BeCauSe
## The Basic like, Compiled, Stackbased language

B basic like<br />
C Compiled<br />
S Simple

Its like forth, its like basic, it has modern syntax. what alse would you ask from a language?

---

## Install
Currently, BeCauSe can only be installed on Linux operating systems due to the fact it uses Nasm and other commands that are only availabe on Linux.

To install BeCauSe, make sure to have ./bcs.py in your path<br />Also make sure to install NASM

---

## Quick start
Interpreting
```console
$ ./bcs.py run examples/adding.sbsc
```

Compiling
```console
$ ./bcs.py com examples/adding.sbsc
$ ./output
```

Keeping the generated assembly
```console
$ ./bcs.py com examples/adding.sbsc debug
$ cat ./output.asm
```
