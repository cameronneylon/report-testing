{% macro created_at(fmt="%d %B %Y") -%}
{{ datetime.datetime.today().strftime(fmt) }}
{% endmacro -%}

{% macro tableize(table_data, table_number) -%}
<table>
    <caption><strong>Table {{table_number}}.</strong> {{ table_data.title }}</caption>
    <thead>
        <tr>
            {% for column in table_data.columns %}
                <th text-align={{column.alignment}}>{{ column.name }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for row in table_data.rows %}
            <tr style="background-color: {{ loop.cycle("white", "Gainsboro") }};">
                {% for column in table_data.columns %}
                    <td text-align={{column.alignment}}>{{ row[column.name] }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>
{% endmacro -%}
