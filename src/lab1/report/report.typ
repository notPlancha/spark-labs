#import "@preview/callisto:0.2.4"
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.8": *
#show: codly-init.with()
#codly(
  languages: (
    // python: (name: [#h(-0.3em)], icon: codly-languages.python.icon),
    python: codly-languages.python,
    sh: codly-languages.sh,
    yaml: codly-languages.yaml,
    Dockerfile: codly-languages.dockerfile,
  ),
  zebra-fill: none,
  fill: luma(95%),
  stroke: 1pt + luma(95%),
  header-cell-args: (align: center, fill: white),
  number-placement: "outside"
)

#show raw.where(lang:"txt"): set text(size: 0.8em)
#show raw.where(lang:"txt"): local.with(display-name: false, display-icon: false, zebra-fill: luma(98%))
#show heading.where(level: 1): set text(size: 40pt)
= Starting the Cluster

#codly(header: [Dockerfile on the server])
```Dockerfile
FROM apache/spark:4.0.1
# switch to root to install packages
USER root
RUN pip install --no-cache-dir "pandas==2.3.2" "pyarrow==21.0.0"
# switch back to spark user
USER spark
```

#codly(header: [compose.yaml on the server])
```yaml
services:
  spark:
    build: .
    hostname: apache-spark
    ports:
      - "7077:7077"    # Spark master port
      - "8080:8080"    # Spark master web UI
      - "8081:8081"    # Spark worker web UI
      - "15002:15002"  # Spark Connect server port
      - "4040:4040"    # Spark Connect web UI
    command: >
      bash -c "/opt/spark/sbin/start-master.sh;
              /opt/spark/sbin/start-connect-server.sh;
              /opt/spark/sbin/start-worker.sh spark://192.168.1.7:7077;
              sleep infinity"
```


```sh
$ ls
compose.yaml  Dockerfile
$ docker compose up -d
[+] Running 1/1
 ✔ Container spark-docker-spark-1  Started                                                                     0.5s
```

// callisto templates are hard to change for now

#pagebreak()

= Task 1
#callisto.render(nb: json("/src/lab1/task1.ipynb"))

#pagebreak()

= Task 2
#callisto.render(nb: json("/src/lab1/task2.ipynb"))
