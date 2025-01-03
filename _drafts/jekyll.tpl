{% extends 'markdown.tpl' %}

{%- block header -%}
---
layout: post
categories: blog
author: Everett Robinson
---
{%- endblock header -%}

{% block input %}
{{ '{% highlight python %}' }}
{{ cell.source }}
{{ '{% endhighlight %}' }}
{% endblock input %}

{% block data_gif %} 
![gif]({{ output.metadata.filenames['image/gif'] | path2support }}) 
{% endblock data_gif %} 

{% block data_svg %} 
![svg]({{ output.metadata.filenames['image/svg+xml'] | path2support }}) 
{% endblock data_svg %} 

{% block data_png %} 
![png]({{ output.metadata.filenames['image/png'] | path2support }}) 
{% endblock data_png %} 

{% block data_jpg %} 
![jpeg]({{ output.metadata.filenames['image/jpeg'] | path2support }}) 
{% endblock data_jpg %} 

{% block markdowncell scoped %} 
{{ cell.source | wrap_text(80) }} 
{% endblock markdowncell %} 

{% block headingcell scoped %}
{{ '#' * cell.level }} {{ cell.source | replace('\n', ' ') }}
{% endblock headingcell %}
