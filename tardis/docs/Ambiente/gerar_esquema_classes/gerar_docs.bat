md docs
sphinx-apidoc -H Tardis -A Luis -V 1.0.0 -d 5 -l -F -P -f -o docs\ src\
copy conf_default.py docs\conf.py  /y
docs\make html

