stretch
=======

[![Build Status](https://travis-ci.org/paddycarey/stretch.svg?branch=master)](https://travis-ci.org/paddycarey/stretch)

Dead simple autoscaling for Marathon.

- Zero configuration (applications define their own configuration)
- Application agnostic (works with any language/stack/application type)

Users can configure each application with a unique set of triggers and thresholds for scaling when deploying. stretch includes a number of built-in triggers (CPU, RAM, HTTP) that are ready to use, but if required it is possible to add completely custom triggers.

**WARNING:** stretch is currently pre-alpha quality, use in production at your own risk.


## How it works

```python
#!/usr/bin/env pseudocode

while True:
    for app in marathon.list_applications():
        if not app.configured:
            continue
        result = app.check_triggers()
        if result == SCALE_UP:
            app.scale_up()
        elif result == SCALE_DOWN:
            app.scale_down()
    sleep(30)
```

stretch fetches a list of all deployed applications using the Marathon API. The list of applications is parsed and those without valid autoscaling configurations are discarded.

For each configured application, stretch checks the configured triggers, aggregating the results of all triggers to make a single decision or whether to scale an application up/down or to do nothing.

stretch repeats this process (with a configurable delay between runs) until stopped.


## Triggers

Triggers are fundamental to how stretch operates. Triggers are configured on a per application basis and return a scale-up/scale-down/do-nothing response. Triggers define the configuration values that they require, each type can require extra values as needed.

stretch will scale an application up if any one of its triggers returns a `SCALE_UP` response, but will only scale an application down if **all** triggers return `SCALE_DOWN` responses.

Built-in triggers include:

- **CPU Usage:** Per-task CPU usage (system time (in secs) + user time (in secs)).
- **Memory Usage:** Per-task Memory usage (percentage total usage).
- **HTTP Threshold:** Retrieve a float value via HTTP from each instance and averages them.
- **HTTP Single Value Threshold:** Retrieve a float value via HTTP from a single URL.

All current built-in triggers can be configured with upper/lower thresholds which control when scaling is triggered. Custom triggers do not have to use the threshold mechanic.

TODO/potential triggers

- **Datadog:** Retrieve metrics/values from the datadog API.
- **New Relic:** Retrieve application statistics from New Relic.
- **Redis:** Trigger scaling based on the result of a user defined Redis command.
- **SQL:** Trigger scaling based on the result of a user defined SQL statement.
- **HAProxy:** Set upper/lower thresholds based on requests/second.

Full configuration details for built in triggers follows below.


## Configuration

An application defines its own autoscaling configuration using Marathon labels at deploy time. If the required labels are not defined the application will be ignored and not considered for scaling.

### Application-level configuration

- **SCALING_FACTOR:** *(float: default 1.5)* The multiplier that is used when calculating the new number of instances required for a scaling operation.
- **SCALING_MIN_INSTANCES:** *(int: default current instances)* The minimum number of instances that the application should never be scaled below. **Note:** Using the current instance count as the default value when not set means that this application will only ever be scaled up, not down.
- **SCALING_MAX_INSTANCES:** *(int: default current instances)* The maximum number of instances that the application should never be scaled above. **Note:** Using the current instance count as the default value when not set means that this application will only ever be scaled down, not up.

### Trigger-specific configuration

When configuring triggers, a common prefix is used to group all configuration for each single trigger. Prefixes should take the form `r'^SCALING_TRIGGER_[0-9]+'`. The numbers (`[0-9]+`) used are irrelevant, but should be unique for each specific trigger being configured per application, e.g.:

```json
"labels": {
    ...
    "SCALING_TRIGGER_00_TYPE": "mem",
    "SCALING_TRIGGER_00_LOWER_THRESHOLD": "20",
    "SCALING_TRIGGER_00_UPPER_THRESHOLD": "80",
    "SCALING_TRIGGER_01_TYPE": "http",
    "SCALING_TRIGGER_01_URL": "/metrics/requests-per-second",
    "SCALING_TRIGGER_01_LOWER_THRESHOLD": "250",
    "SCALING_TRIGGER_01_UPPER_THRESHOLD": "1000",
    ...
}
```

For all sections below, the variable `$(TRIGGER_PREFIX)` is used to represent the per-trigger unique prefix.

#### Common configuration

- **$(TRIGGER_PREFIX)_TYPE:** *(string: required)* The trigger type is a required setting for all triggers. It controls which of the available trigger types is to be used. Depending on the type selected, additional configuration values may be required.

#### Trigger-specific configuration

##### CPU Usage Trigger `(cpu)`

Trigger scaling based on the total CPU time (system + user), averaged across all running instances.

- **$(TRIGGER_PREFIX)_LOWER_THRESHOLD:** *(float: required)* The lower bound for CPU usage (averaged across all instances). If the current value is less than this number the trigger will return a `SCALE_DOWN` result.
- **$(TRIGGER_PREFIX)_UPPER_THRESHOLD:** *(float: required)* The upper bound for CPU usage (averaged across all instances). If the current value is larger than this number the trigger will return a `SCALE_UP` result.

##### Memory Usage Trigger `(mem)`

Trigger scaling based on % total memory usage, averaged across all running instances.

- **$(TRIGGER_PREFIX)_LOWER_THRESHOLD:** *(float: required)* The lower bound for memory usage (% total usage, averaged across all instances). If the current value is less than this number the trigger will return a `SCALE_DOWN` result.
- **$(TRIGGER_PREFIX)_UPPER_THRESHOLD:** *(float: required)* The upper bound for memory usage (% total usage, averaged across all instances). If the current value is larger than this number the trigger will return a `SCALE_UP` result.

##### HTTP Trigger `(http)`

Retrieve a single float value from a HTTP endpoint on each running instance. Trigger scaling based on the average of all values received from the instances.

- **$(TRIGGER_PREFIX)_URL:** *(string: required)* The URL on each instance that the current value should be fetched from. This URL should only include the path/query string portion e.g. `/status/jobs-in-queue?queue=batch`, including the host or domain will result in a misconfiguration error for the triger. The numbers returned from all instances will be averaged before use.
- **$(TRIGGER_PREFIX)_LOWER_THRESHOLD:** *(float: required)* If the current value is less than this number the trigger will return a `SCALE_DOWN` result.
- **$(TRIGGER_PREFIX)_UPPER_THRESHOLD:** *(float: required)* If the current value is larger than this number the trigger will return a `SCALE_UP` result.

##### HTTP Single Value Trigger `(http_single)`

Retrieve a single float value from one HTTP endpoint. Trigger scaling based on the value received.

- **$(TRIGGER_PREFIX)_URL:** *(string: required)* The URL that the current value should be fetched from. This URL should be absolute e.g. `http://www.example.com/metrics/requests-count?per=second`. Failure to use an absolute URL will result in a misconfiguration error for the triger.
- **$(TRIGGER_PREFIX)_LOWER_THRESHOLD:** *(float: required)* If the current value is less than this number the trigger will return a `SCALE_DOWN` result.
- **$(TRIGGER_PREFIX)_UPPER_THRESHOLD:** *(float: required)* If the current value is larger than this number the trigger will return a `SCALE_UP` result.


## TODO

stretch is a work in progress, and there is a lot of work remaining to be done. A non-exhaustive list might look something like:

- Tests, tests, tests, and more tests.
- Extensive documentation.
- Asynchronous/concurrent operation.
- More trigger types.
- Package and release to PyPI.
- Refactor to enable third-party plugins (triggers) from external packages.

If there are specific issues you'd like addressed or prioritised, please don't hesitate to file an issue.


## Copyright & License

- Copyright © 2016 Patrick Carey (https://github.com/paddycarey)
- Licensed under the **MIT** license.
