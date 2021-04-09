# # from unittest.mock import ANY

# # from freezegun import freeze_time
# from rest_framework import serializers, status
# from rest_framework.reverse import reverse

# from ..factories.trade import TradePostFactory


# def test_trade_post_list(api_client, django_assert_max_num_queries):
#     trade_posts = TradePostFactory.create_batch(10)

#     with django_assert_max_num_queries(2):
#         r = api_client.get(reverse('tradepost-list'), {'limit': 0})

#     assert r.status_code == status.HTTP_200_OK
#     assert len(r.data) == 10
#     assert r.data[0] == {
#         'uuid': str(trade_posts[0].uuid),
#         'created_at': serializers.DateTimeField().to_representation(trade_posts[0].created_at),
#         'updated_at': serializers.DateTimeField().to_representation(trade_posts[0].updated_at),
#         # 'owner': str(trade_posts[0].owner.pk),
#         'owner_role': trade_posts[0].owner_role,
#         'transaction_type': trade_posts[0].transaction_type.pk,
#         'currency': trade_posts[0].currency.pk,
#         'payment_method': trade_posts[0].payment_method.pk,
#         'exchange': trade_posts[0].exchange.pk,
#         'margin': trade_posts[0].margin,
#         'rate': trade_posts[0].rate,
#         'amount': trade_posts[0].amount,
#         'terms_of_trade': trade_posts[0].terms_of_trade,
#         'min_reputation': trade_posts[0].min_reputation,
#         'broadcast_trade': trade_posts[0].broadcast_trade,
#         'is_active': trade_posts[0].is_active,
#     }
