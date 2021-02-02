TEMPLATE = """<a href="{{ entry.link }}">{{ entry.safe_title }}</a>
<i>By</i>: <b>{{ entry.author }}</b>
{{ entry.safe_description }}
<i>Source</i>: <a href="{{ channel.link }}">{{ channel.safe_title }}</a>
"""
