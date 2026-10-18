1,python manage.py startapp accounts
2,project/settings.py  ---> add app : app_name='accounts'
3,project/urls.py: path('accounts/',include('accounts.urls'))
4,accounts/urls.py   app_name='accounts'    path("",include('django.contrib.auth.urls)
5,make new file: Blog/accounts/registrations/login.html:
    {% extends 'blogs_app/base.html' %}
    {% block content %}
{% if form.errors %}
<p>the name or password is not match.try again.</p>
{% endif %}
<form action="{% url 'accounts:login' %}" method='post'>
{% csrf_token %}
{{ form.as_div }}
<button type='submit'>login please</button>
</form>
{% endblock content %}
