// start: draw volcano plotly
function setInitialScatter(){
  let scatter_x = [];
  let scatter_y = [];
  let scatter_text = [];
  let scatter_colors = [];
  let scatter_point_size = [];

  var scatter_myPlot = document.getElementById('scatter_myDiv')

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;
    if(geneID){
      scatter_text.push(geneID[0]);
      for (var value in readJson.data.nodes[key].information){
        if(value.endsWith('logCPM') | value.endsWith('baseMean') | value.endsWith('volume')){
          logCPM = readJson.data.nodes[key].information[value]
          scatter_x.push(logCPM)
        } else if(value.endsWith('fc')){
          fc_temp = readJson.data.nodes[key].information[value];
          if (fc_temp > 0) {
            fc = logB(fc_temp,2);
          } else {
            fc = -logB(-fc_temp,2);
          }
          scatter_y.push(fc)
        }
      }

        if(geneID && fc >= 1){
        // red
        scatter_colors.push(scatterRed);
        scatter_point_size.push(scatterPlotPointSize);
      } else {
        // blue
        scatter_colors.push(scatterBlue);
        scatter_point_size.push(scatterPlotPointSize);
      }
    }
  }

  // x = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1],
  // y = [1, 2, 3, 2, 3, 2, 3, 2, 3, 4],
  // colors = ['#00000', '#00000','#00000','#00000','#00000','#00000','#00000','#00000','#00000','#00000'],
  // text = ['11541','11540','11433','11576','11548','11459','11499','11550','11474','11496'],
  scatter_data = [{x:scatter_x, y:scatter_y, type:'scatter',
           mode:'markers', marker:{size:scatterPlotPointSize, color:scatter_colors} ,text:scatter_text}],

  scatter_layout = {
    yaxis: {
    title: scatterPlotYaxisTitle
    },
    xaxis: {
    title: scatterPlotXaxisTitle
    },
    hovermode:'closest',
    title: scatterPlotTitle,
    width: scatterPlotWidth,
    height: scatterPlotHeight,
  };

  Plotly.newPlot('scatter_myDiv', scatter_data, scatter_layout);
  // end: draw plotly
  return {color: scatter_colors, myplot: scatter_myPlot, size: scatter_point_size};
}


function scatter_paintImage(ids){
  let index;
  for(var i=0; i < scatter_data[0].text.length; i++){
      if (ids[0] === scatter_data[0].text[i]) {
        scatterHoverColor = scatter_colors[i]
        scatter_colors[i] = scatterInteractiveColor;
        scatter_point_size[i] = 10;
        index = i;
      }
  }

  var scatter_update = {'marker':{color: scatter_colors, size:scatter_point_size}};
  Plotly.restyle('scatter_myDiv', scatter_update, [0]);

  return [scatterHoverColor, index];
}

function scatter_unpaintImage(index, scatterHoverColor){
  scatter_colors[index] = scatterHoverColor;
  scatter_point_size[index] = scatterPlotPointSize

  var scatter_update = {'marker':{color: scatter_colors, size:scatter_point_size}};
  Plotly.restyle('scatter_myDiv', scatter_update, [0]);
}

function scatterPlotMain(){
  scatter_config = setInitialScatter();
  scatter_colors = scatter_config.color;
  scatter_myPlot = scatter_config.myplot;
  scatter_point_size = scatter_config.size;

  const scatterOriginalColor = $.extend(true,[],scatter_colors);

  // plotly hover event
  scatter_myPlot.on('plotly_hover', function(scatter_data){
    pn = scatter_data.points[0].pointNumber;
    ids = [scatter_data.points[0].text];
    inchlib.highlight_rows(ids);
    bar_paintImage(ids, readJson);
    box_paintImage(ids);
    informations = get_information(ids);

    scatter_colors[pn] = scatterInteractiveColor;
    var scatter_update = {'marker':{color: scatter_colors, size:scatterPlotPointSize}};
    Plotly.restyle('scatter_myDiv', scatter_update, 0);

  });

  // plotly unhover event
  scatter_myPlot.on('plotly_unhover', function(scatter_data){
    scatter_colors = $.extend(true,[],scatterOriginalColor);

    inchlib.unhighlight_cluster([scatter_data.points[0].text]);
    var scatter_update = {'marker':{color: scatter_colors, size:scatterPlotPointSize}};
    Plotly.restyle('scatter_myDiv', scatter_update, 0);
  });
}

function logB(x, base) {
  return Math.log(x) / Math.log(base);
}