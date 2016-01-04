Example Web Application
=======================

This example shows a simple web application written in Go that exposes the number of requests per second (averaged over the last minute) via a simple metrics endpoint.

The `http` trigger is used in combination with the metrics endpoint to implement scaling based on the average number of requests being handled per second by each individual instance.
