# -*- coding: utf-8 -*-
"""Institutional Open Access Report Generation v0.1

Code for the generating of observatory.academy or COKI
institutional reports using precipy.
"""

import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydata_google_auth
import seaborn as sns
import json

from academic_observatory.analysis import charts, helpers

plt.style.use('seaborn-white')
sns.set_context("talk")

warnings.filterwarnings('ignore')

id_vars = ['id', 'name', 'published_year',
           'country', 'country_code', 'region', 'subregion',
           'Total Publications', 'Year of Publication', 'University Name', 'Region', 'Country']

project_id = 'coki-scratch-space'

HDF5_CANONICAL_FILENAME = "store.h5"


def get_data(af, current_table,
                          project_id=project_id,
                          focus_year=2018, 
                          year_range: tuple=(2000, 2019)):

    SCOPES = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/drive',
    ]

    credentials = pydata_google_auth.get_user_credentials(
        SCOPES,
    )

    template_sql = '''
SELECT
    id,
    name,
    country,
    country_code,
    region,
    subregion,
    published_year,
    combined.total as total,
    combined.oa as total_oa,
    combined.green as green,
    combined.gold as gold,
    combined.gold_just_doaj as gold_just_doaj,
    combined.hybrid as hybrid,
    combined.bronze as bronze,
    combined.green_only as green_only,
    combined.green_in_home_repo as green_in_home_repo,
    combined.total_citations as total_citations,
    combined.articles_with_citations as cited_articles,
    combined.total_oa_citations as oa_citations,
    combined.total_gold_citations as gold_citations,
    combined.total_green_citations as green_citations,
    combined.total_hybrid_citations as hybrid_citations

FROM
    `{}` as institutions,
    UNNEST(years) as years

WHERE
    years.published_year > 2000 and
    years.published_year < 2020
'''

    institutions_sql = template_sql.format(current_table)
    institutions = pd.io.gbq.read_gbq(institutions_sql,
                                      project_id=project_id,
                                      credentials=credentials,
                                      dialect='standard',
                                      verbose=False)

    helpers.calculate_percentages(institutions,
                                  ['total_oa', 'green', 'gold', 'gold_just_doaj',
                                   'hybrid', 'bronze', 'green_only', 'green_in_home_repo'],
                                  'total')
    helpers.clean_geo_names(institutions)
    helpers.nice_column_names(institutions)

    template_sql = '''
SELECT
  id,
  years.published_year as published_year,
  funders.name as name,
  funders.count as count,
  funders.oa as oa,
  funders.green as green,
  funders.gold as gold

FROM `{}`,
  UNNEST(years) as years,
  UNNEST(years.combined.funders) as funders

WHERE
  years.published_year = {}

ORDER BY published_year DESC, count DESC
'''
    funders_sql = template_sql.format(current_table, focus_year)
    funders = pd.io.gbq.read_gbq(funders_sql,
                                 project_id=project_id,
                                 credentials=credentials,
                                 dialect='standard',
                                 verbose=False)
    helpers.calculate_percentages(funders,
                                  ['oa', 'green', 'gold'],
                                  'count')
    helpers.nice_column_names(funders)

    template_sql = '''
SELECT
  id,
  years.published_year as published_year,
  type.type as type,
  type.total as total,
  type.oa as oa,
  type.green as green,
  type.gold as gold

FROM `{}`,
  UNNEST(years) as years,
  UNNEST(years.combined.output_types) as type

WHERE
  years.published_year > {} AND
  years.published_year < {}

ORDER BY published_year DESC
'''
    type_sql = template_sql.format(current_table, *year_range)
    output_types = pd.io.gbq.read_gbq(type_sql,
                                      project_id=project_id,
                                      credentials=credentials,
                                      dialect='standard',
                                      verbose=False)
    helpers.calculate_percentages(output_types,
                                  ['oa', 'green', 'gold'],
                                  'total')
    helpers.clean_output_type_names(output_types)
    helpers.nice_column_names(output_types)
    
    with pd.HDFStore(HDF5_CANONICAL_FILENAME) as store: # write directly to the CACHE file location
        store['institutions'] = institutions
        store['funders'] = funders
        store['outputs_types'] = output_types
    af.add_existing_file(HDF5_CANONICAL_FILENAME, remove=True)


