<style>
    @page {
        size: letter landscape;
        margin: 2cm;
    }
</style>

## Welcome

This is some text.

Here is a list of keys:
{% for k in keys %}
### {{ k }}

{% if data[k].files is defined %}
{% for cn, info in data[k].files.items() %}
- {{ cn  }}
{% for kk, vv in info.items() -%}
     - {{ kk }}: {{ vv }}
{% endfor -%}
![Plot]({{ data[k].files[cn]['local_path'] }})
{% endfor %}
{% endif %}


{% endfor %}

