set shell := ["cmd.exe", "/c"]

@setup:
  uv sync

@report LAB:
  typst compile ./src/{{LAB}}/report/report.typ --root .

@watch LAB:
  typst watch ./src/{{LAB}}/report/report.typ --root .

@open LAB:
  @just report {{LAB}}
  start ./src/{{LAB}}/report/report.pdf

@notebook_to_script FILE:
  jupyter nbconvert --to python {{FILE}}

@archive:
  @just report lab1
  git archive -o labs.zip HEAD

@stream:
  echo "start streaming"
  ssh plancha@192.168.1.7 -t /usr/bin/nc -lk 9999