SELECT
    (SELECT COUNT(*) FROM public.stg_pedido)
        AS pedidos_origem,

    (SELECT COUNT(*) FROM public.fato_pedido)
        AS pedidos_carregados,

    (SELECT COUNT(DISTINCT numero_pedido)
     FROM public.fato_pedido)
        AS pedidos_distintos,

    (SELECT COUNT(*) FROM public.fato_pedido
     WHERE sk_loja IS NULL
        OR sk_categoria IS NULL
        OR sk_tempo_pedido IS NULL
        OR sk_tempo_entrega IS NULL)
        AS chaves_nulas,

    (SELECT COUNT(*) FROM public.dim_loja)
        AS total_lojas,

    (SELECT COUNT(*) FROM public.dim_categoria)
        AS total_categorias,

    (SELECT COUNT(*) FROM public.dim_tempo)
        AS total_datas;