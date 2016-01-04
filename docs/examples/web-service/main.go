package main

import (
	"fmt"
	"net/http"

	metrics "github.com/rcrowley/go-metrics"
)

var (
	m metrics.Meter
)

func rootHandler(w http.ResponseWriter, r *http.Request) {
	m.Mark(1)
	w.Write([]byte("Hello World!"))
}

func metricsHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "%.0f", m.Rate1())
}

func init() {
	m = metrics.NewMeter()
	metrics.Register("requests", m)
}

func main() {
	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/status/metrics/", metricsHandler)
	http.ListenAndServe(":8080", nil)
}
