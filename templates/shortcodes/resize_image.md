{%- set lazy_loading = lazy_loading | default(value=true) -%}
{%- set width = width | default(value=1200) -%}
{%- set height = height | default(value=1200) -%}
{%- set op = op | default(value="fit") -%}
{%- set format = format | default(value="webp") -%}
{%- set quality = quality | default(value=75) -%}
{% set resized_img = resize_image(path=page.colocated_path~path, width=width, height=height, op=op, format=format, quality=quality) %}
{{ resized_img.url }}