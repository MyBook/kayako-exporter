===============
kayako exporter
===============

::

    Usage: kayako_exporter [OPTIONS]

      Kayako metrics exporter for Prometheus

    Options:
      --port INTEGER        Port to serve prometheus stats [default: 9223]
      --url TEXT            HTTP URL for Kayako instance
      --login TEXT          Kayako username
      --password TEXT       Kayako password
      --p TEXT              Kayako password
      --department-id TEXT  Kayako department to monitor [default: all available]
      --verbose
      --version
      --help                Show this message and exit.



Deploying with Docker
---------------------
::

    docker run -d --env=KAYAKO_URL="https://kayako.example.com/" --env="KAYAKO_LOGIN=username" --env="KAYAKO_PASSWORD=secret" mybook/kayako-exporter
