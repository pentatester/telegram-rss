TEMPLATE = """<a href="{{ entry.link }}">{{ entry.safe_title }}</a>
<i>{{ author }}</i>: <b>{{ entry.author }}</b>
{% if entry.published %}<i>{{ published }}</i>: <b>{{ entry.published }}</b>{% endif %}
{{ entry.safe_description }}
<i>{{ source }}</i>: <a href="{{ channel.link }}">{{ channel.safe_title }}</a>
"""
