# About
This repository is a *prometheus* instrumentation playground for *python*. It is inteded to be used in conjunction with [asobiba-prometheus-config](https://github.com/soma-kurisu/asobiba-prometheus-config), a playground for all things configuration in the prometheus ecosystem.

## Sampling
To get some metrics, you need to run the sample application you are playing with and hit it's endpoint. For instance for [Scenario 1: hello prometheus](#Scenario-1:-hello-prometheus) following command will do the trick:

```Shell
for i in {1..1000}; do curl http://localhost:8001; sleep $((RANDOM % 10)); done
```

## Scenario 1: hello prometheus
Contains basic examples of how to use the prometheus client library to instrument a python application with metrics. 

In [offset and @ modifiers](#offset-and-@-modifiers) I look at how to use the `@` modifier to offset the time of a metric. Start() and end() are used in conjunction with range vectors for this purpose. For another basic *PromQL* example targeting these types of modifiers see [asobiba-prometheus-config/queries](https://github.com/soma-kurisu/asobiba-prometheus-config/queries/02-offset-and-at-modifiers.md)

### offset and @ modifiers

- https://prometheus.io/docs/prometheus/latest/querying/basics/#modifier

`start()` and `end()` can be used as values for the `@` modifier as special values.

For a range query, they resolve to the start and end of the range query respectively and remain the same for all steps.

- https://prometheus.io/blog/2021/02/18/introducing-the-@-modifier/

Following query plots the `1m` `rate` of `hello_world`-metrics of those series whose `last` `1h` `rate` was among the `top 5`.

Compare result vectors and graphs of (1) `start()`-anchored (2)`end()`-anchored and (3) non-anchored range queries.
```C
// (1) start()-anchored
rate({
  __name__=~"(hello_world.*(s_total|bucket)|prometheus_http_requests_total)", 
  __name__!~".*exception.*", 
  le=~"(|.Inf)"
}[1m])
  and
topk(5, 
  rate({
    __name__=~"(hello_world.*(s_total|bucket)|prometheus_http_requests_total)", 
    __name__!~".*exception.*", 
    le=~"(|.Inf)"
  }[1h] @ start())
)
```

```C
// (2) end()-anchored
rate({
  __name__=~"(hello_world.*(s_total|bucket)|prometheus_http_requests_total)", 
  __name__!~".*exception.*", 
  le=~"(|.Inf)"
}[1m])
  and
topk(5, 
  rate({
    __name__=~"(hello_world.*(s_total|bucket)|prometheus_http_requests_total)", 
    __name__!~".*exception.*", 
    le=~"(|.Inf)"
  }[1h] @ end())
)
```

```C
// (3) non-anchored
rate({
  __name__=~"(hello_world.*(s_total|bucket)|prometheus_http_requests_total)", 
  __name__!~".*exception.*", 
  le=~"(|.Inf)"
}[1m])
  and
topk(5, 
  rate({
    __name__=~"(hello_world.*(s_total|bucket)|prometheus_http_requests_total)", 
    __name__!~".*exception.*", 
    le=~"(|.Inf)"
  }[1h])
)
```