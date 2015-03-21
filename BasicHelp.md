
```
EWO - Emerge (-e) World Optimizer (v0.4)

Usage: ewo [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -s TOUCH_FROMDATE, --setstart=TOUCH_FROMDATE
                        set the starting point (possible values are 'NOW' or a
                        genlop-style date like 'Mon Jun 05 11:09:37 2007')
  -P, --purgestart      remove the previously set starting point
  -v, --showstart       show the already set starting point
  -f, --fetchonly       use the --fetchonly option in the emerge command
  -i, --ignore-smartworld
                        sometimes could be useful to ignore smartworld cache
                        (e.g. when some 'fetch restricted' files are removed
                        since last ewo run)
  -o, --problematic-only
                        this option should be used *before* running ewo in
                        'exec-mode' to avoid problems related with interactive
                        and fetch restricted ebuilds and to fully support
                        multiple emerge jobs (interactive force --jobs=1)
  -m MODE, --mode=MODE  using mode 'exec' an 'emerge -1 [...]' will start
                        automatically; using 'pretend' ewo simply shows the
                        todo packages list on the stdout and using 'emerge-
                        pretend' (Default) the output of 'emerge -1vp [...] |
                        less' will be shown.The 'cleaner' mode removes files
                        related with the already-done ebuilds.
```