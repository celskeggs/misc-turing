python toascii.py test.mach >test2.mach && python compile.py test2.mach >test2.asm && nasm -f elf32 test2.asm -ggdb && gcc -O3 compile-host.c test2.o -o test2 -m32 -ggdb && echo done
