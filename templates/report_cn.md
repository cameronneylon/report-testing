{% import "macros.md" as helper with context %}
<style>
@font-face {
    font-family: Gelasio;
    src: url('fonts/Gelasio-Regular.ttf');
}
@font-face {
    font-family: DancingScript;
    src: url('fonts/DancingScript-VariableFont:wght.ttf');
}
@font-face {
    font-family: Baskerville;
    src: url('fonts/LibreBaskerville-Regular.ttf');
}
@font-face {
    font-family: Garamond;
    src: url('/Users/266883j/Documents/oa_reporting_demo/fonts/Garamond.ttf')
}
/* Italic */
@font-face {
   font-family: Garamond;
   src: url('/Users/266883j/Documents/oa_reporting_demo/fonts/Garamond-Italic.ttf');
   font-style: italic;
}

/* Bold */
@font-face {
   font-family: Garamond;
   src: url('/Users/266883j/Documents/oa_reporting_demo/fonts/Garamond-Bold.ttf');
   font-weight: bold;
}
@font-face {
    font-family: Montserrat;
    src: url('/Users/266883j/Documents/oa_reporting_demo/fonts/Montserrat-Regular.ttf')
}
@page {
    size: a4 portrait;
    @frame content_frame {          
            left: 1cm; width: 19cm; top: 1.5cm; height: 25.2cm;
        }
    @frame left_footer_frame {           
            -pdf-frame-content: left_footer_content;
            left: 1.5cm; width: 10cm; top: 26.7cm; height: 2cm;
            border-style: solid none none none;
        }

    @frame right_footer_frame {
            -pdf-frame-content: right_footer_content;
            left: 17cm; width 3cm; top: 26.7cm; height: 2cm;
            border-style: solid none none none;
    }
}
body {
    font-family: Garamond, serif;
}

h1 { 
    font-family: Montserrat, sans-serif;
    font-size: 18pt;
    color: #404040;
    margin: 0 ;
    padding: 2pt;
}
h2 { 
    font-family: Montserrat, sans-serif;
    font-size: 14pt;
    color: DimGrey;
    margin: 0 ;
    padding: 2pt;
}
h3 { 
    font-size: 12pt ; 
    font-family: Montserrat, sans-serif;
    margin: 0;
    padding: 2pt;    
} 
h4 { font-size: 12pt ; } 
p { 
    font-size: 11pt;
    margin: 0;
    padding-top: 0;
}
table {
    font-size: 9pt ;
}
th {
    table-layout: auto;
    padding-top: 4pt;
    padding-left: 2pt;
    padding-right: 0pt;
    background-color: white;
    text-align: center;
    font-weight: bold;
    border-bottom-color: black;
    border-bottom-width: 1px;
    border-bottom-style: solid;
    border-top-color: black;
    border-top-width: 1px;
    border-top-style: black;
}
td {
    padding-top: 2pt;
    padding-left: 2pt;
    padding-right: 0pt;
	text-align: center;
}
img {
    vertical-align: top;
}

figcaption {
    font-size: 9pt;
}
caption {
    font-size: 9pt;
}

.hcenter {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}

.vcenter {
    display: block;
    margin-topt: auto;
    margin-bottom: auto;
}

</style>

{% set metadata = load_json("metadata.json") %}
{% set oa_table_by_year = load_json('oa_table_by_year.json') %}
{% set focus_year = load_json('focus_year_data.json') %}

<!-- Static Frame Left Footer for Reports -->

<div id="left_footer_content">
    <p>
    Produced by the Curtin Open Knowledge Initiative - page <pdf:pagenumber>
    </p>

    <p>
    Report Version 0.1 - Generated on {{ helper.created_at() }}
    </p>
</div>

<!-- Static Frame Right Footer for Reports -->

<div id="right_footer_content">
    <img src="/Users/266883j/Documents/oa_reporting_demo/assets/coki_small.png" width="150" class="vcenter" />
</div>

<!-- Content Frame for Report Contents -->

# Open Knowledge Report for {{ metadata.entity_name }}

<i>{{ metadata.entity_name }}, GRID: {{ metadata.identifier }}, Report generated on {{ helper.created_at() }}</i>

## Data Sources and Outline

Data were collected from four main sources. Bibliographic data sources (Microsoft Academic, Scopus and
Web of Science) were searched to obtain DOIs representing research outputs associated with {{ metadata.entity_name }}. Crossref Metadata was collected for each DOI identified to provide information on funding and publication dates. Citation data was obtained from the Open Citations Corpus. Finally, DOIs were checked against Unpaywall to determine open access status.

### Limitations
The main limitations relate to the timeframes over which data sources have collected data and the coverage of repositories by Unpaywall. Funder data only exists from the commencement of the Fundref initiative and is not complete. Finally the bibliographic data sources themselves have substantial biases and limitations with respect to affiliation sources. These are mitigated through our use of three independent data sources.

The precise levels of open access should be treated with caution and comparison to other analyses is not straightforward. The comparisons made using other Unpaywall data and within this report may be considered reliable with the caveat that they measure visibility and indexing and not necessarily the up to date contents of the repository.

## Analysis

### Published outputs, numbers and types

All collected outputs matching the search terms above were deduplicated by DOI and the type determined from Crossref metadata. This can give a broad view of the growth of outputs over time and an overview of the diversity and types of outputs. Growth of the set of outputs indexed by the bibliographic data sources used will be a contributor to the growth in outputs.

<figure>
    <p>
    <img src="outputs_time_chart.png" width=450px />
    <img src="outputs_pie_chart.png"  width=350px />
    <figcaption><strong>Figure 1.</strong> Outputs of {{ metadata.entity_name }} over time and by proportion for {{ focus_year.published_year }}. These data are for those objects captured in Crossref metadata. This means that particularly for datasets and reports the numbers will be under-reported as many of these categories of outputs do not received Crossref DOIs.</figcaption>
