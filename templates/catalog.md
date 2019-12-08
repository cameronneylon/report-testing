<style>
    @page {
        size: letter portrait;
        margin: 2cm;
    }

    p {
        font-size: 12pt;
    }
</style>

## Welcome

This is an automatically generated catalog of the functions and assets that have been generated.

{% for k in keys %}
### Function: {{ k }}

{% if data[k].files is defined %}
{% for cn, info in data[k].files.items() %}
#### Generated file:  {{ cn }}

{% for kk, vv in info.items() -%}
     - {{ kk }}: {{ vv }}
{% endfor -%}

![Plot]({{ data[k].files[cn]['local_path'] }})
{% endfor %}
{% endif %}


{% endfor %}

