// plotly chart
function plot(rows) {

  // function unpack(rows, key) {
  // return rows.map(function(row) { return row[key]; });
  // // return rows[key];
  // }

var trace1 = {
  type: "scatter",
  mode: "lines+markers",
  name: 'dollar',
  // x: unpack(rows, 'Transaction_Date'),
  // y: unpack(rows, 'sum'),
  x: Object.keys(rows['Transaction Amount']),
  y: Object.values(rows['Transaction Amount']),
  line: {color: '#17BECF'}
}

var trace2 = {
  type: "bar",
  yaxis: 'y2',
  mode: "lines",
  name: 'quant',
  // x: unpack(rows, 'Transaction_Date'),
  // y: unpack(rows, 'mean'),
  x: Object.keys(rows['Transaction Amount']),
  y: Object.values(rows['Quantity ']),
  line: {color: '#7F7F7F'}
}

var data = [trace1,trace2];
var maxY = Math.max(...Object.values(rows['Transaction Amount']));
console.log('maxY:');
console.log(maxY);

var datesapn = [Object.keys(rows['Transaction Amount'])[0] , Object.keys(rows['Transaction Amount'])[rows.length - 1] ]
    
var layout = {
  // title: 'Time Series with Rangeslider', 
  xaxis: {
    autorange: true, 
    range: datesapn, 
    rangeselector: {buttons: [
        {
          count: 1, 
          label: '1m', 
          step: 'month', 
          stepmode: 'backward'
        }, 
        {
          count: 6, 
          label: '6m', 
          step: 'month', 
          stepmode: 'backward'
        }, 
        {step: 'all'}
      ]}, 
    rangeslider: {range: datesapn}, 
    type: 'date',
    rangemode: "tozero",
  }, 
  yaxis: {
    // autorange: true, 
    // range: [0, maxY], 
    type: 'linear',
    overlaying:'y2',
    anchor: 'x',
    rangemode: "tozero"
  },
  yaxis2: {
    title: '(quant)',
    titlefont: {color: 'rgb(148, 103, 189)'},
    tickfont: {color: 'rgb(148, 103, 189)'},
    // overlaying: 'y',
    side: 'right',
    anchor:'x',
    
    // overlaying: 'y',
  }
};

Plotly.newPlot('myDiv', data, layout);
}



//
//  ------------------
//
// Ulity
// --------------
//
function set_select_daterange_handle() {
    $('select')[0].selectedIndex = 0;

    $('select').on('change', function() {
        $.ajax({
            type: "GET",
            url: "/?freq=" + this.value,
            dataType: "json",
            success: function(data) {
                console.log(data)
                plot(data)
            },
            error: function() {
                alert('There was an error')
            }
        })

    })
    $('input[name="daterange"]').daterangepicker();
    $('input[name="daterange2"]').daterangepicker();

    //     $('input[name="daterange"]').daterangepicker({
    //   minDate: moment().subtract(2, 'years')
    // }, function (startDate, endDate, period) {
    //   $(this).val(startDate.format('L') + ' – ' + endDate.format('L'))
    // });
    $('input[name="daterange"]').on('apply.daterangepicker', function(ev, picker) {
        console.log("----");
        // console.log(picker.startDate.format('YYYY-MM-DD'));
        // console.log(picker.endDate.format('YYYY-MM-DD'));
        var start = picker.startDate.format('YYYY-MM-DD');
        var end = picker.endDate.format('YYYY-MM-DD');
        console.log("start");

        console.log(start);
        console.log(end);

        $.ajax({
            type: "GET",
            url: "/getReturned?start=" + start + "&end=" + end,
            dataType: "json",
            success: function(data) {
                console.log(data);
                $('#div2').html(data);
                $('#div2 table').DataTable();
            },
            error: function() {
                alert('There was an error')
            }
        })


    });

};