
var render = function (templateid, targetid, data) {
  var source   = $(templateid).html();
  var template = Handlebars.compile(source);
  var html    = template(data);
  $(targetid).html(html);
}

var renderGallery = function (templateid, targetid, data) {
  var source   = $(templateid).html();
  var template = Handlebars.compile(source);
  var html    = template(data);

  $(targetid).html(html);
  $(targetid).find(".image").each(function() {
    var el = $(this);
    var url = el.css("background-image");
    url = url.substr(4, url.length-5);

    var img = $("<img class='hidden'></img>")
      .attr("src", url)
      .load(function() {
        var w = img.width();
        var h = img.height();
        var ratio = 100.0 / h;
        h = 100;
        w = ratio * w;
        el.width(w).height(h);
        console.log([img.width(), img.height()]);
      });
    $("body").append(img);
  });
}


var jobpapers = { 
  papers: [
    {
    authors: "Leilani Battle, Edward Benson, Aditya Parameswaran, Eugene Wu",
    title: "Indexing Cost Sensitive Prediction",
    url: "./files/papers/csp-techreport.pdf",
    conference: "Technical Report (in submission)",
    links: []
   },
    {
    authors: "  Eugene Wu, Samuel Madden",
    title: "Scorpion: Explaining Away Outliers in Aggregate Queries",
    url: "./files/papers/scorpion-vldb13.pdf",
    conference: "VLDB 2013 (Selected as one of the best papers of the conference!)",
    links: []
   },
   {
    authors: "  Eugene Wu, Samuel Madden, Michael Stonebraker",
    title: "SubZero: a Fine-Grained Lineage System for Scientific Databases",
    url: "./files/papers/subzero-icde13.pdf",
    conference: "ICDE 2013 (Selected as one of the best papers of the conference!)",
    links: []
   },
   {
    authors: "Eugene Wu, Carlo Curino, Sam Madden",
    title: "No Bits Left Behind",
    url: "./files/papers/bits-cidr11.pdf",
    conference: "CIDR 2011",
    links: []
   },
   {
    authors: "Eugene Wu, Yanlei Diao, Shariq Rizvi",
    title: "High-performance complex event processing over streams",
    url: "./files/papers/sase-sigmod06.pdf",
    conference: "SIGMOD 2006",
    links: []
   },
   {
    authors: "  Adam Marcus, Eugene Wu, Sam Madden, Robert Miller",
    title: "Crowdsourced Databases: Query Processing with People",
    url: "./files/papers/qurk-cidr11.pdf",
    conference: "CIDR 2011",
    links: []
   },
   {
    authors: "  Adam Marcus, Eugene Wu, David Karger, Samuel Madden, Robert Miller",
    title: "Human-powered Sorts and Joins",
    url: "./files/papers/qurk-vldb2012.pdf",
    conference: "VLDB 2012",
    links: []
   }  ]
};



