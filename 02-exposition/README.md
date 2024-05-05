selfhosted expositioning of metrics to prometheus 
- apart start_http_server
- focus on
    - Web Server Gateway Interface (WSGI)
    - Twisted event-driven network engine
    - Multiprocess with Gunicorn
        setup before running Gunicorn:
        - set environment variable called prometheus_multiproc_dir pointing to empty directory which client lib  uses to track metrics. clean this folder before each application restart to handle potential changes in instrumentation.
        > export prometheus_multiproc_dir=$PWD/multiproc
        > rm -rf $prometheus_multiproc_dir
        > mkdir -p $prometheus_multiproc_dir
        > gunicorn -w 2 -c config.py app:app