</figure>

### Open Access Status

Open access status is determined globally using Unpaywall data. This gives details of both repository locations and of publisher-based open access. Where Unpaywall is fully indexing the university repository we can determine the levels of institutional archiving.

In {{ focus_year.published_year }} the overall level of open access for {{ metadata.entity_name }} was {{ focus_year.percent_total_oa }}%.

<figure>
    <p>
    <img src="oapc_by_time.png" width=400px />
    <img src="oa_bar_chart.png"  width=450px />
    <figcaption><strong>Figure 2.</strong> Open Access Performance Over Time and Comparison With Peer Institutions.</figcaption>
</figure>

### Funders and Open Access Status of Funded Outputs

All DOIs identified for {{ focus_year.year }} were matched to funder names provided in Crossref metadata. For DOIs matched to each funder DOI open access status was determined. The number of overall outputs and those open access as well as the proportion is given. This analysis is dependent on the quality of Crossref funder metadata provided by publishers. Currently this is patchy, so numbers should be treated as lower-bound estimates. The percentage of open access is generally reliable as an estimate.


{% set table_columns = oa_table_by_year[0].keys() %}
<table>
    <caption><strong>Table 1.</strong> Open Access by Type and Year of Publication for {{ metadata.entity_name }}</caption>
    <thead>
        <tr>
            {% for col in table_columns %}
                {% if col == 'Year' %}
                <th text-align=left>{{ col }}</th>
                {% else %}
                <th>{{ col }}</th>
                {% endif %}
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for row in oa_table_by_year[1:] %}
            <tr>
                {% for col in table_columns %}
                    {% if col == 'Year' %}
                    <td text-align=left>{{ row[col] }}</td>
                    {% else %}
                    <td>{{ row[col] }}</td>
                    {% endif %}
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>

<figure>
    <p>
    <img src="funder_bar_chart.png" width=600 />
    <figcaption><strong>Figure 3.</strong> Funders and Open Access Status for Outputs Published in {{ focus_year.pubished_year }}.</figcaption>
</figure>

### Citations

Citation data is obtained from the Open Citations Corpus which has some limitations as some large publishers do not contribute to this open data source. We therefore do not present counts here but use this as a sample to calculate citations per article and examine the open access citation advantage for specific types of access. These values can be quite volatile, especially for access types with limited numbers so trends over time are the most useful comparisons to make. It is not straightforward to draw a causal conclusion between access type and citation advantage. It can be useful to examine the relative citation advantage across access types however. 

<figure>
    <p>
    <img src="cite_per-article.png" width=450px />
    <img src="cite_bar.png" width=350px />
    <figcaption><strong>Figure 4.</strong> Citations per output for different classes of access for {{ metadata.entity_name }} publications and the relative citation advantage per article by access type in {{ focus_year.published_year }}.</figcaption>
</figure>

## Methodology and Further References

A detailed description of the methodology used to generate the data, including the specific details of queries and processing can be found in the Supplementary Methodology section of Huang et al (2020) which is the source of the information provided here. 

### Data Gathering

Our pragmatic approach is to include the widest coverage of outputs for each of the universities under consideration. This implies defining a target population for all potential research outputs, which is no trivial task. For this analysis, we consider the set of all research outputs with Crossref DOIs as this target population. This is identified as the most practical approach that allows tracking and disambiguation of research objects using persistent identifiers. At the same time, it provides processes for both the standardisation of publication dates and the use of Unpaywall's OA information.

API queries were ran against Web of Science (via Organisation-Enhance name search) and Scopus (via Affiliation ID search) to extract metadata of all outputs affiliated to each university for the time frames 2000 to 2018. These are matched against outputs from a Microsoft Academic snapshot to result in a comprehensive set of outputs for each university. Subsequently, these are filtered down to include only objects with Crossref DOIs. This current set of universities is then further expanded to include additional universities from countries that had low representations in the initial sample, and goes through the same data collection process.

All collected Crossref DOIs are matched against an Unpaywall database snapshot for their open access information. This allows us to calculate total numbers for various modes of open access (e.g., number of Gold OA publications) for each university across different timeframes (using the "year" component of the Crossref "issued date" field). The Unpaywall information used to determine various open access modes is as displayed in Figure 1. Crossref DOIs not found in Unpaywall are defaulted to be not open access and Crossref DOIs that do not have an "issued date" are removed from the process.

### Open Access Status

While there is a large body of literature on OA, the definitions of OA are quite diverse in detail. Policy makers and researchers may choose to use the OA terminology in different ways. Popular discrepancies include the coverage of journals without formal license of reuse and articles only accessible via academic social medias or illegal pirate sites. We use the following definitions for the modes of OA determined as part of our data workflow:

- **Total OA:** A research output that is free to read online, either via the publisher website or in an OA repository.
- **Gold:** A research output that is either published in a journal listed by the Directory of Open Access Journals (DOAJ), or (if journal not in DOAJ) is free to read via publisher with any open license.
- **Gold DOAJ:** A research output that is published in a journal listed by DOAJ.
- **Hybrid:** A research output that is published in a journal not listed by DOAJ, but is free to read from publisher with an open license.
- **Bronze:** A research output that is free to read online via publisher without an open license.
- **Green:** A research output that is free to read online via an OA repository.
- **Green Only:** A research output that is free to read online via an OA repository, but is not available for free via the publisher.
- **Green in Home Repo:** A research output that is free to read online via the matched affiliation's institional repository.

It should be noted that these definitions are not always mutually exclusive in coverage. For example, an article can be both Gold OA and Green OA. On the other hand, the set of all Gold OA and the set of all Green Only OA do not have any common element by definition.

