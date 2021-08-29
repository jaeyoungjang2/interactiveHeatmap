// login view setting
function multiplePush(colArray,repeat,color){
  for (var i = 0 ; i < repeat; i++) {
    colArray.push(color);
  }
}

function bar_paintImage(ids, readJson){
  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];

  multiplePush(bar_colors,readJson.data.test.length,barRed);
  multiplePush(bar_colors,readJson.data.control.length,barGray);

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;
    bar_x = readJson.data.feature_names;

    if(geneID && geneID == ids[0]){
      for (var value in readJson.data.nodes[key].information){
        if(value.startsWith('N_')){
          N_expression = readJson.data.nodes[key].information[value];
          bar_y.push(N_expression);
        }
      }
    }
  }

  barplot_data = [{x:bar_x, y:bar_y, type:'bar',
    marker:{color:bar_colors}}],
  layout = {
    title:barPlotTitle,
    yaxis: {
      title: barPlotYaxisTitle
    },
    width: barPlotWidth,
    height: barPlotHeight
  };
  Plotly.newPlot('barplot_myDiv', barplot_data, layout);
}


function barplotMain() {
  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];

  geneID = readJson.data.nodes[0].objects;
  bar_x = readJson.data.feature_names;

  for (var value in readJson.data.nodes[0].information){

    if(value.startsWith('N_')){
      N_expression = readJson.data.nodes[0].information[value];
      bar_y.push(N_expression);
    }
  }

  multiplePush(bar_colors,readJson.data.test.length,barRed);
  multiplePush(bar_colors,readJson.data.control.length,barGray);

  // draw bar plot
  var bar_myPlot = document.getElementById('barplot_myDiv')

  barplot_data = [{x:bar_x, y:bar_y, type:'bar',
  marker:{color:bar_colors}}],
  layout = {
    title:barPlotTitle,
    yaxis: {
      title: barPlotYaxisTitle
    },
    width: barPlotWidth,
    height: barPlotHeight
  };
  Plotly.newPlot('barplot_myDiv', barplot_data, layout);
  // draw bar plot end
}


function barplotMain2(readJson) {
  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];

  geneID = readJson.data.nodes[key].objects;
  bar_x = readJson.data.feature_names;

  for (var value in readJson.data.nodes[key].information){

    if(value.startsWith('N_')){
      N_expression = readJson.data.nodes[key].information[value];
      bar_y.push(N_expression);
    }
  }

  multiplePush(bar_colors,readJson.data.test.length,barRed);
  multiplePush(bar_colors,readJson.data.control.length,barGray);

  // draw bar plot
  var bar_myPlot = document.getElementById('barplot_myDiv')

  barplot_data = [{x:bar_x, y:bar_y, type:'bar',
  marker:{color:bar_colors}}],
  layout = {
    title:barPlotTitle,
    yaxis: {
      title: barPlotYaxisTitle
    },
    width: barPlotWidth,
    height: barPlotHeight
  };
  Plotly.newPlot('barplot_myDiv', barplot_data, layout);
  // draw bar plot end
}