---
layout: layout.liquid
title: Reviews
description: Expert reviews and buying guides for the best kitchen tools and appliances.
permalink: /reviews/index.html
---

<h1 class="category-title">{{ title }}</h1>
<p class="category-subtitle">{{ description }}</p>

{% assign categories = "kitchen-essentials,cooking-appliances,bakeware,storage-solutions" | split: "," %}

{% for category in categories %}
  <h2 style="margin-top:2rem; text-transform:capitalize;">
    {{ category | replace: "-", " " }}
  </h2>
  <div class="articles-grid">
    {% for product in products %}
      {% if product.category == category %}
        {% assign name = product.title | default: product.productName %}
        {% assign url  = product.articleLink | default: product.link | default: "#" %}
        {% assign text = product.excerpt | default: product.summary | default: product.text %}
        <article class="article">
          {% if product.image %}<img src="{{ product.image }}" alt="{{ name }}" class="article-image">{% endif %}
          <div class="article-content">
            <h2 class="article-title"><a href="{{ url }}">{{ name }}</a></h2>
            {% if text %}<p class="article-excerpt">{{ text }}</p>{% endif %}
            {% if product.rating %}
              <div class="article-meta">
                {% for i in (1..product.rating) %}★{% endfor %}
              </div>
            {% endif %}
          </div>
        </article>
      {% endif %}
    {% endfor %}
  </div>
{% endfor %}