def generate_table_data(batch,
                        title,
                        df: pd.DataFrame,
                        identifier: str,
                        columns: list,
                        identifier_column: str = 'id',
                        sort_column: str = 'Year of Publication',
                        sort_ascending: bool = True,
                        decimals: int = 0,
                        short_column_names: list = None,
                        column_alignments = None) -> dict:

    table_data = pd.DataFrame()
    df = df[df[identifier_column] == identifier]
    df.sort_values('Year of Publication', inplace=True)
    for i, column in enumerate(columns):
        col_data = df[column]
        if short_column_names:
            column = short_column_names[i]
        if col_data.dtype == 'float64':
            col_data = np.int_(col_data.round(decimals=decimals))
        table_data[column] = col_data
    table_data.sort_values(sort_column, ascending=sort_ascending, inplace=True)
    table_data_list =  table_data.to_dict(orient='records')
    
    if short_column_names:
        columns = short_column_names
    if not column_alignments:
        column_alignments = ['center'] * len(columns)
    column_list = [ {'name' : name, 'alignment' : alignment} for name, alignment in zip(columns, column_alignments)]
    return {'title': title,
            'columns': column_list,
            'rows': table_data_list}


def get_gcp_credentials():
    SCOPES = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/drive',
    ]

    credentials = pydata_google_auth.get_user_credentials(
        SCOPES,
    )
    return credentials


