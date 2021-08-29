class HtmlWithoutPval:
    def __init__(self):
        self.goDescription = ""
        self.keggDescription = ""
        self.labelDescription = ""

    def writeGoColumn(self, goDic, DEG_group, htmlType):
        if htmlType.lower() == "main":
            relativePath = "."
        if htmlType.lower() == "sub":
            relativePath = ".."

        goConverterDic = {"BP":"biological process","CC":"cellular component","MF":"molecular function"}
        for source in goDic:
            self.goDescription+=f'''<div class="enrichment-title"><caption >g:Profiler ({goConverterDic[source]})</caption></div>\n
            <style>th,td {{padding-bottom: 12px; padding-right:50px;}}</style>
            <table class="enrichment-table">
                <th>Term</th>
                <th>p-Adj</th>
            '''
            for goTerm in goDic[source]:
                self.goDescription+=f'''<tr>
                    <td style="text-align: left; cursor: pointer" onclick="load_json('{relativePath}/json/{DEG_group}/{source}/{goTerm}.json','{goTerm}')">{goTerm}</td>
                    <td align="right">{goDic[source][goTerm]}</td>
                </tr>
                '''
            self.goDescription+="</table>"

    def writeKEGGColumn(self, keggDic, DEG_group, htmlType):
        if htmlType.lower() == "main":
            relativePath = "."
        if htmlType.lower() == "sub":
            relativePath = ".."

        self.keggDescription+=f'''<div class="enrichment-title"><caption >KEGG</caption></div>\n
        <style>th,td {{padding-bottom: 12px; padding-right:50px;}}</style>
        <table class="enrichment-table">
            <th>Term</th>
            <th>p-Adj</th>
        '''
        for keggTerm in keggDic:
            self.keggDescription+=f'''<tr>
                <td style="text-align: left; cursor: pointer" onclick="load_json('{relativePath}/json/{DEG_group}/KEGG/{keggTerm}.json','{keggTerm}')">{keggTerm}</td>
                <td align="right">{keggDic[keggTerm]}</td>
            </tr>
            '''
        self.keggDescription+="</table>"

    def writeLabelColumn(self, DegGroupDic):

        for data3File in DegGroupDic:
            degGroup = DegGroupDic[data3File]
            degGroup = degGroup.replace("/","_").replace(" ","_").replace("-","_").replace("(","_").replace(")","_").replace(",","_").replace(".","_")
            if degGroup == "data3_File":
                self.labelDescription += f'''
                <li>
                    <a href="#">
                        <div style="display: flex; align-items: center; justify-content: space-between; ">
                        <span class="icon"><i class="fa-type fas fa-users"></i></span>
                        <span><a href="../data3_File.html">data3_File</a></span>
                        </div>
                    </a>
                </li>
                '''
                continue

            self.labelDescription += f'''
            <li>
                <a href="#">
                    <div style="display: flex; align-items: center; justify-content: space-between; ">
                    <span class="icon"><i class="fa-type fas fa-users"></i></span>
                    <span><a href="{degGroup}.html">{degGroup}</a></span>
                    </div>
                </a>
            </li>
            '''

    def makeHtmlReport(self, fileName, DEG_group, htmlType, plotName):
        if htmlType.lower() == "main":
            relativePath = "."
        if htmlType.lower() == "sub":
            relativePath = ".."
        fw=open(fileName,'w')
        fw.write(
	f'''
<html>
<head>
    <!-- sidebar -->
    <head><link rel="stylesheet" href="{relativePath}/css/sidebar.css"></head>
    <head><link rel="stylesheet" href="{relativePath}/css/selectbox.css"></head>
    <head><link rel="stylesheet" href="{relativePath}/css/scrollbar.css"></head>
    <head><link rel="stylesheet" href="{relativePath}/css/enrichment.css"></head>
    <script src="{relativePath}/javascript/inchlibMainWithoutPval.js"></script>
    <script src='{relativePath}/javascript/barplot.js'></script>
    <script src='{relativePath}/javascript/boxplot.js'></script>
    <script src='{relativePath}/javascript/scatter_plotly_mod.js'></script>

    <!-- inchlib -->
    <script src="https://code.jquery.com/jquery-2.2.1.js"></script>
    <script src="http://download.macrogen.com/~seqdata/NGS/NGS_DEG_ver2/test/kinetic-v5.1.0.min.js"></script>
    <script src="{relativePath}/javascript/Inchlib.js"></script>

    <!-- plotly -->
    <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>

    <!-- read Json file -->
    <script src="{relativePath}/json/data3_{DEG_group}.json"></script>

    <!-- navy css -->
    <link rel="stylesheet" type="text/css" href="{relativePath}/css/style.css">
    <link rel="stylesheet" type="text/css" href="{relativePath}/css/reset.css">

    <!-- read JS file  -->
    <script src="{relativePath}/javascript/variableConfigs.js"></script>
    <script src="{relativePath}/javascript/navyWithOutPval.js"></script>
    <script>
        readJson = runinchlib(eval({DEG_group}));
    </script>
</head>

<body>
    <div class="toggle" onclick="toggleMenu()"></div>
        <div class="navigation">

            <ul>
                {self.labelDescription}
            </ul>
        </div>

    <div class="column-position">

        <div id="inchlib">
        </div>

        <div >
            <select id="app-cover" onchange="categoryChange(this)">
                    <option value="scatter">{plotName}</option>
            </select>
            <div id='scatter_myDiv'>
                <script>scatterPlotMain();</script>
            </div>


            <select id="app-cover" onchange="categoryChange(this)">
                    <option value="barplot">Bar plot</option>
                    <option value="boxplot">Box plot</option>
            </select>
            <div id='barplot_myDiv' style='margin-bottom: 50px;'>
                <script>barplotMain(readJson);</script>
            </div>
            <div id='boxplot_myDiv' style='margin-bottom: 50px;' class='visibility'>
                <script>boxPlotMain();</script>

            </div>
        </div>

        <!-- <select name="pets" multiple size="4" class="selctbox-type">

        </select> -->


        <div>
            {self.goDescription}
            {self.keggDescription}
        </div>

    </div>

    <nav class="nav">
        <ul class="nav__list">
            <div>
                <li style="font-size: 5px">Gene</li>
                <li class="nav_gene">Gene</li>
            </div>
            <div>
                <li style="font-size: 5px">gene_Symbol</li>
                <li class="gene_Symbol">gene_Symbol</li>
            </div>
            <div>
                <li style="font-size: 5px">description</li>
                <li class="description">description</li>
            </div>
            <div>
                <li style="font-size: 5px">gene_biotype</li>
                <li class="gene_biotype">gene_biotype</li>
            </div>
            <div>
                <li style="font-size: 5px">fold_change</li>
                <li class="fold_change">fold_change</li>
            </div>
        </ul>
    </nav>
    <script
    src="http://kit.fontawesome.com/6478f529f2.js"
    crossorgin="anonymous">
    </script>
    <script type="text/javascript">
        function toggleMenu(){{
            let navigation = document.querySelector('.navigation');
            let toggle = document.querySelector('.toggle');
            navigation.classList.toggle('active');
            toggle.classList.toggle('active');
        }}
    </script>
    <script type="text/javascript">
        function load_json(src, dataKey) {{
            // console.log(key);
          var head = document.getElementsByTagName('head')[0];

          //use class, as we can't reference by id
          var element = head.getElementsByClassName("json")[0];

          try {{
            element.parentNode.removeChild(element);
          }} catch (e) {{
            //
          }}

          var script = document.createElement('script');
          script.type = 'text/javascript';
          script.src = src;
          script.className = "json";
          script.async = false;
          head.appendChild(script);


          setTimeout(function() {{
            readJson = runinchlib(eval(dataKey));
            barplotMain2(readJson);
            boxPlotMain2();
            scatterPlotMain();
          }}, 50);
        }}



    </script>
</body>

</html>
	''')
        fw.close()