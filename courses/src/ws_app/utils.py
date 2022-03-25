from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_ws_notification_to_groups(groups, msg_type, data):
    channel_layer = get_channel_layer()

    for group in groups:
        async_to_sync(channel_layer.group_send)(
            group,
            {
                'type': msg_type,
                'data': data,
            }
        )
