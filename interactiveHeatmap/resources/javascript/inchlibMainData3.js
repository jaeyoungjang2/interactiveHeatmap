function runinchlib(file) {
    var readJson = file;

    var volcanoHoverColor;
    $(document).ready(function() { //run when the whole page is loaded
        let hoverGene;
        window.inchlib = new InCHlib({ //instantiate InCHlib
            target: "inchlib", //ID of a target HTML element
            metadata: Config_metadata, //turn on the metadata
            column_metadata: Config_column_metadata, //turn on the column metadata
            draw_row_ids: Config_draw_row_ids,
            dendrogram: Config_dendrogram,
            fixed_row_id_size: Config_fixed_row_id_size,
            max_height: Config_max_height, //set maximum height of visualization in pixels
            width: Config_width, //set width of visualization in pixels
            heatmap_colors: Config_heatmap_colors, //set color scale for clustered data
            metadata_colors: Config_metadata_colors //set color scale for metadata
         });

        nav_init();
        inchlib.read_data_from_file(readJson); //read input json file
        inchlib.draw(); //draw cluster heatmap

        inchlib.events.row_onmouseover = function(ids, evt){
            hoverGene = ids;
            inchlib.highlight_rows(ids);
            bar_paintImage(ids, readJson);
            bar_Data3paintImage(ids, readJson);

            informations = get_information(ids);
            inchlib.unhighlight_cluster();
        };

        inchlib.events.row_onmouseout = function(){
            inchlib.unhighlight_rows(hoverGene);
        };
    });
    return readJson;
}
