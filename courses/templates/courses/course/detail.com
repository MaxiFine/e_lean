{% extends "base.html" %}
{% block title %}
{{ object.title }}
{% endblock %}
{% block content %}
{% with subject=object.subject %}
<h1>
{{ object.title }}
</h1>
<div class="module">
<h2>Overview</h2>
<p>
<a href="{% url "course_list_subject" subject.slug %}">
{{ subject.title }}</a>.
{{ object.modules.count }} modules.
Instructor: {{ object.owner.get_full_name }}
</p>
{{ object.overview|linebreaks }}
</div>
{% endwith %}
{% endblock %}