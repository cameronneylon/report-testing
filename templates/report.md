{% import "macros.md" as helper with context %}
<style>
@font-face {
    font-family: Gelasio;
    src: url('/Users/ana/dev/oa_reporting_demo/fonts/Gelasio-Regular.ttf');
}
@font-face {
    font-family: DancingScript;
    src: url('/Users/ana/dev/oa_reporting_demo/fonts/DancingScript-VariableFont:wght.ttf');
}
@font-face {
    font-family: Baskerville;
    src: url('/Users/ana/dev/oa_reporting_demo/fonts/LibreBaskerville-Regular.ttf');
}
@page {
    size: letter portrait;
    margin: 3cm;
}
body {
    font-family: Gelasio, serif;
}
h1 { 
    font-size: 20pt;
}
h2 { 
    font-size: 18pt;
}
h3 { font-size: 16pt ; } 
h4 { font-size: 14pt ; } 
p { font-size: 12pt; }
</style>

{% set metadata = load_json("metadata.json") %}

## {{ metadata.entity_name }} - Open Access Report

<i>{{ metadata.entity_name }}, GRID: {{ fn_params('oagen.compare_grid', 'grid_id') }}, Report generated on {{ helper.created_at() }}</i>

### Analysis

#### Analysis of bibliographic output types

All collected outputs matching the search terms above were deduplicated by DOI and the type determined from Crossref metadata. This can give a broad view of the growth of outputs over time and an overview of the diversity and types of outputs. The Crossref metadata on type is patchy and not always consistent so this should be taken as an overview but it should be reasonably consistent.  Growth of the bibliographic sources themselves will be a contributor to the growth in outputs.

<img src="output_types_by_time.png" width="300" /><img src="output_types_pie.png" width="300" />

### Citations

<img src="citations_by_time.png" width="300" /><img src="citations_ppn_by_time.png" width="300" />

### Open Access Status

In the year {{ fn_params('oagen.compare_grid', 'focus_year') }}, open access percent was {{ load_json('focus_year_oa_stats.json').percent_OA }}.

![Open Access By Time](oapc_by_time.png)

![Open Access By Time](oapc_comp_by_time.png)

