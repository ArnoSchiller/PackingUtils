
import streamlit as st

from packutils.data.bin import Bin
from packutils.data.order import Order
from packutils.data.article import Article
from packutils.solver.palletier_wish_packer import PalletierWishPacker, PackerConfiguration
from packutils.eval.packing_evaluation import PackingEvaluation, PackingEvaluationWeights
from packutils.visual.packing_visualization import PackingVisualization

import matplotlib
matplotlib.use('Agg')

st.write("""# Packing Visualisation""")

max_bins = 2
bins = [Bin(800, 1, 500)
        for _ in range(max_bins)]
packer = PalletierWishPacker(bins=bins)

with st.expander("Order", expanded=True):
    num_articles = st.number_input(
        "Number of article types", value=1, step=1, min_value=1)
    order = Order(
        "Test",
        articles=[
            Article(f"Article {idx+1}", width=20,
                    length=1, height=20, amount=1)
            for idx in range(num_articles)
        ])
    _c1, _c2, _c3, _c4 = st.columns(4)
    for article in order.articles:
        article.article_id = _c1.text_input(
            key=f"{article.article_id}_id",
            label="Name", value=article.article_id, disabled=True)
        article.width = _c2.number_input(
            key=f"{article.article_id}_width",
            label="Width", min_value=10, max_value=500, step=1)
        article.height = _c3.number_input(
            key=f"{article.article_id}_height",
            label="Height", min_value=10, max_value=500, step=1)
        article.amount = _c4.number_input(
            key=f"{article.article_id}_amount",
            label="Amount", step=1, min_value=0)

    st.write(order)


if sum([a.amount for a in order.articles]) < 1:
    st.warning("No articles to pack.")
else:
    with st.expander("Scoring weights", expanded=False):
        _c1, _c2, _c3 = st.columns(3)
        item_distribution_weight = _c1.number_input(
            label="item_distribution", value=1.0
        )
        item_stacking_weight = _c2.number_input(
            label="item_stacking", value=1.0
        )
        item_grouping_weight = _c3.number_input(
            label="item_grouping", value=1.0
        )
        weights = PackingEvaluationWeights(
            item_distribution=item_distribution_weight,
            item_stacking=item_stacking_weight,
            item_grouping=item_grouping_weight
        )
        st.write(weights.__dict__)

    vis = PackingVisualization()
    eval = PackingEvaluation(weights)
    variant = packer.pack_variant(order)
    variants = [variant]

    configurations = PackerConfiguration.generate_random_configurations(
        30, bin_stability_factor=0.7,
        item_volumes=[a.width*a.length*a.height / bins[0].volume for a in order.articles])

    variants = packer.pack_variants(order=order, configs=configurations)

    scored_variants = [(eval.evaluate_packing_variant(vc[0]), vc)
                       for vc in zip(variants, configurations)]
    scored_variants = sorted(
        scored_variants, key=lambda x: x[0][0], reverse=True)
    for idx, (scores, (variant, config)) in enumerate(scored_variants):
        st.write(f"### Variant {idx+1} - Score:", scores[0])

        _c1, _c2 = st.columns(2)
        with _c1.expander("Configuration", expanded=False):
            st.write(config.__dict__)
        with _c2.expander("Score details", expanded=False):
            st.write(scores[1])

        for bin_idx, bin in enumerate(variant.bins):
            cols = st.columns(max_bins)
            cols[bin_idx].pyplot(vis.visualize_bin(bin, show=False))
