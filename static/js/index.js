let setValueCloseGlobal = 0


function renderChart(data) {

    const ctx = document.getElementById("myChart");
    let contx = ctx.getContext("2d")

    // let labels = Object.keys(data.stock_prices);
    let labels = data.dates;
    console.log('here')

    let stockPrices = Object.values(data.stock_prices);

    if (stockPrices.length > labels.length) {
        labels = Object.keys(data.stock_prices);
    }


    let datasets = [
        {
            label: "Stock Price",
            yAxisID: "A",
            borderColor: "#36a2eb",
            data: stockPrices,
            tension: 0,
            tension: 0,
            borderWidth: 1,
            backgroundColor: createGradient(contx, '#36a2eb'),
        },
    ];

    const axes = {};
    const nAxisPoints = 8;

    const config = {
        type: "line",
        data: {
            labels: labels,
            datasets: datasets,
        },
        options: {
            animation: false,
            maintainAspectRatio: false,
            tooltips: {
                mode: "index",
            },
            legend: {
                labels: {
                    fontColor: "#ffffff",
                }
            },
            scales: {
                xAxes: [
                    {
                        ticks: {
                            fontColor: "white",
                        },
                    }],
                yAxes: [{
                    id: "A",
                    type: "linear",
                    position: "right",
                    ticks: {
                        fontColor: "white",
                    },
                    scaleLabel: {
                        display: true,
                        labelString: "Stock Price",
                        fontColor: "#36a2eb",
                    },
                }, ...Object.values(axes)],
            },
        },
    };

}

function formatIndexValues(values) {
    return values.map(({ date, open, high, low, close }) => {
      var offset = new Date(date).getTimezoneOffset()*60;
      return {
        date: date,
        x: new Date(date).getTime()-offset,
        y: [open.toFixed(2), high.toFixed(2), low.toFixed(2), close.toFixed(2)]
      }
    }) 
  }

  function findMinMax(values) {
    let yMin = Number.MAX_VALUE
    let yMax = Number.MIN_VALUE
  
    values.forEach(({ y }) => {
      yMin = Math.min(yMin, y[0])
      yMin = Math.min(yMin, y[1])
      yMin = Math.min(yMin, y[2])
      yMin = Math.min(yMin, y[3])
  
      yMax = Math.max(yMax, y[0])
      yMax = Math.max(yMax, y[1])
      yMax = Math.max(yMax, y[2])
      yMax = Math.max(yMax, y[3])
    })
  
    return { yMin, yMax }
  }


