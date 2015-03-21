_Ewo_ is a tool written in Python for the [Gentoo GNU/Linux](http://www.gentoo.org) distribution to optimize the recompilation of the whole system, all installed packages.

Usually one can simply use `emerge -e world` and `emerge --resume` when something bad happens, but sometimes you need to run another emerge process to solve a problem and this alter the desired `emerge --resume` behavior. _Ewo_ solves this issue and it can be used in general to compile all the packages that have not been updated or replaced after a specific date (CFLAGS, LDFLAGS change, compiler upgrade and so on).
Using a config file named `package.skip` the user can avoid useless packages reinstallation, like large binary packages for example.

Take a look at `ewo --help` before use it or read BasicHelp