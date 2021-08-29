// Inchlib heatmap options
Config_draw_row_ids = false;  // set heatmap row id
Config_target = "inchlib";  // ID of a target HTML element
Config_metadata = true;  // turn on the metadata
Config_column_metadata = false;  // turn on the column metadata
Config_dendrogram = true;
Config_fixed_row_id_size = 0;
Config_max_height = 1070;  // set maximum height of visualization in pixels
Config_width = 800;  // set width of visualization in pixels
Config_heatmap_colors = "BuYl";  // set color scale for clustered data
Config_metadata_colors = "Reds";  // set color scale for metadata

// volcano plot options
volcanoRed = 'rgb(191,56,42)';  // volcano plot red color
volcanoBlue = 'rgb(12,75,142)';  // volcano plot blue clor
volcanoTitle = 'The log2 fold change and p-value<br> obtained from the comparison of the average<br> for each group plotted as the volcano plot.';  // volcano plot title
volcanoPvalueCutOff = 1.3;  // volcano plot pvalue cut off
volcanoFoldchangeCutOff = 1;  // volcano plot fold change cut off
volcanoWidth = 500;  // volcano plot width
volcanoHeight = 500;  // volcano plot height
volcanoPointSize = 5;  // volcano plot point size
volcanoPlotTargetPointSize = 10; // volcano plot mouse over target point size
volcanoInteractiveColor = 'green' // Color changed in volcano plot when heatmap is selected
volcanoYaxisTitle = '-log10(raw.p-value)'
volcanoXaxisTitle = 'log2(fold change)'
volcanoTitleFontSize = 14

// scatter plot options
scatterRed = 'rgb(191,56,42)';  // scatter plot red color
scatterBlue = 'rgb(12,75,142)';  // scatter plot blue clor
scatterPlotTitle = 'Shows overall average expression level <br>between log2 Fold Change';  // scatter plot title
scatterPlotWidth = 500;  // scatter plot width
scatterPlotHeight = 500;  // scatter plot height
scatterPlotPointSize = 5;
scatterInteractiveColor = 'green' // Color changed in volcano plot when heatmap is selected
scatterPlotXaxisTitle = 'average expression'
scatterPlotYaxisTitle = 'log2(fold change)'

// bar plot options
barRed = 'rgba(222,45,38,0.8)'
barGray = 'rgba(204,204,204,1)'
barPlotTitle = "Below barplot show <br> the corresponding sample's expression value."
barPlotYaxisTitle = "Normalized value"
barPlotWidth = 500;  // bar plot width
barPlotHeight = 500;  // bar plot height

// data3 bar plot (fold change) options
data3FcBarPlotTitle = "Below barplot is the fc result for each group."
data3FcBarPlotXaxisTickAngle = 20;
data3FcBarPlotWidth = 500;  // data3 bar plot width
data3FcBarPlotHeight = 500;  // data3 bar plot height
data3FcBarPlotYaxisTitle = 'log2(fold change)'

// data3 bar plot (fold change & pvalue ) options
data3FcPvalBarPlotAnnotation = '***: pvalue < 0.001<br> **: pvalue < 0.01<br> *: pvalue < 0.05<br> N.S.: No Significant'
data3FcPvalBarPlotXaxisTickAngle = 20;
data3FcPvalBarPlotWidth = 500;  // data3 bar plot width
data3FcPvalBarPlotHeight = 500;  // data3 bar plot height
data3FcPvalBarPlotYaxisTitle = 'log2(fold change)'
data3FcPvalBarPlotAnnotationXposition = 1
data3FcPvalBarPlotAnnotationYPosition = 1.25

// box plot options
boxPlotRed = 'rgba(222,45,38,0.8)'
boxPlotGray = 'rgba(204,204,204,1)'
boxPlotTitle = "Below boxplots show the distribution of expression <br> for that group based on percentiles.<br> (median, 50 percentile, 75 percentile, maximum and minimum)";
boxPlotYaxisTitle = "Normalized value"
boxPlotWidth = 500;  // box plot width
boxPlotHeight = 500;  // box plot height
boxPlotTitleFontSize = 14