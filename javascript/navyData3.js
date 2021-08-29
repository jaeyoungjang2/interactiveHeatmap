function get_information(gene){
  var gene_Symbol
  var description
  var gene_biotype
  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;

    if(geneID && geneID[0] == gene){
      // scatter_colors.push('#00000');
      for (var value in readJson.data.nodes[key].information){
        if(value.endsWith('Gene_Symbol')){
          gene_Symbol = readJson.data.nodes[key].information[value]
          // console.log(gene_Symbol);
        } else if(value.endsWith('Description')){
          description = readJson.data.nodes[key].information[value]
          // console.log(description);
        } else if(value.endsWith('gene_biotype')){
          gene_biotype = readJson.data.nodes[key].information[value]
          // console.log(gene_biotype);
        } else if(value.endsWith('fc')){
          fold_change = readJson.data.nodes[key].information[value]
          // console.log(gene_biotype);
        } else if(value.endsWith('raw.pval')){
          raw_pval = readJson.data.nodes[key].information[value]
          // console.log(gene_biotype);
        }
      }
      // return [gene_Symbol, description, gene_biotype];
      nav_changer(gene, gene_Symbol, description, gene_biotype, fold_change, raw_pval);
    }
  }
  // return [gene_Symbol, description, gene_biotype];
}

function nav_changer(gene, gene_Symbol, description, gene_biotype, fold_change, raw_pval){

  const navGene = document.querySelector(".nav_gene");
  const navGeneSymbol = document.querySelector(".gene_Symbol");
  const navDescription = document.querySelector(".description");
  const navGeneBiotype = document.querySelector(".gene_biotype");

  navGene.innerHTML = gene;
  navGeneSymbol.innerHTML = gene_Symbol
  navDescription.innerHTML = description
  navGeneBiotype.innerHTML = gene_biotype
}

// select box

function categoryChange(e){
  if (e.value == "scatter") {
    document.querySelector("#volcano_myDiv").classList.add('visibility');
    document.querySelector("#scatter_myDiv").classList.remove('visibility');
  } else if(e.value == "volcano") {
    document.querySelector("#scatter_myDiv").classList.add('visibility');
    document.querySelector("#volcano_myDiv").classList.remove('visibility');
  } else if(e.value == "barplot") {
    document.querySelector("#boxplot_myDiv").classList.add('visibility');
    document.querySelector("#barplot_myDiv").classList.remove('visibility');

  } else if(e.value == "boxplot") {
    document.querySelector("#barplot_myDiv").classList.add('visibility');
    document.querySelector("#boxplot_myDiv").classList.remove('visibility');
  }
}


function nav_init(){
  const navGene = document.querySelector(".nav_gene");
  const navGeneSymbol = document.querySelector(".gene_Symbol");
  const navDescription = document.querySelector(".description");
  const navGeneBiotype = document.querySelector(".gene_biotype");
  navGene.innerHTML = "gene";
  navGeneSymbol.innerHTML = "gene_Symbol"
  navDescription.innerHTML = "description"
  navGeneBiotype.innerHTML = "gene_biotype"
}