def plot_graphs(batch,
              identifier: str,
              comparison: list,
              focus_year: int,
              year_range: tuple = (2000, 2019)):

    store_filepath = batch.path_to_cached_file(HDF5_CANONICAL_FILENAME, "get_data")
    print(store_filepath)
    with pd.HDFStore(store_filepath) as store: # write directly to the CACHE file location
        institutions = store['institutions']
        funders = store['funders']
        output_types = store['outputs_types']

    # Basic Report Metadata
    metadata = {'entity_name': helpers.id2name(institutions, identifier),
         'identifier': identifier,
         'year': focus_year,
         'year_range': year_range}

    for f in batch.generate_file('metadata.json'):
        json.dump(metadata, f)

    # Focus Year Metadata
    focus_data = institutions[(institutions.id == identifier) &
                              (institutions.published_year == focus_year)]
    d = focus_data.to_dict(orient='records')[0]
    for k in d.keys():
        if type(d.get(k)) == float:
            d[k] = np.round(d.get(k), decimals=1)
    
    for f in batch.generate_file('focus_year_data.json'):
        json.dump(d, f)

    # Outputs and Output Types
    outputs_over_time = charts.OutputTypesTimeChart(output_types,
                                                    identifier,
                                                    year_range)
    outputs_over_time.process_data()
    output_types_graph = outputs_over_time.plot()
    output_types_graph.savefig('outputs_time_chart.png', bbox_inches='tight', dpi=300)
    batch.add_existing_file('outputs_time_chart.png', remove=True)

    outputs_pie = charts.OutputTypesPieChart(output_types,
                                         identifier,
                                         focus_year)
    outputs_pie.process_data()
    outputs_pie_graph = outputs_pie.plot()
    outputs_pie.watermark('assets/coki_small.png', xpad=100)
    outputs_pie_graph.savefig('outputs_pie_chart.png', bbox_inches='tight', dpi=300)
    batch.add_existing_file('outputs_pie_chart.png', remove=True)

    # OA Values over time
    oa_columns = ['Year of Publication',
                  'Total Publications',
                  'Open Access (%)',
                  'Total Gold OA (%)',
                  'Total Green OA (%)',
                  'Gold in DOAJ (%)',
                  'Hybrid OA (%)',
                  'Bronze (%)'
                  ]

    short_column_names = ['Year',
                          'Total',
                          'OA (%)',
                          'Gold OA (%)',
                          'Green OA (%)',
                          'DOAJ Journals (%)',
                          'Hybrid OA (%)',
                          'Bronze (%)'
                          ]

    oa_table_data = generate_table_data(batch,
                                        f"Open Access by Type and Year of Publication for {metadata.get('entity_name')}", 
                                        institutions,
                                        identifier,
                                        oa_columns,
                                        sort_column='Year',
                                        short_column_names=short_column_names)
    for f in batch.generate_file('oa_table_by_year.json'):
        json.dump(oa_table_data, f)

    # Percent OA over time
    oa_progress = charts.OApcTimeChart(institutions,
                                                 identifier,
                                                 year_range,
                                                 )
    oa_progress.process_data()
    oa_progress_chart = oa_progress.plot()
    oa_progress_chart.savefig("oapc_by_time.png", bbox_inches='tight', dpi=300)
    batch.add_existing_file("oapc_by_time.png", remove=True)

    # Global Comparison
    global_comparison = charts.ScatterPlot(institutions,
                                           'Total Green OA (%)', 
                                           'Total Gold OA (%)', 
                                           'Year of Publication', 2017,
                                            hue_column='Region', 
                                            size_column='Total Publications')
    global_comparison.process_data()
    global_comparison_chart = global_comparison.plot()
    global_comparison_chart.savefig("global_comparison.png", bbox_inches='tight', dpi=300)
    batch.add_existing_file("global_comparison.png", remove=True)

    # Time Path
    evolution = charts.TimePath(institutions,
                                year_range,
                                [identifier] + comparison,
                                'Total Green OA (%)', 
                                'Total Gold OA (%)' 
                                )
    evolution.process_data()
    evolution_chart = evolution.plot()
    evolution.watermark('assets/coki_small.png', xpad=-100)
    evolution_chart.savefig("timepath.png", bbox_inches='tight', dpi=300)
    batch.add_existing_file("timepath.png", remove=True)
    
    # OA Bar Chart
    if identifier in comparison:
        comparison.remove(identifier)
    oa_bar = charts.BarComparisonChart(institutions,
                                       [identifier] + comparison,
                                       focus_year)
    oa_bar.process_data()
    oa_bar_chart = oa_bar.plot()
    oa_bar.watermark('assets/coki_small.png', xpad=-100)
    oa_bar_chart.savefig("oa_bar_chart.png", bbox_inches='tight', dpi=300)
    batch.add_existing_file("oa_bar_chart.png", remove=True)

    # OA by Funder graph
    funder_bar = charts.FunderGraph(funders,
                                    identifier=identifier,
                                    focus_year=focus_year)
    funder_bar.process_data()
    funder_bar_chart = funder_bar.plot()
    funder_bar.watermark('assets/coki_small.png', xpad=-1500)
    funder_bar_chart.savefig("funder_bar_chart.png", bbox_inches='tight', dpi=300)
    batch.add_existing_file("funder_bar_chart.png", remove=True)

    # Citation graphs
    for kind in ['count', 'per-article', 'advantage']:
        cite_count = charts.CitationCountTimeChart(institutions,
                                                   identifier,
                                                   year_range,
                                                   kind)
        d = cite_count.process_data()
        f = cite_count.plot()
        #f = cite_count.watermark('assets/coki_small.png', xpad=-600)
        fname = 'cite_' + kind + '.png'
        f.savefig(fname, bbox_inches='tight', dpi=300)
        batch.add_existing_file(fname, remove=True)

    cite_bar = charts.OAAdvantageBarChart(institutions,
                                          focus_year,
                                          identifier)
    d = cite_bar.process_data()
    f = cite_bar.plot()
    cite_bar.watermark('assets/coki_small.png', xpad=100)
    f.savefig('cite_bar.png', bbox_inches='tight', dpi=300)
    batch.add_existing_file('cite_bar.png', remove=True)
