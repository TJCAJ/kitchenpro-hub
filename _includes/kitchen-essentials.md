---
layout: layout.liquid
title: Kitchen Essentials
description: Must-have tools every kitchen needs.
permalink: /kitchen-essentials/index.html
---

<h1 class="category-title">{{ title }}</h1>
<p class="category-subtitle">{{ description }}</p>

<div class="articles-grid">
  {% for product in products %}
    {% if product.category == "kitchen-essentials" %}
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