// render chart
async function renderIndexChart(title, values, prev_day_close, current_price, typeDate, isFirstLoad) {
    // let value = b.close - a.close;
    let value = current_price - prev_day_close;
    // let change = ((b.close /prev_day_close) -1) * 100;
    if (typeDate === "daily") setValueCloseGlobal = values[values.length - 1]?.close?.toFixed(2)
    let change = (setValueCloseGlobal - values[0]?.close?.toFixed(2)) / values[0]?.close?.toFixed(2) * 100
    var closeColor = null;
    //creating the percentage changed text and css
    if (values.length <= 0) {
        closeColor = "#00a449";
        subtitleText = `0 (0%)`;
    } else {
        if (parseFloat(change) > 0) {
            closeColor = "#00a449";
            subtitleText = `${(setValueCloseGlobal - values[0]?.close?.toFixed(2)).toFixed(2)} (${change.toFixed(2) ? change.toFixed(2) : 0}%)`;
        } else {
            closeColor = "#fb5058";
            subtitleText = `${(setValueCloseGlobal - values[0]?.close?.toFixed(2)).toFixed(2)} (${change.toFixed(2) ? change.toFixed(2) : 0}%)`;
        }
    }
    values = formatIndexValues(values);

    const { yMin, yMax } = findMinMax(values);
    let minTimestamp;
    let maxTimestamp;

    if (typeDate === 'monthly') {
        // years
        minTimestamp = getTimestampForTime(values[0].date, 0, 0);
        maxTimestamp = getTimestampForTime(values[values.length - 1].date, 23, 59);
    } else if (typeDate === 'weekly') {
        // 2 years
        const uniqueYears = [...new Set(values.map((item) => item.date.substring(0, 4)))];
        if (uniqueYears.length >= 2) {
            minTimestamp = getTimestampForTime(`${uniqueYears[0]}-01-01`, 0, 0);
            maxTimestamp = getTimestampForTime(`${uniqueYears[uniqueYears.length - 1]}-12-31`, 23, 59);
        } else {
            minTimestamp = getTimestampForTime(`${uniqueYears[0]}-01-01`, 0, 0);
            maxTimestamp = getTimestampForTime(`${uniqueYears[0]}-12-31`, 23, 59);
        }
    } else if (typeDate === 'daily') {
        // last 12 month
        const uniqueYears = [...new Set(values.map((item) => item.date.substring(0, 4)))];
        minTimestamp = getTimestampForTime(`${uniqueYears[0]}-01-01`, 0, 0);
        maxTimestamp = getTimestampForTime(`${uniqueYears[0]}-12-31`, 23, 59);
    } else if (typeDate === 'intraday') {
        // showing today
        const today = new Date();
        const formattedToday = today.toISOString().substring(0, 10);
        minTimestamp = getTimestampForTime(formattedToday, 8, 30);
        maxTimestamp = getTimestampForTime(formattedToday, 17, 0);
    }

    let switching_ = false;


    let dataFilterCandle = [
        {
            name: title,
            type: 'candlestick',
            data: values,
        },
    ]

    let yAxisChart = [
        {
            axisTicks: {
                show: true,
            },
            axisBorder: {
                show: true,
                color: 'white'
            },
            labels: {
                style: {
                    colors: 'white',
                }
            },
            tooltip: {
                enabled: true,
                shared: true,
            },
            min: yMin,
            max: yMax,
        }
    ]

    const nAxisPoints = 8;


    var options = {
        annotations: {
            yaxis: [{
                y: current_price?.toFixed(2),
                strokeDashArray: 5,
                borderColor: 'transparent',
                fillColor: 'transparent',
                opacity: 0,
                offsetX: -10,
                offsetY: -3,
                width: '120%',
                label: {
                    borderColor: '#c2c2c2',
                    borderWidth: 1,
                    borderRadius: 2,
                    text: current_price?.toFixed(2),
                    textAnchor: 'start',
                    position: 'left',
                    offsetX: 0,
                    offsetY: 0,
                    style: {
                        background: '#f3c736',
                        color: '#000',
                        fontWeight: 600,
                        fontSize: "12px",
                        padding: {
                            left: 1,
                            right: 3,
                            top: 2,
                            bottom: 2,
                        }
                    },
                },
            },
                //   {
                //     y: 50,
                //     strokeDashArray: 5,
                //     borderColor: '#9d0a0c',
                //     fillColor: '#9d0a0c',
                //     opacity: 0.3,
                //     offsetX: 0,
                //     offsetY: -3,
                //     width: '120%',

                // }
            ],
        },
        series: dataFilterCandle,
        grid: {
            borderColor: "rgba(255, 255, 255, 0.25)",
            strokeDashArray: 6,
            xaxis: {
                lines: {
                    show: true,
                },
            },
            yaxis: {
                lines: {
                    show: true,
                },
            },
        },
        chart: {
            type: 'line',
            height: 500,
            width: "097%"
        },
        title: {
            text: title,
            align: 'left',
            style: {
                color: "#929cb3",
                fontSize: "20px",
                fontWeight: 700
            }
        },
        xaxis: {
            min: minTimestamp,
            max: maxTimestamp,
            labels: {
                style: {
                    cssClass: "white-label",
                    colors: "#929cb3"
                }
            },
            axisTicks: {
                show: true,
                borderType: 'solid',
                color: '#78909C',
                height: 6,
                offsetX: 0,
                offsetY: 0
            },
            type: "datetime",
            title: {
                // text: date,
                offsetX: 150,
                offsetY: -250,
                style: {
                    color: undefined,
                    fontSize: '14px',
                    fontFamily: '"Inter", sans-serif !important',
                    fontWeight: 600,
                    cssClass: 'apexcharts-xaxis-title',
                    color: "#929cb3"
                },
            }
        },
        yaxis: yAxisChart,
        legend: {
            labels: {
                colors: ['transparent', '#fff', '#fff'],
            },
            markers: {
                fillColors: ['transparent', '#333', '#333'], // 'transparent' hides the legend marker for Series 3
            },
        },
        tooltip: {
            enabled: true,
            theme: "dark",
            shared: true,
            enabledOnSeries: [0, 1, 2],
            style: {
                fontFamily: "Inter",
            },
            x: {
                show: false
            }
        },
        subtitle: {
            text: subtitleText,
            align: 'left',
            floating: false,
            style: {
                fontSize: '18px',
                fontWeight: '600',
                fontFamily: '"Inter", sans-serif !important',
                color: closeColor,
                cssClass: "candlestickSubtitle",
            }
        },
        stroke: {
            width: [1.25, 0.5]
        },
        // markers: {
        //   size: 5, 
        //   strokeWidth: 0,
        //   fillOpacity: 1,
        //   hover: {
        //     size: 7 
        //   }
        // },
    };


    // Create a new chart container
    var newChartContainer = document.createElement('div');
    newChartContainer.id = 'chart-candle';
    document.querySelector(`#index-chart-container-candle`).appendChild(newChartContainer);

    // Create a new chart
    var chart = await new ApexCharts(newChartContainer, options);
    await chart.render();

    // Show the chart container
    document.getElementById(`index-chart-container-candle`).classList.remove('index-chart-hidden');

    if (!isFirstLoad) {
        $("#chart-candle").show();
    }

    if (switching_) {
        chart.update();
    }

}





document.addEventListener("DOMContentLoaded", function(event) {
    symbol = "nepse";
const url = `http://localhost:8000/api/v1/stock_data?ticker=${symbol}`;

fetch(url)
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Assuming the response contains JSON data
        return response.json();
    })
    .then(data => {
        console.log(data)

        renderIndexChart(symbol.toUpperCase(),
        data,
        data[data.length-2]?.close,
        data[data.length-1]?.close,
        data,
        false)
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });


});
