---
layout: layout.liquid
title: Cooking Appliances
description: Professional-grade appliances to elevate your cooking game and save time in the kitchen.
permalink: /cooking-appliances/index.html
---

<section class="category-header">
  <div class="container">
    <h1 class="category-title">{{ title }}</h1>
    <p class="category-subtitle">{{ description }}</p>
  </div>
</section>

<main class="main">
  <div class="container">
    <div class="articles-grid">
      {% for product in products %}
        {% if product.category == "cooking-appliances" %}
          {% assign name = product.title | default: product.productName %}
          {% assign url  = product.articleLink | default: product.link | default: "#" %}
          {% assign text = product.excerpt | default: product.summary | default: product.text %}
          <article class="article">
            {% if product.image %}<img src="{{ product.image }}" alt="{{ name }}" class="article-image">{% endif %}
            <div class="article-content">
              <h2 class="article-title"><a href="{{ url }}">{{ name }}</a></h2>
              {% if product.dateUpdated %}<div class="article-meta">Updated: {{ product.dateUpdated }}</div>{% endif %}
              {% if text %}<p class="article-excerpt">{{ text }}</p>{% endif %}
              {% assign buy = product.amazonLink | default: product.link %}
              {% if buy %}<a href="{{ buy }}" class="amazon-link" target="_blank" rel="nofollow">Shop on Amazon</a>{% endif %}
            </div>
          </article>
        {% endif %}
      {% endfor %}
    </div>
  </div>
</main>
