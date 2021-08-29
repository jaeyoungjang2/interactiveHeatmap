// start: draw volcano plotly


function setInitialVolcano(readJson){
  let volcano_x = [];
  let volcano_y = [];
  let volcano_text = [];
  let volcano_colors = [];
  let volcano_point_size = [];

  var volcano_myPlot = document.getElementById('volcano_myDiv')

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;
    if(geneID){
      volcano_text.push(geneID[0]);
      let fc;
      let pval;
      for (var value in readJson.data.nodes[key].information){
        if(value.endsWith('fc')){
          fc_temp = readJson.data.nodes[key].information[value];
          if (fc_temp > 0) {
            fc = logB(fc_temp,2);
          } else {
            fc = -logB(-fc_temp,2);
          }

          volcano_x.push(fc)
        } else if(value.endsWith('raw.pval')){
          pval = -logB(readJson.data.nodes[key].information[value],10)
          volcano_y.push(pval)
        }
      }
      if(geneID && (fc >= volcanoFoldchangeCutOff) && pval >= volcanoPvalueCutOff){
          // red
          volcano_colors.push(volcanoRed);
          volcano_point_size.push(volcanoPointSize);

        } else {
          // blue
          volcano_colors.push(volcanoBlue);
          volcano_point_size.push(volcanoPointSize);
        }
    }
  }

  volcano_data = [{
    x:volcano_x,
    y:volcano_y,
    type:'scatter',
    mode:'markers',
    marker:{
      size: volcanoPointSize,
      color:volcano_colors
    },
    text:volcano_text
  }],
  layout = {
    title: {text: volcanoTitle,
      font: {size: volcanoTitleFontSize},
      xref: 'paper',
      yref: 'paper',
    },
    yaxis: {
    title: volcanoYaxisTitle
    },
    xaxis: {
    title: volcanoXaxisTitle
    },
    hovermode:'closest',
    width: volcanoWidth,
    height: volcanoHeight
  };

  Plotly.newPlot('volcano_myDiv', volcano_data, layout);
  // end: draw plotly
  return {color: volcano_colors, myplot: volcano_myPlot, size: volcano_point_size};
}

function volcano_paintImage(ids, volcanoHoverColor){
  let index;
  for(var i=0; i < volcano_data[0].text.length; i++){
      if (ids[0] === volcano_data[0].text[i]) {
        volcanoHoverColor = volcano_colors[i]
        volcano_colors[i] = volcanoInteractiveColor;
        volcano_point_size[i] = volcanoPlotTargetPointSize;
        index = i;
      }
  }
  var volcano_update = {'marker':{color: volcano_colors, size: volcano_point_size}};
  Plotly.restyle('volcano_myDiv', volcano_update, [0]);

  return [volcanoHoverColor, index];
}

function volcano_unpaintImage(index, volcanoHoverColor){
  volcano_colors[index] = volcanoHoverColor;
  volcano_point_size[index] = volcanoPointSize
  var volcano_update = {'marker':{color: volcano_colors, size: volcano_point_size}};
  Plotly.restyle('volcano_myDiv', volcano_update, [0]);
}


function volcanoPlotMain(readJson){
  volcano_config = setInitialVolcano(readJson);
  volcano_colors = volcano_config.color;
  volcano_myPlot = volcano_config.myplot;
  volcano_point_size = volcano_config.size;

  const volcanoOriginalColor = $.extend(true,[],volcano_colors);

//   // volcano plot hover event
  volcano_myPlot.on('plotly_hover', function(volcano_data){
    pn = volcano_data.points[0].pointNumber;
    ids = [volcano_data.points[0].text];
    inchlib.highlight_rows(ids);
    bar_paintImage(ids, readJson);
    box_paintImage(ids);
    get_information(ids);

    volcano_colors[pn] = volcanoInteractiveColor;
    var volcano_update = {'marker':{color: volcano_colors, size: volcanoPointSize}};
    Plotly.restyle('volcano_myDiv', volcano_update, 0);
  });

// // // plotly unhover event
  volcano_myPlot.on('plotly_unhover', function(volcano_data){
    volcano_colors = $.extend(true,[],volcanoOriginalColor);
    var volcano_update = {'marker':{color: volcano_colors, size: volcanoPointSize}};
    Plotly.restyle('volcano_myDiv', volcano_update, 0);
  });
}


function logB(x, base) {
  return Math.log(x) / Math.log(base);
}