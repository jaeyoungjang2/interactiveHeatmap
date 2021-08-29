function bar_Data3paintImage(ids, readJson){
  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];
  let pval_lst = [];

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;

    if(geneID && geneID == ids[0]){
      for ( var i = 0; i < readJson.data.group_names.length; i++) {
        fc_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".fc"]
        pval_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".raw.pval"]
        bar_x.push(readJson.data.group_names[i]);
        if (fc_temp > 0) {
          fc = logB(fc_temp,2);
          bar_colors.push(volcanoRed);
        } else {
          fc = -logB(-fc_temp,2);
          bar_colors.push(volcanoBlue);
        }
        bar_y.push(fc)
        if (pval_temp < 0.001) {
          pval_lst.push("***");
        } else if (pval_temp < 0.01) {
          pval_lst.push("**");
        } else if (pval_temp < 0.05) {
          pval_lst.push("*");
        } else {
          pval_lst.push("N.S.")
        }
      }
    }
  }


  barplot_data = [{
    x:bar_x,
    y:bar_y,
    type:'bar',
    text: pval_lst,
    textposition: 'outside',
    marker:{color:bar_colors}}]

  layout = {
    yaxis: {
      zeroline: true,
      gridwith: 4
    },
    annotations: [
    {
      xref: 'paper',
      yref: 'paper',
      xanchor: 'right',
      yanchor: 'top',
      x: data3FcPvalBarPlotAnnotationXposition,
      y: data3FcPvalBarPlotAnnotationYPosition,
      text: data3FcPvalBarPlotAnnotation,
      textposition: 'outside',
      showarrow: false,
    }
  ],
    xaxis: {
      tickangle: data3FcPvalBarPlotXaxisTickAngle
    },
    yaxis: {
    title: data3FcPvalBarPlotYaxisTitle
    }
  };

  Plotly.newPlot('barplot_myDiv2', barplot_data, layout);
}


function barplotData3Main() {
  ids = readJson.data.nodes[0].objects;
  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];
  let pval_lst = [];

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;

    if(geneID && geneID == ids[0]){
      for ( var i = 0; i < readJson.data.group_names.length; i++) {
        fc_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".fc"]
        pval_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".raw.pval"]
        bar_x.push(readJson.data.group_names[i]);
        if (fc_temp > 0) {
          fc = logB(fc_temp,2);
          bar_colors.push(volcanoRed);
        } else {
          fc = -logB(-fc_temp,2);
          bar_colors.push(volcanoBlue);
        }
        bar_y.push(fc)
        if (pval_temp < 0.001) {
          pval_lst.push("***");
        } else if (pval_temp < 0.01) {
          pval_lst.push("**");
        } else if (pval_temp < 0.05) {
          pval_lst.push("*");
        } else {
          pval_lst.push("")
        }
      }
    }
  }


  barplot_data = [{
    x:bar_x,
    y:bar_y,
    type:'bar',
    text: pval_lst,
    textposition: 'outside',
    marker:{color:bar_colors}}]

  layout = {
    width: data3FcPvalBarPlotWidth,
    height: data3FcPvalBarPlotHeight,
    yaxis: {
      zeroline: true,
      gridwith: 4
    },
    annotations: [
    {
      xref: 'paper',
      yref: 'paper',
      xanchor: 'right',
      yanchor: 'top',
      x: 1,
      y: 1.25,
      text: data3FcPvalBarPlotAnnotation,
      textposition: 'outside',
      showarrow: false,
    }
  ],
    xaxis: {
      tickangle: data3FcPvalBarPlotXaxisTickAngle
    },
    yaxis: {
    title: data3FcPvalBarPlotYaxisTitle
    }
  };

  Plotly.newPlot('barplot_myDiv2', barplot_data, layout);
}

function barplotData3Main2(readJson) {

  ids = readJson.data.nodes["inchlib#0"].objects;

  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];
  let pval_lst = [];

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;

    if(geneID && geneID == ids[0]){
      for ( var i = 0; i < readJson.data.group_names.length; i++) {
        fc_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".fc"]
        pval_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".raw.pval"]
        bar_x.push(readJson.data.group_names[i]);
        if (fc_temp > 0) {
          fc = logB(fc_temp,2);
          bar_colors.push(volcanoRed);
        } else {
          fc = -logB(-fc_temp,2);
          bar_colors.push(volcanoBlue);
        }
        bar_y.push(fc)
        if (pval_temp < 0.001) {
          pval_lst.push("***");
        } else if (pval_temp < 0.01) {
          pval_lst.push("**");
        } else if (pval_temp < 0.05) {
          pval_lst.push("*");
        } else {
          pval_lst.push("")
        }
      }
    }
  }


  barplot_data = [{
    x:bar_x,
    y:bar_y,
    type:'bar',
    text: pval_lst,
    textposition: 'outside',
    marker:{color:bar_colors}}]

  layout = {
    width: data3FcPvalBarPlotWidth,
    height: data3FcPvalBarPlotHeight,
    yaxis: {
      zeroline: true,
      gridwith: 4
    },
    annotations: [
    {
      xref: 'paper',
      yref: 'paper',
      xanchor: 'right',
      yanchor: 'top',
      x: data3FcPvalBarPlotAnnotationXposition,
      y: data3FcPvalBarPlotAnnotationYPosition,
      text: data3FcPvalBarPlotAnnotation,
      textposition: 'outside',
      showarrow: false,
    }
  ],
    xaxis: {
      tickangle: data3FcPvalBarPlotXaxisTickAngle
    },
    yaxis: {
    title: data3FcPvalBarPlotYaxisTitle
    }
  };

  Plotly.newPlot('barplot_myDiv2', barplot_data, layout);
}