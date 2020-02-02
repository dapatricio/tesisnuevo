! function(s) {
  "use strict";
  var a = function() {
    this.$body = s("body"), this.charts = []
  };

  a.prototype.respChart = function(e, r, t, o) {
    var n = e.get(0).getContext("2d"),
      i = s(e).parent();
    return function() {
      var a;

      switch (e.attr("width", s(i).width()), r) {
        case "Bar":
          a = new Chart(n, {
            type: "bar",
            data: t,
            options: o
          });
          break;
        case "Line":
          a = new Chart(n, {
            type: "line",
            data: t,
            options: o
          });
          break;
      }
      console.log(a);
      return a
    }()
  }, a.prototype.initCharts = function() {
    var a = [];

    if (0 < s("#bar-chart-example").length) {
      a.push(this.respChart(s("#bar-chart-example"), "Bar", {
        labels: labels,
        datasets: [{
          label: "Respuesta " + user,
          backgroundColor: "#4a81d4",
          borderColor: "#4a81d4",
          hoverBackgroundColor: "#4a81d4",
          hoverBorderColor: "#4a81d4",
          data: rp
        }, {
          label: "Nivel Recomendado",
          backgroundColor: "#f1556c",
          borderColor: "#e3eaef",
          hoverBackgroundColor: "#e3eaef",
          hoverBorderColor: "#e3eaef",
          data: rr
        }]
      }, {

        scales: {
          yAxes: [{
            gridLines: {
              display: !1
            },
            stacked: !1,
            ticks: {
              stepSize: 1
            }
          }],
          xAxes: [{
            barPercentage: .8,
            categoryPercentage: .5,
            stacked: !1,
            gridLines: {
              color: "rgba(0,0,0,0.01)"
            }
          }]
        }
      }))
    }
    if (0 < s("#line-chart-example").length) {
      a.push(this.respChart(s("#line-chart-example"), "Line", {
        labels: labels,
        datasets: [{
          label: "Respuesta " + user,
          backgroundColor: "rgba(26, 128, 156, 0.3)",
          borderColor: "#1abc9c",
          data: rp
        }, {
          label: "Promedio Area Academica",
          fill: !0,
          backgroundColor: "transparent",
          borderColor: "#f1556c",

          data: ra
        }]
      }, {


        tooltips: {
          intersect: !1
        },
        hover: {
          intersect: !0
        },
        plugins: {
          filler: {
            propagate: !1
          }
        },
        scales: {
          xAxes: [{
            reverse: !0,
            gridLines: {
              color: "rgba(0,0,0,0.05)"
            }
          }],
          yAxes: [{
            ticks: {
              stepSize: 1
            },
            display: !0,

            gridLines: {
              color: "rgba(0,0,0,0)",
              fontColor: "#fff"
            }
          }]
        }
      }))

  }
  return a
}, a.prototype.init = function() {
  var e = this;
  Chart.defaults.global.defaultFontFamily = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif',
    e.charts = this.initCharts(),
    s(window).on("resize", function(a) {
      s.each(e.charts, function(a, e) {
        try {
          e.destroy()
        } catch (a) {}
      }), e.charts = e.initCharts()
    })
}, s.Dashboard3 = new a, s.Dashboard3.Constructor = a
}(window.jQuery),
function(a) {
  "use strict";
  window.jQuery.Dashboard3.init()
}();
