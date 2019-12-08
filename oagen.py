# -*- coding: utf-8 -*-
"""Updated Open Access Report Generation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Eh6LqIRRUVNpmiauUd17VSPpyocLh1pM

"""

## General incantations ##
from collections import OrderedDict
#from google.colab import auth
from pathlib import Path
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pydata_google_auth

plt.style.use('seaborn-white')
sns.set_context("talk")

import warnings
warnings.filterwarnings('ignore')


def do_everything(batch):
    #auth.authenticate_user()

    SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive',
]

    credentials = pydata_google_auth.get_user_credentials(
            SCOPES,
            )

    """# Entities and key parameters for the report"""
    
    report_grids = [
            'grid.7340.0'
            ]
    grid_ids = "','".join([g for g in report_grids])
    
    comparison_groups = [
            'us_ucs', 
            'uk_rus',
            'au_go8'
            ]
    group_ids = "','".join([g for g in comparison_groups])
    
    focus_year = 2017
    
    """# Collect Data from BigQuery"""
    
    #@title
    ## Collect data ##
    project_id = 'open-knowledge-datasets'
    
    grid_sql = f'''
    SELECT
     id,
     name,
     country,
     region,
     subregion,
     years.published_year,
     years.total,
     years.total_oa,
     (SELECT count from UNNEST(years.gold) where status = true) as gold,
     (SELECT count from UNNEST(years.green) where status = true) as green,
     (SELECT count from UNNEST(years.green_only) where status = true) as green_only,
     (SELECT count from UNNEST(years.hybrid) where status = true) as hybrid,
     (SELECT count from UNNEST(years.bronze) where status = true) as bronze,
     years.percent_OA,
     years.percent_green,
     years.percent_green_only,
     years.percent_gold,
     years.percent_gold_doaj,
     years.percent_hybrid,
     years.percent_bronze,
     years.total_citations,
     years.articles_with_citations,
     years.citations_per_article,
     years.citations_per_citated_article,
     (SELECT citations from UNNEST(years.oa_citations) where oa_status = "Open Access") as citations_oa_articles,
     (SELECT count from UNNEST(years.output_types) WHERE type = "journal_articles") as journal_articles,
     (SELECT count from UNNEST(years.output_types) WHERE type = "book_sections") as book_sections,
     (SELECT count from UNNEST(years.output_types) WHERE type = "authored_books") as authored_books,
     (SELECT count from UNNEST(years.output_types) WHERE type = "edited_volumes") as edited_volumes,
     (SELECT count from UNNEST(years.output_types) WHERE type = "proceedings_article") as proceedings_articles,
     (SELECT count from UNNEST(years.output_types) WHERE type = "reports") as reports,
     (SELECT count from UNNEST(years.output_types) WHERE type = "datasets") as datasets,
     (SELECT count from UNNEST(years.output_types) WHERE type = "other_outputs") as other_outputs 
    FROM `open-knowledge-datasets.outputs_2019_Oct.institutions`, UNNEST(years) as years 
    WHERE 
      years.published_year > 2000 and 
      years.published_year < 2019 and
      years.total > 100
    '''
    
    outputs = pd.io.gbq.read_gbq(grid_sql, project_id=project_id, credentials=credentials, dialect = 'standard', verbose=False)
    
    group_sql = f'''
    SELECT
     id,
     name,
     years.published_year,
     years.total,
     years.total_oa,
     (SELECT count from UNNEST(years.gold) where status = true) as gold,
     (SELECT count from UNNEST(years.green) where status = true) as green,
     (SELECT count from UNNEST(years.green_only) where status = true) as green_only,
     (SELECT count from UNNEST(years.hybrid) where status = true) as hybrid,
     (SELECT count from UNNEST(years.bronze) where status = true) as bronze,
     years.percent_OA,
     years.percent_green,
     years.percent_green_only,
     years.percent_gold,
     years.percent_gold_doaj,
     years.percent_hybrid,
     years.percent_bronze,
     years.total_citations,
     years.articles_with_citations,
     years.citations_per_article,
     years.citations_per_citated_article,
     (SELECT count from UNNEST(years.output_types) WHERE type = "journal_articles") as journal_articles,
     (SELECT count from UNNEST(years.output_types) WHERE type = "book_sections") as book_sections,
     (SELECT count from UNNEST(years.output_types) WHERE type = "authored_books") as authored_books,
     (SELECT count from UNNEST(years.output_types) WHERE type = "edited_volumes") as edited_volumes,
     (SELECT count from UNNEST(years.output_types) WHERE type = "reports") as reports,
     (SELECT count from UNNEST(years.output_types) WHERE type = "datasets") as datasets,
     (SELECT count from UNNEST(years.output_types) WHERE type = "other_outputs") as other_outputs 
    
    FROM `open-knowledge-datasets.outputs_2019_Oct.groups`, UNNEST(years) as years 
    WHERE 
      years.published_year > 2000 and 
      years.published_year < 2019 and
      id in ('{group_ids}')
    '''
    
    groups = pd.io.gbq.read_gbq(group_sql, project_id=project_id, dialect = 'standard', verbose=False)
    
    country_list = outputs[outputs['id'].isin(report_grids)].country.unique()
    country_ids = "','".join([g for g in country_list])
    
    country_sql= f'''
    SELECT
     id,
     id as name,
     years.published_year,
     years.total,
     years.total_oa,
     (SELECT count from UNNEST(years.gold) where status = true) as gold,
     (SELECT count from UNNEST(years.green) where status = true) as green,
     (SELECT count from UNNEST(years.green_only) where status = true) as green_only,
     (SELECT count from UNNEST(years.hybrid) where status = true) as hybrid,
     (SELECT count from UNNEST(years.bronze) where status = true) as bronze,
     years.percent_OA,
     years.percent_green,
     years.percent_green_only,
     years.percent_gold,
     years.percent_gold_doaj,
     years.percent_hybrid,
     years.percent_bronze,
     years.total_citations,
     years.articles_with_citations,
     years.citations_per_article,
     years.citations_per_citated_article
    FROM `open-knowledge-datasets.outputs_2019_Oct.countries`, UNNEST(years) as years 
    WHERE 
      years.published_year > 2000 and 
      years.published_year < 2019 and
      id in ('{country_ids}')
    '''
    
    countries = pd.io.gbq.read_gbq(country_sql, project_id=project_id, dialect = 'standard', verbose=False)
    countries.name = countries['id']
    
    funder_sql = f'''
    SELECT
      id,
      grids.name,
      years.published_year as year,
      funders.name as funder_name,
      funders.count as funder_count,
      funders.oa as funder_oacount
    FROM `open-knowledge-datasets.outputs_2019_Oct.institutions` as grids, UNNEST(years) as years, UNNEST(funders) as funders 
    WHERE 
      years.published_year > 2000 and 
      years.published_year < 2019 and
      id in ('{grid_ids}')
    '''
    
    funding = pd.io.gbq.read_gbq(funder_sql, project_id=project_id, dialect = 'standard', verbose=False)
    
    """# Data Cleanup"""
    
    ## Calculate citations per OA article
    outputs['citations_per_oa_article'] = outputs['citations_oa_articles'] / outputs['total_oa']
    
    ## Append outputs to groups ##
    groups = groups.append(outputs, ignore_index=True).drop_duplicates()
    groups = groups.append(countries, ignore_index=True).drop_duplicates()
    groups.sort_values(by=['id','published_year'])
    
    
    ## Melted (long form) dataframes ##
    
    melt = outputs.melt(
            id_vars = ['id', 'name', 'published_year', 'country', 'region', 'subregion'],
            var_name = 'variables'
            )
    
    melt_groups = groups.melt(
            id_vars = ['id', 'name', 'published_year'],
            var_name = 'variables'    
            )
    ## OA % over time ##
    oapctime_variables = ['percent_OA', 'percent_green', 'percent_gold', 'percent_hybrid', 'percent_bronze']
    
      ## OA % Bar chart ##
    oa_pc_bar = ['percent_bronze','percent_hybrid','percent_gold_doaj','percent_green_only' ]
    
    # Data cleanup required, mainly on country names #
    country_clean = { "country" : {
        "United Kingdom of Great Britain and Northern Ireland" : "United Kingdom",
        "Iran (Islamic Republic of)" : "Iran",
        "Korea, Republic of" : "South Korea",
        "Taiwan, Province of China" : "Taiwan"
        }
        }
    outputs.replace(to_replace = country_clean, inplace=True)
    outputs.loc[outputs.country.isin(['Canada', 'United States of America']), 'region'] = 'North America'
    outputs = outputs.replace('Americas', 'Latin America')

    for grid in report_grids:
        subregion = outputs[outputs.id == grid]['subregion'].values[0]
        country = [outputs[outputs.id==grid]['country'].values[0]]
        comparison = comparison_groups + country
    
        ## Output types and numbers over time ##
        type_variables = ['total', 'journal_articles', 'proceedings_articles', 'book_sections', 'authored_books', 'edited_volumes'
              ]
    
        type_names = ['Total Outputs' , 'Journal Articles', 'Conference Proceedings','Book Sections', 'Books', 'Edited Volumes' 
                ]
    
        output = sns.FacetGrid(melt[(melt.variables.isin(type_variables)) & (melt.id==grid)].sort_values('published_year'),
                col="name", 
                hue ='variables', hue_order = type_variables,#, palette = oa_palette,
                height=5, aspect=1)
        output.map(plt.plot, "published_year", "value", marker = "o")
        output.set(xlabel='Published Year', ylabel= 'Number', yscale='log', title=None )
        l = output.ax.legend(labels = type_names,
                bbox_to_anchor=(1,0.8))
   
        batch.save_matplotlib_plt(output, "%s_output_types_by_time.png" % grid)
    
        ## Pie chart of output types for $year ##
        pie_variables = type_variables[1:len(type_variables)]
        pie_names = type_names[1:len(type_names)]
    
        data = melt[(melt.variables.isin(pie_variables)) & (melt['id']==grid) & (melt.published_year==focus_year)][['variables', 'value']]
        data = data.set_index('variables').reindex(pie_variables)

        print(data)
        batch.save_plain_text(data.to_html(), "pie_variables.html")
        batch.save_plain_text(data.to_json(), "pie_variables.json")
        batch.save_dict_as_json(data.to_dict(), "pie_variables_dict.json")

        outputs_pie = data.plot.pie(y='value', startangle=90, labels=None, legend=True, colors = sns.color_palette()[1:])
        outputs_pie.set_ylabel('')
        my_circle=plt.Circle( (0,0), 0.4, color='white')
        p=plt.gcf()
        p.gca().add_artist(my_circle)
        l = outputs_pie.legend(labels = pie_names,
              bbox_to_anchor=(1,0.8))
        #plt.show()
        batch.save_matplotlib_plt(p, "%s_output_types_pie.png" % grid)
    
        ## Citations over time ##
        cited_variables = ['total', 'total_citations', 'articles_with_citations',  
              ]
    
        cited_names = ['Total Outputs' , 'Total Citations', 'Cited Articles' 
              ]
    
        citations = sns.FacetGrid(melt[melt.variables.isin(cited_variables)][melt.id==grid].sort_values('published_year'),
              col="name", 
              hue ='variables', hue_order = cited_variables,#, palette = oa_palette,
              height=5, aspect=1)
        citations.map(plt.plot, "published_year", "value", marker = "o")
        citations.set(xlabel='Published Year', ylabel= 'Number', yscale='log', title=None )
        l = citations.ax.legend(labels = cited_names,
              bbox_to_anchor=(1,0.8))
    
        batch.save_matplotlib_plt(citations, "%s_citations_by_time.png" % str(grid))
    
        ## Citations per article##
        citedppn_variables = ['citations_per_article','citations_per_citated_article', 'citations_per_oa_article' 
                ]
    
        citedppn_names = ['Citations per Article' , 'Citations per Cited Article', 'Citations per OA Article'
                ]
    
        citationpa = sns.FacetGrid(melt[melt.variables.isin(citedppn_variables)][melt.id==grid].sort_values('published_year'),
              col="name", 
              hue ='variables', hue_order = citedppn_variables, 
              height=5, aspect=1)
        citationpa.map(plt.plot, "published_year", "value", marker = "o")
        citationpa.set(xlabel='Published Year', ylabel= 'Number of Citations', title=None )
        l = citationpa.ax.legend(labels = citedppn_names,
              bbox_to_anchor=(1,0.8))
    
        batch.save_matplotlib_plt(citationpa, "%s_citations_ppn_by_time.png" % str(grid))
    
        ## Percent OA over time ##
        variables = ['percent_OA', 'percent_green', 'percent_gold_doaj', 'percent_hybrid', 'percent_bronze']

        names = ['Total OA' , 'Green', 'Gold (DOAJ)', 'Hybrid', 'Bronze' 
              ]
        oa_palette = ['black', 'darkgreen', 'gold', 'orange', 'brown']
    
        pcoa = sns.FacetGrid(melt[melt.variables.isin(variables)][melt.id==grid].sort_values('published_year'),
              col='name', 
              hue ='variables', hue_order = variables, palette = oa_palette,
              height=5, aspect=1)
        pcoa.map(plt.plot, 'published_year', 'value', marker = "o")
        pcoa.set(xlabel='Published Year', ylabel= '% of Total Outputs', title=None )
        l = pcoa.ax.legend(labels = names,
              bbox_to_anchor=(1,0.8))
    
        batch.save_matplotlib_plt(pcoa, "%s_oapc_by_time.png" % str(grid))
    
        ## Percent OA Comparisons ##
        names = ['UC System', 'Russell Group', 'Group of Eight']
        oacomp = sns.FacetGrid(melt_groups[(melt_groups.variables.isin(variables)) & (melt_groups.id.isin(comparison_groups))].sort_values('published_year'),
              col='name', #col_order = comparison_groups,
              height = 4, aspect=1,
              hue ='variables', hue_order = variables, palette = oa_palette)
        oacomp.map(plt.plot, 'published_year', 'value').set_titles('{col_name}')
        oacomp.set(xlabel='Published Year', ylabel= '% of Total Outputs')
        #l = g.ax.legend(labels = names,
        #                bbox_to_anchor=(1,0.8))
    
        batch.save_matplotlib_plt(oacomp, "%s_oapc_comp_by_time.png" % str(grid))
    
        ## OA in the region ##
        region_oa_scatter = sns.relplot(x="percent_green", y="percent_gold", data=outputs[outputs.subregion==subregion][outputs.published_year==focus_year], 
                size="total", sizes = (50,500), hue = "country", alpha=0.7)
        sns.scatterplot(x="percent_green", y="percent_gold", data=outputs[outputs['id']==grid][outputs.published_year==focus_year], 
              color="black", s=200, marker = 'X', legend = False)
        region_oa_scatter = region_oa_scatter.set(xlim=(0,100),ylim=(0,100), xlabel='Total Green %', ylabel = 'Total Gold %')
    
        batch.save_matplotlib_plt(region_oa_scatter, "%s_region_oa_map.png" % str(grid))
    
        ## Global OA map ##
        global_oa = sns.relplot(x="percent_green", y="percent_gold", data=outputs[outputs.published_year==focus_year], 
              size = 'total', sizes = (50,500),
              hue = 'region', alpha=0.6)
        sns.scatterplot(x="percent_green", y="percent_gold", data=outputs[outputs['id']==grid][outputs.published_year==focus_year], 
              color="black", s=200, marker = 'X', legend = False)
        global_oa = global_oa.set(xlim=(0,100), ylim=(0,100), xlabel='Total Green %', ylabel = 'Total Gold %')
    
        batch.save_matplotlib_plt(global_oa, "%s_global_oa_map.png" % str(grid))

        ## Open Access Path ##
        pathmap = sns.relplot(x="percent_green", y="percent_gold", data=groups[groups.id.isin([grid, *comparison])].sort_values('published_year'), 
              #size = 'total', sizes = (50,500),
              hue = 'name', alpha=0.6)
        sns.lineplot(x="percent_green", y="percent_gold", data=groups[groups.id.isin([grid, *comparison])].sort_values('published_year'), 
              hue = 'name', legend = False, sort=False)
        pathmap = pathmap.set(xlim=(0,80), ylim=(0,50), xlabel='Total Green %', ylabel = 'Total Gold %')
        batch.save_matplotlib_plt(pathmap,  '%s_oa_path_comparison.png' % str(grid))
    
        ##OA Types Bar Chart##
        data = groups[(groups.published_year==focus_year) & (groups.id.isin([grid, *comparison]))]
        data = data.set_index('id').reindex([grid, *comparison])
        ax = data[['percent_bronze','percent_hybrid','percent_gold_doaj','percent_green_only' ]].plot(
              kind='bar', stacked=True, colors=['brown','orange','gold','green'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xticklabels([data[data.index==grid]['name'].iloc[0] for grid in [grid, *comparison]])
        ax.set(ylabel ='Percent of all outputs', xlabel=None)
        l = ax.legend(labels = ['Bronze %' , 'Hybrid %','Gold (DOAJ) %', 'Green only %'],
              loc='upper center', bbox_to_anchor=(1.45, 0.8))
    
        batch.save_matplotlib_plt(ax.figure, '%s_oa_type_comparison.png' % str(grid))
    
    
        ## New OA funder graph ##
        fundergraph, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize = (8,4))
        data = funding[(funding.id==grid) & (funding.year==focus_year)].sort_values('funder_count', ascending=False)[0:10]
    
        data = data.melt(id_vars = ['id', 'name','year', 'funder_name'],
              var_name = 'variables')
        data = data.sort_values('value', ascending=False)
        p = sns.catplot(y="funder_name", x="value", hue="variables", kind="bar", data=data[0:20], ax = axes[0])
        axes[0].set(ylabel = None, xlabel='Number of Outputs')
        handles, labels = axes[0].get_legend_handles_labels()
        l = axes[0].legend(handles, ['Total', 'Open Access'])
    
        data = funding[funding.id==grid][funding.year==focus_year]
        data['percent_by_funder'] = data['funder_oacount']/data['funder_count']*100
        data = data.sort_values('funder_count', ascending=False)
        sns.catplot(y="funder_name", x="percent_by_funder", kind="bar", data=data[0:10], color='blue', ax = axes[1])
        axes[1].set(ylabel =None, xlabel='% Open Access')
    
        batch.save_matplotlib_plt(fundergraph, "%s_oapc_by_funder.png" % str(grid))
   



        # outputs[(outputs.country=='Canada') & (outputs.percent_green > 30) & (outputs.published_year == 2017)][['name', 'percent_green', 'percent_gold', 'percent_OA']].sort_values('percent_green')


if __name__=="__main__":
    do_everything(None)