var papers = { 
  papers: [
    {
      authors: "Leilani Battle, Edward Benson, Aditya Parameswaran, Eugene Wu",
      title: "Indexing Cost Sensitive Prediction",
      url: "./files/papers/csp-techreport.pdf",
      conference: "Technical Report (in submission)",
      links: []
    },
    {
      authors: "Eugene Wu, Leilani Battle, Samuel Madden",
      title: "The Case for Data Visualization Management Systems",
      url: "./files/papers/ermac-vldb14.pdf",
      conference: "VLDB 2014",
      links: []
    },
   { 
    authors: "Eugene Wu, Adam Marcus and Sam Madden",
    title: "Data In Context: Aiding News Consumers while Taming Dataspaces",
    conference: "DBCrowd 2013",
   },
   {
    authors: "Alvin Cheung, Lenin Ravindranath, Eugene Wu, Samuel Madden, Hari Balakrishnan",
    title: "Mobile applications need Targeted Micro-updates",
    url: "./files/papers/apsys13.pdf",
    conference: "APSYS 2013"
   },
   {
    authors: "  Eugene Wu, Samuel Madden",
    title: "Scorpion: Explaining Away Outliers in Aggregate Queries",
    url: "./files/papers/scorpion-vldb13.pdf",
    conference: "VLDB 2013 (Selected as one of the best papers of the conference!)",
    links: [ {url: "./files/talks/scorpion_vldb13.pdf", text: "Slides (pdf)"}]
   },
   {
    authors: "  Eugene Wu, Samuel Madden, Michael Stonebraker",
    title: "SubZero: a Fine-Grained Lineage System for Scientific Databases",
    url: "./files/papers/subzero-icde13.pdf",
    conference: "ICDE 2013 (Selected as one of the best papers of the conference!)",
    links: []
   },
   {
    authors: "  Eugene Wu, Samuel Madden, Michael Stonebraker",
    title: "A Demonstration of DBWipes: Clean as You Query",
    url: "./files/papers/dbwipes-vldb2012.pdf",
    conference: "VLDB 2012",
    links: []
   },
   {
    authors: "  Adam Marcus, Eugene Wu, David Karger, Samuel Madden, Robert Miller",
    title: "Human-powered Sorts and Joins",
    url: "./files/papers/qurk-vldb2012.pdf",
    conference: "VLDB 2012",
    links: []
   },
   {
    authors: "Eugene Wu, Sam Madden",
    title: "Partitioning Techniques for Fine-Grained Indexing",
    url: "./files/papers/shinobi-icde11.pdf",
    conference: "ICDE 2011",
    links: []
   },
   {
    authors: "    Adam Marcus, Eugene Wu, David Karger, Samuel Madden, Robert Miller",
    title: "Demonstration of Qurk: A Query Processor for Human Operators",
    url: "./files/papers/qurk-sigmod2011.pdf",
    conference: "SIGMOD 2011",
    links: []
   },
   {
    authors: "Eugene Wu, Carlo Curino, Sam Madden",
    title: "No Bits Left Behind",
    url: "./files/papers/bits-cidr11.pdf",
    conference: "CIDR 2011",
    links: []
   },
   {
    authors: "  Adam Marcus, Eugene Wu, Sam Madden, Robert Miller",
    title: "Crowdsourced Databases: Query Processing with People",
    url: "./files/papers/qurk-cidr11.pdf",
    conference: "CIDR 2011",
    links: []
   },
   {
    authors: "    Carlo Curino, Evan Jones, Raluca Popa, Nirmesh Malviya, Eugene Wu, Sam Madden, Hari Balakrishnan, Nickolai Zeldovich",
    title: "Relational Cloud: A Database-as-a-Service for the Cloud",
    url: "./files/papers/relcloud-cidr11.pdf",
    conference: "CIDR 2011",
    links: []
   },
   {
    authors: "Carlo Curino, Evan Jones, Yang Zhang, Eugene Wu, Sam Madden",
    title: "Relational Cloud: The Case for a Database Service",
    url: "./files/papers/caseforrelationalcloud.pdf",
    conference: "",
    links: [{url: "http://hdl.handle.net/1721.1/52606", text: "Technical Report"}]
   },
   {
    authors: "Philippe Cudre-Mauroux, Eugene Wu, Sam Madden",
    title: "TrajStore: An Adaptive Storage System for Very Large Trajectory Data Sets",
    url: "./files/papers/trajstore-icde10.pdf",
    conference: "ICDE 2010",
    links: []
   },
   {
    authors: "Eugene Wu, Philippe Cudre-Mauroux, Sam Madden",
    title: "Demonstration of the TrajStore System",
    url: "./files/papers/trajstore-vldb09demo.pdf",
    conference: "VLDB 2009",
    links: []
   },
   {
    authors: "Philippe Cudre-Mauroux, Eugene Wu, Sam Madden",
    title: "The Case for RodentStore: An Adaptive, Declarative Storage System",
    url: "http://www-db.cs.wisc.edu/cidr/cidr2009/Paper_97.pdf",
    conference: "CIDR 2009",
    links: []
   },
   {
    authors: "Michael Cafarella, Alon Halevy, Daisy Wang, Eugene Wu, Yang Zhang",
    title: "WebTables: Exploring the Power of Tables on the Web",
    url: "./files/papers/webtables-vldb08.pdf",
    conference: "VLDB 2008",
    links: []
   },
   {
    authors: "Michael Cafarella, Nodira Khoussainova, Daisy Wang, Eugene Wu, Yang Zhang, Alon Halevy",
    title: "Uncovering the Relational Web",
    url: "./files/papers/relweb-webdb08.pdf",
    conference: "WebDB 2008",
    links: []
   },
   {
    authors: "Daniel Gyllstrom, Eugene Wu, Hee-Jin Chae, Yanlei Diao, Patrick Stahlberg, Gordon Anderson",
    title: "SASE: Complex Event Processing over Streams (Demo)",
    conference: "CIDR 2007",
    links: []
   },
   {
    authors: "Eugene Wu, Yanlei Diao, Shariq Rizvi",
    title: "High-performance complex event processing over streams",
    url: "./files/papers/sase-sigmod06.pdf",
    conference: "SIGMOD 2006",
    links: []
   },
   {
    authors: "Daniel Gyllstrom, Eugene Wu, Hee-Jin Chae, Yanlei Diao, Patrick Stahlberg, Gordon Anderson",
    title: "SASE: Complex Event Processing over Streams",
    conference: "CoRR 2006",
    links: []
   },
   {
    authors: "Minos N. Garofalakis, Kurt P. Brown, Michael J. Franklin, Joseph M. Hellerstein, Daisy Zhe Wang, Eirinaios Michelakis, Liviu Tancau, Eugene Wu, Shawn R. Jeffery, Ryan Aipperspach",
    title: "Probabilistic Data Management for Pervasive Computing: The Data Furnace Project",
    conference: "IEEE Data Eng. Bull.",
    links: []
   },
   {
    authors: "Michael J. Franklin, Shawn R. Jeffery, Sailesh Krishnamurthy, Frederick Reiss, Shariq Rizvi, Eugene Wu, Owen Cooper, Anil Edakkunni, Wei Hong",
    title: "Design Considerations for High Fan-In Systems: The HiFi Approach",
    url: "./files/papers/",
    conference: "CIDR 2005",
    links: []
   },
   {
    authors: "Owen Cooper, Anil Edakkunni, Michael J. Franklin, Wei Hong, Shawn R. Jeffery, Sailesh Krishnamurthy, Frederick Reiss, Shariq Rizvi, Eugene Wu",
    title: "HiFi:  A Unified Architecture for High Fan-in Systems",
    conference: "VLDB 2004 Demo",
    links: []
   }
  ]
};



var shirts = [
  "magneto.png",
  "shredder.png",
  "skeletor.png",
  "bitsfactory.png",
  "robotassemble.png",  
  "2pacbiggie.png",
  "ahab.png",
  "bearninja.png",
  "dinospace.png",
  "penguin.png",
  "skynet.png",
  "hal.png"
];

var misc = [  
  "gexperiments.jpg",
  "cameraculture.png",
  "caveman.png",
  "turtle.png",

];

var posters = [
  "assassin.png",
  "sithhappens.png",
  "superheros.png"
]

var ultimate = [
  "grimbeaver.png",
  "grim2.png",
  "ghostface.png",
  "rambo.png",  
  "mixednuts.png",
  "mixedfront.png",
]

var layerpp = [
  "volley1.png",
  "volley4.png"
];

var rap = [
  "alleyez.png",
  "readytodie.png",
  "violentbydesign.png"
];

var kc = [
  "orange.gif",
  "satsuma.gif",
  "noochtella.png"
]

var wildthings = [
  "wildthings_sleep.png",
  "wildthings_cartoon.png"
]

var slamdunks = [
  "slamdunk.png",
  "slamdunk2.png",
  "slamdunk3.png",
  "slamdunk5.png",
]
