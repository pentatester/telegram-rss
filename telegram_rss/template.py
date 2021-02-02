TEMPLATE = """<a href="{{ entry.link }}">{{ entry.safe_title }}</a>
<i>{{ author }}</i>: <b>{{ entry.author }}</b>
{{ entry.safe_description }}
<i>{{ source }}</i>: <a href="{{ channel.link }}">{{ channel.safe_title }}</a>
"""
